
/*

compute different of two images.Used for static goods detection
*/

#include "stdafx.h"
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<opencv2/core/core.hpp>

#define threshold_diff1 10 //threshold of difference of frames
#define threshold_diff2 10
using namespace cv;
using namespace std;

int main()
{
	Mat img_src1, img_src2, img_src3;  //a 3-frames  difference 
	Mat img_dst, gray1, gray2, gray3;
	Mat gray_diff1, gray_diff2;       // save subtraction result of two frames
	Mat gray;						 //show foreground
	bool pause = false;
	VideoCapture cap(0);
	if (!cap.isOpened())
	{
		printf("camera not ready..");
		return -1;
	}

	for (;;)
	{
		if (!false)
		{
			cap>> img_src1;
			GaussianBlur(img_src1,img_src1,Size(3,3),0);
			cvtColor(img_src1, gray1, CV_BGR2GRAY);

			waitKey(5);
			cap >> img_src2;
			GaussianBlur(img_src2, img_src2, Size(3, 3), 0);
			cvtColor(img_src2,gray2,CV_BGR2GRAY);
			imshow("video src",img_src2);

			waitKey(5);
			cap >> img_src3;
			GaussianBlur(img_src3, img_src3, Size(3, 3), 0);
			cvtColor(img_src3, gray3, CV_BGR2GRAY);

			subtract(gray2, gray1, gray_diff1);   // the second frame subtract the firt frame
			subtract(gray3, gray2, gray_diff2);   // the thrid frame subtract the second frame
			
			for (int i = 0; i < gray_diff1.rows; i++)
			{
				for (int j = 0; j < gray_diff1.cols; j++)
				{
					if (abs(gray_diff1.at<unsigned char>(i, j)) > threshold_diff1)
						gray_diff1.at<unsigned char>(i, j) = 255;					//
					else
						gray_diff1.at<unsigned char>(i, j) = 0;

					if (abs(gray_diff2.at<unsigned char>(i, j)) > threshold_diff2)
						gray_diff2.at<unsigned char>(i, j) = 255;
					else
						gray_diff2.at<unsigned char>(i, j) = 0;

			    }
				bitwise_and(gray_diff1, gray_diff2, gray);
				imshow("foreground", gray);
			 }
			char c = (char)waitKey(10);
			if (c == 27)
			{
				break;
			}
			else if (c == ' ')
				pause != pause;
		}
	}
    return 0;
}

