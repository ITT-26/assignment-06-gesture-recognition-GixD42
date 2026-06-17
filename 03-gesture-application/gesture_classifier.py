from constants import *
from sklearn.preprocessing import StandardScaler
from scipy.signal import resample
from keras.models import load_model
import numpy as np
from pathlib import Path
import os
import logging
import warnings

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)


class GestureClassifier:
    def __init__(self):

        # base directory
        base_dir = Path(__file__).resolve().parent
        repo_root = base_dir.parent

        # path to model
        model_path = repo_root / "model" / "model_lstm_64.keras"
        # load model
        self.model = load_model(str(model_path))

        # number of points to resample to (same as in training)
        self.num_points = 64

        # class names in the same order as the model output
        self.class_names = ['arrow', 'caret', 'check', 'circle', 'delete_mark', 'left_curly_brace', 'left_sq_bracket',
                            'pigtail', 'rectangle', 'right_curly_brace', 'right_sq_bracket', 'star', 'triangle', 'v', 'x']

    def predict(self, points):
        if len(points) < 20:
            return None, 0.0

        arr = np.array(points, dtype=float)

        # adjust y axis (pyglet y is inverted compared to typical Cartesian coordinates)
        arr[:, 1] = -arr[:, 1]

        # same preprocessing as in the notebook
        scaler = StandardScaler()
        arr = scaler.fit_transform(arr)
        arr = resample(arr, self.num_points)

        x = np.expand_dims(arr, axis=0)
        probs = self.model.predict(x, verbose=0)[0]
        idx = int(np.argmax(probs))

        # only return gestures for spell
        if self.class_names[idx] not in SPELLS:
            return None, 0.0

        # only return if above threshold
        if probs[idx] < SPELL_THRESHOLD:
            return None, 0.0

        # return predicted class and confidence
        return self.class_names[idx], float(probs[idx])
