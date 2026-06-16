# Helper functions, Point and Rectangle classes for the $1 gesture recognizer are defined here.
# This is to make the other file more readable

import math

# needed in here
PHI = 0.5 * (-1.0 + math.sqrt(5.0))


# point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# rectangle class
class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# helper functions (similar js code from https://depts.washington.edu/acelab/proj/dollar/index.html)
class Helper:

    @staticmethod
    # makes all gestures have n points
    def resample(points, n):
        points = [Point(p.x, p.y) for p in points]
        # interval length
        I = Helper.path_length(points) / (n - 1)
        # accumulated distance
        D = 0.0

        # new points (starts with first point)
        new_points = [points[0]]

        # iterator for points
        i = 1

        # resample points
        while i < len(points):
            # distance between current point and previous point
            d = Helper.distance(points[i - 1], points[i])

            # skip points with zero distance
            if d == 0.0:
                i += 1
                continue

            # accumulated distance + current distance >= interval length
            if (D + d) >= I:
                # new x and y coordinates between previous point and current point at interval length
                qx = points[i - 1].x + ((I - D) / d) * \
                    (points[i].x - points[i - 1].x)
                qy = points[i - 1].y + ((I - D) / d) * \
                    (points[i].y - points[i - 1].y)

                # new point gets added
                q = Point(qx, qy)
                new_points.append(q)
                points.insert(i, q)

                # accumulated distance reset
                D = 0.0
                i += 1

            # not enough distance yet -> accumulate more
            else:
                D += d
                i += 1

        # if we have one point too less (because of rounding errors), add the last point
        if len(new_points) == n - 1:
            new_points.append(Point(points[-1].x, points[-1].y))

        # return new points
        return new_points

    @staticmethod
    # angle between centroid and first point
    def indicative_angle(points):
        c = Helper.centroid(points)
        return math.atan2(c.y - points[0].y, c.x - points[0].x)

    @staticmethod
    # rotates points by given radians around centroid
    def rotate_by(points, radians):
        c = Helper.centroid(points)
        cos_r = math.cos(radians)
        sin_r = math.sin(radians)
        new_points = []

        for p in points:
            qx = (p.x - c.x) * cos_r - (p.y - c.y) * sin_r + c.x
            qy = (p.x - c.x) * sin_r + (p.y - c.y) * cos_r + c.y
            new_points.append(Point(qx, qy))

        return new_points

    @staticmethod
    # scales points to given size
    def scale_to(points, size):
        box = Helper.bounding_box(points)

        new_points = []
        for p in points:
            qx = p.x * (size / box.width)
            qy = p.y * (size / box.height)
            new_points.append(Point(qx, qy))
        return new_points

    @staticmethod
    # translates points to a new centroid (pt)
    def translate_to(points, pt):
        c = Helper.centroid(points)
        new_points = []
        for p in points:
            qx = p.x + pt.x - c.x
            qy = p.y + pt.y - c.y
            new_points.append(Point(qx, qy))
        return new_points

    @staticmethod
    # finds the best angle for matching points to template unistroke
    def distance_at_best_angle(points, template_unistroke, a, b, threshold):

        # test angles from a to b at phi intervals with distance to template_unistroke
        x1 = PHI * a + (1.0 - PHI) * b
        f1 = Helper.distance_at_angle(points, template_unistroke, x1)

        x2 = (1.0 - PHI) * a + PHI * b
        f2 = Helper.distance_at_angle(points, template_unistroke, x2)

        # search for minimum distance until threshold is met
        while abs(b - a) > threshold:
            # if f1 < f2 -> minimum is between a and x2 -> update b to x2
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = PHI * a + (1.0 - PHI) * b
                f1 = Helper.distance_at_angle(points, template_unistroke, x1)
            # if f1 >= f2 -> minimum is between x1 and b -> update a to x1
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = (1.0 - PHI) * a + PHI * b
                f2 = Helper.distance_at_angle(points, template_unistroke, x2)

        # return the minimum distance
        return min(f1, f2)

    @staticmethod
    # distance between points and template unistroke at given angle
    def distance_at_angle(points, template_unistroke, radians):
        new_points = Helper.rotate_by(points, radians)
        return Helper.path_distance(new_points, template_unistroke.points)

    @staticmethod
    # calculates the centroid of a set of points
    def centroid(points):
        x = 0.0
        y = 0.0
        for p in points:
            x += p.x
            y += p.y
        return Point(x / len(points), y / len(points))

    @staticmethod
    # calculates the bounding box of a set of points
    def bounding_box(points):
        min_x = float("inf")
        max_x = float("-inf")
        min_y = float("inf")
        max_y = float("-inf")

        # get min and max x and y coordinates
        for p in points:
            min_x = min(min_x, p.x)
            min_y = min(min_y, p.y)
            max_x = max(max_x, p.x)
            max_y = max(max_y, p.y)

        # rectangle with top left corner (min_x, min_y) and width and height of max_x - min_x and max_y - min_y
        return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

    @staticmethod
    # calculates the average distance between 2 lists of points
    def path_distance(pts1, pts2):
        d = 0.0
        for i in range(len(pts1)):
            d += Helper.distance(pts1[i], pts2[i])
        return d / len(pts1)

    @staticmethod
    # calculates the total length of a path by adding the distance between each point and the next one
    def path_length(points):
        d = 0.0
        for i in range(1, len(points)):
            d += Helper.distance(points[i - 1], points[i])
        return d

    @staticmethod
    # calculates the distance between two points
    def distance(p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    # converts degrees to radians
    def deg2rad(d):
        return d * math.pi / 180.0
