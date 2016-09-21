# -*- coding:utf-8 -*-
'''
gif图片转换为 jpg

'''
from PIL import Image
import os
import os.path
import shutil
import re

dir = "D:\\TestData\\ImgClassify\\Testset5"
for root, dirs, files in os.walk(dir):
    i = 0
    pathArray = re.split('/|\\\\', root)
    newroot = root
    newroot = newroot.replace(pathArray[len(pathArray)-1], pathArray[len(pathArray)-1]+"_jpeg")
    if not os.path.exists(newroot):
        os.mkdir(newroot)
        print 'create dir newroot successfully...'

    for name in files:
        tmpFile = root+"\\"+name
        if not tmpFile.endswith(".jpg"):
            im = Image.open(tmpFile)
            im = im.convert('RGB')
            targetFile = newroot + "/" + name.split(".")[0] + ".jpg"
            im.save(targetFile, "jpeg")  # 保存图像为png格式
            i = i+1
        else:
            targetFile = newroot+"\\"+name
            shutil.copyfile(tmpFile, targetFile)
    if i%2==0:
        print("picture transfer %d"%i)