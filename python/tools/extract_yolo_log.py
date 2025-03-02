# coding=utf-8
# 该文件用来提取训练log，去除不可解析的log后使log文件格式化，生成新的log文件供可视化工具绘图

def extract_log(log_file,new_log_file,key_word):
f = open(log_file)
train_log = open(new_log_file, 'w')
for line in f:
    # 去除多gpu的同步log
    if 'Syncing' in line:
        continue
    # 去除除零错误的log
    if 'nan' in line:
        continue
    if key_word in line:
        train_log.write(line)

f.close()
train_log.close()

extract_log('person_train_log.txt','person_train_log_loss.txt','images')   #voc_train_log.txt 用于绘制loss曲线
extract_log('person_train_log.txt','person_train_log_iou.txt','IOU')