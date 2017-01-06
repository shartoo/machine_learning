# -*- coding:utf-8 -*-
'''
使用opencv 来做边缘检测
'''

import numpy as np
import cv2
import matplotlib.pyplot as plt #plt.plot(x,y) plt.show()
import os
import time

def find_cicle(img,targetPath):
    '''
      检测图像中圆形标志，并切割保存到targetPath目录中
    :param img:         检测的图片
    :param targetPath:  最后切割完成后要保存的路径
    :return:
    '''
    image = cv2.imread(img)
    # 创建一个图像副本，作为对照
    output = image.copy()
    # 转换为 单一通道的图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # param2参数意义为 累计阈值，此值越大，最终获取的圆形越小，并且是圆的准确率越高
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,20, param1=30,param2=40,minRadius=10,maxRadius=40)
    file = os.path.basename(img)
    file = file.replace(".jpg","")
    circle_list = []
    # ensure at least some circles were found
    print 'begin..'
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
        # loop over the (x, y) coordinates and radius of the circles
        i =0
        for (x, y, r) in circles:
            flag = True
            for have_circle in circle_list:
                tx,ty,tr = have_circle
                gap = (tx-x)**2+(ty-y)**2
                if gap<r**2:
                    flag =False
            if flag:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                circle_list.append((x,y,r))
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                # Crop from x, y, w, h -> 100, 200, 300, 400
                # NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]
                r = r+10   # 原始的圆形 半径太小，此处作为增加范围
                crop_img = image[y-r:y+r,x-r:x+r,:]
                #cv2.imshow("cropped", crop_img)
                saveImg = targetPath+file+"_crop_"+str(i)+".jpg"
                cv2.imwrite(saveImg,crop_img)
                print 'crop image %s saved!...'%saveImg
                #cv2.waitKey(0)
                i+=1

        # show the output image
        #cv2.imshow("output", np.hstack([image, output]))
        #cv2.imshow("output", np.hstack([output]))
        #cv2.waitKey(0)

if __name__=='__main__':
    path = 'E:\\bot_car\\data'
    targetPath = "e:\\bot_car\\data"
    allfile = os.listdir(path)
    start_time = time.time()
    count = 0
    filenum =1000  # 一个文件夹内包含多少文件
    for f in allfile:
        print "img file is :  %s  " % f
        savePath = targetPath + "_" + str(count/filenum) + "\\"
        if not os.path.exists(savePath):
            os.mkdir(savePath)
            print 'path %s   made..'%savePath
        find_cicle(os.path.join(path, f), savePath)
        count = count + 1
        print ' image processing is %d '%count
    end_time = time.time()
    print 'time consumed %d seconds '%(end_time-start_time)
    # file = r'E:\bot_car\data\full_data\03\0a04becc2c9311e69e0400505681e231.jpg'
    # find_cicle(file,'e:\\','tt.jpg')