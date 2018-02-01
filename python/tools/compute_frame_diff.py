# -*- coding:utf-8 -*-
'''
compute difference of two frame to detect goods changes in robot
'''

import cv2
import numpy as np
import time


def compute_img_diff(frame1,frame2,threshold = 30):
    '''
        compute difference of two frame to detect goods changes in robot

    :param frame1:
    :param frame2:
    :return:            difference of two frame
    '''
    frame1 = cv2.GaussianBlur(frame1, (3, 3), 0)
    gray1 = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    frame2 = cv2.GaussianBlur(frame2, (3, 3), 0)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray img1",gray1)
    cv2.imshow("gray img2", gray2)
    #diff_frame = np.zeros((gray2.shape))
    diff_frame = cv2.subtract(gray1,gray2)
    diff_frame[diff_frame>threshold] = 255
    diff_frame[diff_frame<=threshold] = 0
    # for i in range(diff_frame.shape[0]):
    #     for j in range(diff_frame.shape[1]):
    #         if abs(diff_frame[i][j])>threshold:
    #             diff_frame[i][j] = 255
    #         else:
    #             diff_frame[i][j] = 0
    return diff_frame


# cap =  cv2.VideoCapture(0)
# while True:
#     ret, frame = cap.read()
#     frame1 = frame
#
#     time.sleep(0.05)
#     ret, frame = cap.read()
#     frame2 =frame
#
#     diff_frame = compute_img_diff(frame1,frame2)
#
#     cv2.imshow("difference of frames",diff_frame)
#
# cv2.waitKey(0)


frame1 = cv2.imread("D:/data/robot_auto_seller/robot_auto_seller_2layers/all/images/3_kangshifu_7.jpg")
frame2 = cv2.imread("D:/data/robot_auto_seller/robot_auto_seller_2layers/all/images/3_kangshifu_8.jpg")
diff_frame = compute_img_diff(frame1,frame2)
cv2.imshow("difference of frames",diff_frame)
cv2.waitKey(0)