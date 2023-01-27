import cv2
import os
import json
import numpy as np

file = open(os.getcwd()+os.sep+'calibration/camera_calibration.json')
data = json.load(file)
mtx = np.array(data['camera_matrix'])

dist = np.array(data['dist_coeff'])
#optimal_mtx = np.array(data['optimal_camera_matrix'])
print('\nCamera Matrix:\n', mtx)
print('\nDistortion Parameters:\n',dist)


img = cv2.imread(os.getcwd()+os.sep+'camera_calib/chessboard/opencv_frame_37.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0)
dst = cv2.undistort(img, mtx, dist,  mtx)

x,y,w,h = roi
print("roi : ",roi,"\n")
print("new cameramtx",newcameramtx, "\n h,w :", h,w)
dst = dst[y:y+h,x:x+w]
cv2.imwrite(os.getcwd()+os.sep+'camera_calib/cali+result1.jpg',dst)

mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
dst2 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
# dst2 = dst2[y:y+h, x:x+w]
cv2.imwrite(os.getcwd()+os.sep+'camera_calib/cali+result2.jpg',dst2)

cv2.imshow("2",dst2)
cv2.waitKey(0)
#cam = cv2.VideoCapture(0)
camera_matrix=mtx.tolist()
optimal_camera_matrix = newcameramtx.tolist()
dist_coeff = dist.tolist()
# rot_vect = np.array(rvecs).tolist()
# tra_vect = np.array(tvecs).tolist()
data = {"camera_matrix": camera_matrix, "dist_coeff": dist_coeff, "optimal_camera_matrix": optimal_camera_matrix}
# vectors = {"rotation_vectors":rot_vect,"translation_vectors":tra_vect}
fname = "camera_calibration.json"
import json
with open(fname, "w") as f:
    print(data)
    json.dump(data, f)
# fname = "vectors.json"
# with open(fname, "w") as f:
#     print(vectors)
#     json.dump(vectors, f)