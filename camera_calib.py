import numpy as np
import glob
import cv2
import os

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*8,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob(os.getcwd()+os.sep+'camera_calib/chessboard/*.jpg')

for fname in images:
    
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   
    
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (8,6), None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (8,6), corners2, ret)
        cv2.imshow('img', img)
        print(fname)
        cv2.waitKey(10)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print('Camera calibrated:',ret)
print('\nCamera Matrix:\n', mtx)
print('\nDistortion Parameters:\n',dist)
print('\nRotation Vectors:\n',rvecs)
print('\nTranslation Vectors:\n',tvecs)


img = cv2.imread(os.getcwd()+os.sep+'camera_calib/chessboard/opencv_frame_36.jpg')
h,  w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 0, (w,h))
dst = cv2.undistort(img, mtx, dist, None, mtx)

x,y,w,h = roi
# dst = dst[y:y+h,x:x+w]
cv2.imwrite(os.getcwd()+os.sep+'camera_calib/cali+result1.jpg',dst)

mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
dst2 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
# crop the image
x, y, w, h = roi
# dst2 = dst2[y:y+h, x:x+w]
cv2.imwrite(os.getcwd()+os.sep+'camera_calib/cali+result2.jpg',dst2)

#cam = cv2.VideoCapture(0)
camera_matrix=mtx.tolist()
optimal_camera_matrix = newcameramtx.tolist()
dist_coeff = dist.tolist()
rot_vect = np.array(rvecs).tolist()
tra_vect = np.array(tvecs).tolist()
data = {"camera_matrix": camera_matrix, "dist_coeff": dist_coeff, "optimal_camera_matrix": optimal_camera_matrix}
vectors = {"rotation_vectors":rot_vect,"translation_vectors":tra_vect}
fname = "camera_calibration.json"
import json
with open(fname, "w") as f:
    print(data)
    json.dump(data, f)
fname = "vectors.json"
with open(fname, "w") as f:
    print(vectors)
    json.dump(vectors, f)



"""while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("sin correccion", frame)
    dst = cv2.undistort (frame, mtx, dist, None, newcameramtx)
    x,y,w,h = roi
    dst = dst[y:y+h,x:x+w]
    dst2 = cv2.remap(frame, mapx, mapy, cv2.INTER_LINEAR)
    x, y, w, h = roi
    dst2 = dst2[y:y+h, x:x+w]
    
    cv2.imshow("con correccion1", dst)
    cv2.imshow("con correccion2", dst2)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    
cam.release()

cv2.destroyAllWindows()"""