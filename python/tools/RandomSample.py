# -*- coding:utf-8 -*-
'''
随机抽样某个文件夹下数据,并复制到新的文件夹。新文件夹以程序运行时间的小时分钟和_train或_test组成
'''
import os
import random
import re
import time;
import copy
import shutil

def getPathAndLabel(path):
    '''
    :param path:   将要获取的目录位置  ，比如   /home/data/
    :return:            该目录下所有子目录和对应的文件名列表  { subpath1:[file1,file2...], subpath2:[file_a,file_b,...]....}
    '''
    pathLabel ={}
    for tmppath in os.listdir(path):
  #      print tmppath
        if not os.path.isfile(os.path.join(path,tmppath)):
            pathDir = tmppath
            img_names=[]
            subpath =os.path.join(path,tmppath)
            for f in os.listdir(subpath):
                #print f
                if os.path.isfile(os.path.join(subpath,f)):
                    img_names.append(f)
            pathLabel[pathDir]=img_names
    return pathLabel

def process(mypath, percent):

    # ####  以当前时间小时分钟 作为新数据集的父目录中的关键词######
    pathArray = re.split('/|\\\\',mypath)
    newPath = mypath
    # 根据当前时间重命名新生成的随机数
    ticks = time.strftime("%Y-%m-%d %H%M", time.localtime())
    timeStr = str(ticks.split(" ")[1])

    ######  创建训练目录###########
    newTrainPath = newPath.replace(pathArray[len(pathArray)-1],timeStr+"_train")
    print newTrainPath
    if not os.path.exists(newTrainPath):
        os.mkdir(newTrainPath)
        print "create path %s successfully"%str(newTrainPath)
    #####  创建测试目录 ###########
    newTestPath = newPath.replace(pathArray[len(pathArray) - 1], timeStr + "_test")
    print newTestPath
    if not os.path.exists(newTestPath):
        os.mkdir(newTestPath)
        print "create path %s successfully" % str(newTestPath)

    dirAndfiles = getPathAndLabel(mypath)

    ##遍历当前文件夹下所有子目录的所有文件，并重新复制数据
    for parentPath in dirAndfiles.keys():
        completeTrainSubPath = os.path.join(newTrainPath,parentPath)   # 构建训练集的完整子目录，只是将当前目录换名字了
        if not os.path.exists(completeTrainSubPath):                                 # 子目录需要手动创建
            os.mkdir(completeTrainSubPath)
            print "create path %s successfully" % str(completeTrainSubPath)

        completeTestSubPath = os.path.join(newTestPath, parentPath)  # 构建测试集的完整子目录，只是将当前目录换名字了
        if not os.path.exists(completeTestSubPath):  # 子目录需要手动创建
            os.mkdir(completeTestSubPath)
            print "create path %s successfully" % str(completeTestSubPath)

        test_sample = random.sample(dirAndfiles[parentPath],int(len(dirAndfiles[parentPath])*percent))  #从当前子目录文件列表中抽样percent比率的文件
        baseDataCompletePath = os.path.join(mypath,parentPath)
        # 复制    测试    文件到测试目录
        for file in test_sample:
            sourceFile = os.path.join(baseDataCompletePath,file)
            targetFile = os.path.join(completeTestSubPath,file)
            shutil.copyfile(sourceFile,  targetFile)
            print "copy file from %s to  %s successfully!"%(sourceFile,targetFile)
        # 复制    训练   文件到训练目录
        for file in dirAndfiles[parentPath]:
            num = 0
            if file not in test_sample:
                if num<7300:
                    sourceFile = os.path.join(baseDataCompletePath,file)
                    targetFile = os.path.join(completeTrainSubPath,file)
                    shutil.copyfile(sourceFile,  targetFile)
                    print "copy file from %s to  %s successfully!"%(sourceFile,targetFile)
            num = num +1
        print 'coped file number is %d'%num


if __name__=='__main__':
    process("/data/bot_img/all_img_tilltest4_withlabel",0.2)


