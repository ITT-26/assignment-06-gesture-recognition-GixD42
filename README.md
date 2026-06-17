[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/iuYZxbvR)

# 0 Requirements and installation

- Python (3.13 used to code this)
- Install requirements using pip install -r requirements.txt
- The data logs from GRIPS should be stored under datasets/logs

# 1 Implementing the $1 Gesture Recognizer

Usage: ```python gesture_input.py```<br>
An Input Field with instant feedback appears.
Draw with your mouse (you have to hold down the left mouse button)

The recognizer is heavily based on the JavaScript code from this [website](https://depts.washington.edu/acelab/proj/dollar/index.html).

The Protractor was not implemented since it is not the original Recognizer.<br>
All the gestures from the site were implemented but the "zigzag"-gesture because our logs didn't contain them.

# 2 Comparing Gesture Recognizers

To record unistrokes the script unistroke_recorder.py was used.<br>
The data is stored under datasets/mylogs.<br>
The actual assignment is in lstm_demo_starter.ipynb which is based on the notebook from class.<br>
5 different parameters were compared and the conclusion was that 64 works the best while 128 started overfitting.<br>
The Dollar Recognizer didn't really compete with the trained models in terms of performance.

# 3 Gesture Detection Game

In the game Gesture Magic you control a wizard that can use spells with his book.<br>
To use spells you have to perform gestures.<br>
On the left page you find your spells and you can see the cooldown of your magical powers.<br>
Flying enemies cannot be targeted using your earthshaker spell.<br>
Grounded enemies are immune to your sky beam.<br>
No enemy can dodge your starfall spell.<br>
Your goal is to survive as long as you can.<br>
(if the game is too easy or too hard you can play around with some parameters in the constants.py)<br><br>
To start the game use: ```python gesture_application.py```<br>
Your game will have to load a few seconds to use the model.<br>
Once everything is ready you can start the game by pressing the spacebar.