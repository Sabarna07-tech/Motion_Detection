from yolo_manager import YoloManager
from mediapipe_manager import MedipapipeManager
from motion import MOTION
from optical_flow import OpticalFlow
import cv2
import numpy as np

ym = YoloManager()
mm = MedipapipeManager()
mo = MOTION("skeleton.json",
            r"data/custom_skeleton_pose_data/models/svm_motion_model1.pkl",
            r"data/custom_skeleton_pose_data/models/scaler.pkl")

cap = cv2.VideoCapture(0)

# Initialize optical flow
optical_flow = OpticalFlow()
ret, prev_frame = cap.read()
optical_flow.initialize(prev_frame)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame for better visibility
    frame = cv2.resize(frame, (1280, 720))

    # Detect humans using YOLO
    detections = ym.detect(frame)
    # mediapipe detection
    coordinates, skeletons = mm.getSkeletons(detections, frame)
    # motion detection
    motions = mo.getMotion(coordinates, skeletons)

    # Annotate the bounding box and motion label
    for cords, motion in zip(coordinates, motions):
        cv2.rectangle(frame, cords[0], cords[1], (0, 255, 0), 2)
        cv2.putText(frame, motion, (cords[0][0], cords[0][1] + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (58, 125, 255), 2)

    # Optical flow analysis
    rgb_flow = optical_flow.compute_flow(frame)

    # Overlay optical flow on the frame
    frame = cv2.addWeighted(frame, 0.7, rgb_flow, 0.3, 0)

    # Display the processed video
    cv2.imshow("Real-Time Motion Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()



