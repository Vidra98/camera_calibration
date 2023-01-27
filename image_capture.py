import cv2
import os
import json
import numpy as np

cam = cv2.VideoCapture('http://192.168.1.90/mjpg/4/video.mjpg?resolution=1280x720&fps=15')

cv2.namedWindow("test")

# file = open(os.getcwd()+os.sep+'camera_calib/chessboard/logitech_720p/calibration/camera_calibration.json')
# data = json.load(file)
# camera_matrix = np.array(data['camera_matrix'])

# dist_coef = np.array(data['dist_coeff'])
#optimal_mtx = np.array(data['optimal_camera_matrix'])


img_counter = 0
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # h,  w = frame.shape[:2]
    # newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coef, (w,h), 1, (w,h))
    
    # dst = cv2.undistort (frame, camera_matrix, dist_coef, None, newcameramtx)
    # x,y,w,h = roi
    # dst = dst[y:y+h,x:x+w]
    cv2.imshow("test", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = os.getcwd()+os.sep+"camera_calib"+os.sep+"chessboard"+os.sep+ \
            "opencv_frame_{}.jpg".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

cam.release()

cv2.destroyAllWindows()
