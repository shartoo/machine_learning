# -*- coding:utf-8 -*-
'''
以web接口访问虫数据，向虫数据提交一张图片，并返回识别图像中文字的结果
'''
import json
import requests
import sys

if __name__=='__main__':
    from poster.encode import multipart_encode
    from poster.streaminghttp import register_openers
    import urllib2
    import time

    # Register the streaming http handlers with urllib2
    register_openers()
    root_url ='http://chongdata.com/ocr/'
    # Start the multipart/form-data encoding of the file "DSC0001.jpg"
    # "image1" is the name of the parameter, which is normally set
    # via the "name" parameter of the HTML <input> tag.

    # headers contains the necessary Content-Type and Content-Length
    # datagen is a generator object that yields the encoded parameters
    datagen, headers = multipart_encode({"file": open(r"C:\Users\xiatao\Desktop\20099126854760569.jpg", "rb")})
    values = {"langs[]":"cn_sim"}
    # Create the Request object
    request = urllib2.Request(root_url+"upload_file.php", datagen, headers,values)
    # Actually do the request, and get the response
    upfile_result = urllib2.urlopen(request).read()
    print upfile_result
    import re
    result_arr = re.split(r'[;=\']',upfile_result)
    redirect_url = root_url+"wait_res.php?resocr="+result_arr[-2]
    print ".....等待75秒，再次请求.....",redirect_url
    time.sleep(75)
    request_final  = urllib2.Request(redirect_url)
    ocr_out = urllib2.urlopen(request_final).read()
    print "==============OCR 识别结果如下======================"
    print ocr_out
