import cv2
import os
import json
import numpy as np
from pathlib import Path
cam = cv2.VideoCapture('http://192.168.1.90/mjpg/1/video.mjpg?resolution=1280x720&fps=15')

# file = open(os.getcwd()+os.sep+'camera_calib/chessboard/logitech_720p/calibration/camera_calibration.json')
# data = json.load(file)
# camera_matrix = np.array(data['camera_matrix'])

# dist_coef = np.array(data['dist_coeff'])
#optimal_mtx = np.array(data['optimal_camera_matrix'])

width= int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

Path("video").mkdir(parents=True, exist_ok=True)

raw= cv2.VideoWriter('video/raw.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
undistort= cv2.VideoWriter('video/undistort.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

camera_matrix = np.array([[1045.4240520318192, 0.0, 656.8591393400732], [0.0, 1047.6985288571932, 351.21556690420397], [0.0, 0.0, 1.0]])
dist_coef = np.array([-0.31928293576568206, 0.20711792169154086, 0.006682067922980928, 0.0009386492940249929, -0.09308734213915967])

video_counter = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # h,  w = frame.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coef, (w,h), 1, (w,h))
    
    undistort_frame = cv2.undistort(frame, camera_matrix, dist_coef, None)
    # x,y,w,h = roi
    # dst = dst[y:y+h,x:x+w]
    raw.write(frame)
    undistort.write(undistort_frame)

    cv2.imshow('frame', frame)
    cv2.imshow('undistort', undistort_frame)
    cv2.moveWindow('undistort',1500,0)
    cv2.moveWindow('frame',0,500)
    key = cv2.waitKey(1)
    if key == 32:
        video_counter += 1
        raw.release()
        undistort.release()
        raw= cv2.VideoWriter('video/raw' + str(video_counter) + '.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
        undistort= cv2.VideoWriter('video/undistort' + str(video_counter) + '.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))
    if key == 27:
        break

cam.release()
raw.release()
undistort.release()
cv2.destroyAllWindows()
