"""Test crop image"""

# pylint: disable=no-member
import cv2

# Start coords for crop
Y = 235
X = 240
# Height and width for crop
H = 45
W = 480


img = cv2.imread("sample_full.jpg")
crop_img = img[Y : Y + H, X : X + W]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)
