import mediapipe as mp
import numpy as np

class Person:
    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils

    def __init__(self):
        self.name = ""
        self.age = 16

    @staticmethod ## It is not called prior to object init
    def calculate_angle(a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)
        if angle > 180.0:
            angle = 360 - angle
        return angle

    def detect_reps(self, results, exercise, count, stage, thresholds):
        if not results.pose_landmarks:
            return count, stage

        landmarks = results.pose_landmarks.landmark

        if exercise == "pushup":
            shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = self.calculate_angle(shoulder, elbow, wrist)

            if angle > thresholds["pushup_up"]:
                stage = "up"
            elif angle < thresholds["pushup_down"] and stage == "up":
                stage = "down"
                count += 1

        elif exercise == "situp":
            shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            angle = self.calculate_angle(shoulder, hip, knee)

            if angle > thresholds["situp_up"]:
                stage = "down"
            elif angle < thresholds["situp_down"] and stage == "down":
                stage = "up"
                count += 1

        return count, stage