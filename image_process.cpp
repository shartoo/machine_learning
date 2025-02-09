// image_process.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"    
#include<io.h>
#include<opencv2/highgui.hpp>
#include<opencv2/imgproc.hpp>
#include <iostream>
#include <vector>
#include <filesystem>

using namespace std;
using namespace cv;

vector<string> res;

int image_process(string img_name,string target_path)
{	
	Mat image;
	// Just loaded image Lenna.png from project dir to LoadedImage Mat
	cout << "processing image " + img_name << endl;
	image = imread(img_name, IMREAD_COLOR);
	Size size(256, 256);//the dst image size,e.g.100x100
	Mat dst;//dst image
	resize(image, dst, size);//resize image
	Rect lefTopROI(Point(0,0), Point(224, 224));
	Rect rightTopROI(Point((256 - 224), 0), Point(256, 224));
	Rect leftBotROI(Point(0, (256 - 224)), Point(224, 256));
	Rect rightBotROI(Point((256 - 224), (256 - 224)), Point(256, 256));
	Rect centerROI(Point((256 - 224)/2,(256 -224)/2), Point(256-(256-224)/2,256-(256-224)/2));

	Mat lefTopCroppedImage = dst(lefTopROI);
	Mat rightTopCroppedImage = dst(rightTopROI);
	Mat leftBotCroppedImage = dst(leftBotROI);
	Mat rightBotCroppedImage = dst(rightBotROI);
	Mat centerCroppedImage = dst(centerROI);

	Mat leftTopFlip;
	Mat rightTopFlip;
	Mat leftBotFlip;
	Mat rightBotFlip;
	Mat centerFlip;

	flip(lefTopCroppedImage, leftTopFlip, 1);
	flip(rightTopCroppedImage, rightTopFlip, 1);
	flip(leftBotCroppedImage, leftBotFlip, 1);
	flip(rightBotCroppedImage, rightBotFlip, 1);
	flip(centerCroppedImage, centerFlip, 1);

	imwrite(target_path.replace(target_path.rfind(".jpg"), target_path.size(),"_leftTop_.jpg"), lefTopCroppedImage);
	imwrite(target_path.replace(target_path.rfind("_leftTop_.jpg"), target_path.size(), "_rightTop_.jpg"), rightTopCroppedImage);
	imwrite(target_path.replace(target_path.rfind("_rightTop_.jpg"), target_path.size(), "_leftBot_.jpg"), leftBotCroppedImage);
	imwrite(target_path.replace(target_path.rfind("_leftBot_.jpg"), target_path.size(), "_rightBot_.jpg"), rightBotCroppedImage);
	imwrite(target_path.replace(target_path.rfind("_rightBot_.jpg"), target_path.size(), "_center_.jpg"), centerCroppedImage);

	imwrite(target_path.replace(target_path.rfind("_center_.jpg"), target_path.size(), "_leftTopFlip_.jpg"), leftTopFlip);
	imwrite(target_path.replace(target_path.rfind("_leftTopFlip_.jpg"), target_path.size(), "_rightTopFlip_.jpg"), rightTopFlip);
	imwrite(target_path.replace(target_path.rfind("_rightTopFlip_.jpg"), target_path.size(), "_leftBotFlip_.jpg"), leftBotFlip);
	imwrite(target_path.replace(target_path.rfind("_leftBotFlip_.jpg"), target_path.size(), "_rightBotFlip_.jpg"), rightBotFlip);
	imwrite(target_path.replace(target_path.rfind("_rightBotFlip_.jpg"), target_path.size(), "_centerFlip_.jpg"), centerFlip);
	cout << "saving to " + target_path << endl;
}


void getFiles(string path, vector<string>& files)
{
	//文件句柄  
	intptr_t    hFile = 0;
	//文件信息  
	struct _finddata_t fileinfo;
	string p;
	if ((hFile = _findfirst(p.assign(path).append("\\*").c_str(), &fileinfo)) != -1)
	{
		do
		{
			//如果是目录,迭代之  
			//如果不是,加入列表  
			if ((fileinfo.attrib &  _A_SUBDIR))
			{
				if (strcmp(fileinfo.name, ".") != 0 && strcmp(fileinfo.name, "..") != 0)
					getFiles(p.assign(path).append("/").append(fileinfo.name), files);
			}
			else
			{
				files.push_back(p.assign(path).append("/").append(fileinfo.name));
			}
		} while (_findnext(hFile, &fileinfo) == 0);
		_findclose(hFile);
	}
}


int main()
{	
	cout << "begin..." << endl;
	string filePath = "d:/workspace/python/alexnet_image_sence_classify/data/train";
	string savedPath = "d:/workspace/python/alexnet_image_sence_classify/data/preprocessed";
	for (int m = 0; m < 10; m++)
	{
		string currPath = filePath + "/c" + to_string(m);
		cout << "process " + currPath << endl;
		vector<string> files;
		getFiles(currPath,files);
		int size = files.size();
		cout << "size is:\t"+to_string(size) << endl;
		for (int i = 0; i < size; i++)
		{
			string savePath = files[i];
			image_process(files[i], savePath.replace(54, 5, "preprocessed"));
		}
	}

}