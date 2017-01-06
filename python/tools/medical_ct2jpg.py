# -*- coding:utf-8 -*-
'''
将医疗图像CT 转换为jpg格式
'''
import SimpleITK as sitk
import numpy as np
import csv
import os
from PIL import Image
import matplotlib.pyplot as plt

def load_itk_image(filename):
	itkimage = sitk.ReadImage(filename)
	numpyImage = sitk.GetArrayFromImage(itkimage)
	numpyOrigin = np.array(list(reversed(itkimage.GetOrigin())))
	numpySpacing = np.array(list(reversed(itkimage.GetSpacing())))
	return numpyImage, numpyOrigin, numpySpacing
	
def readCSV(filename):
	lines = []
	with open(filename, "rb") as f:
		csvreader = csv.reader(f)
		for line in csvreader:
			lines.append(line)
	return lines
	
def worldToVoxelCoord(worldCoord, origin, spacing):
	stretchedVoxelCoord = np.absolute(worldCoord - origin)
	voxelCoord = stretchedVoxelCoord / spacing
	return voxelCoord

def normalizePlanes(npzarray):
	maxHU = 400.
	minHU = -1000.
	npzarray = (npzarray - minHU) / (maxHU - minHU)
	npzarray[npzarray>1] = 1.
	npzarray[npzarray<0] = 0.
	return npzarray
	
img_path = "C:/subset0/1.3.6.1.4.1.14519.5.2.1.6279.6001.640729228179368154416184318668.mhd"
cand_path = "C:/subset0/candidates.csv"

numpyImage, numpyOrigin, numpySpacing = load_itk_image(img_path)
print numpyImage.shape
print numpyOrigin
print numpySpacing

cands = readCSV(cand_path)
#print cands
# get candidates
for cand in cands[1:]:
	worldCoord = np.asarray([float(cand[3]),float(cand[2]),float(cand[1])])
	voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
	voxelWidth = 65

pic_index =0
for cand in cands[1:]:
	worldCoord = np.asarray([float(cand[3]),float(cand[2]),float(cand[1])])
	voxelCoord = worldToVoxelCoord(worldCoord, numpyOrigin, numpySpacing)
	voxelWidth = 65
	patch = numpyImage[voxelCoord[0],voxelCoord[1]-voxelWidth/2:voxelCoord[1]+voxelWidth/2,voxelCoord[2]-voxelWidth/2:voxelCoord[2]+voxelWidth/2]
	patch = normalizePlanes(patch)
	print "data"
	print worldCoord
	print voxelCoord
	print patch
	#outputDir = ’patches/’
	plt.imshow(patch, cmap="gray")
	#plt.show()
	plt.savefig("d:/lungNow/%s.jpg"%pic_index)
	img = Image.open("d:/lungNow/%s.jpg"%pic_index)
	img.thumbnail((64, 64), Image.ANTIALIAS)  # resizes image in-place
	img.save("d:/lungNow/%s.jpg"%pic_index,"JPEG")
	pic_index=pic_index+1

