import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from readmala2 import readmala2
import cv2
import time
import matplotlib.colors as mcolors


start_time=time.time()
matplotlib.use('TkAgg')
dataFolder = 'E:\Mayihang\\2023_1_30\\200MHz_rawdata\ASCII'
outputpath = 'E:\\Mayihang\\雷达数据集\\200Mhzdata\\images'
file = 'E:/Mayihang/2023_1_30/zhengding/ASCII/20230224ZHENGDINGHENGZHOUBEIJIE_001_A1'
file_list = [file for file in os.listdir(dataFolder) if file.endswith('.RD3')]
os.chdir(dataFolder)
for file_name in file_list:
    file_name1 = os.path.splitext(file_name)[0]
    file_name = os.path.join(dataFolder, file_name1)
    header, Data = readmala2(file_name)
    start = 0
    distance = header['DISTANCE_INTERVAL']
    # 计算数组的最大值和最小值
    max_val = np.max(Data)
    min_val = np.min(Data)
    max_val=max(abs(max_val),abs(min_val))
    # 归一化到 [-1, 1]
    Data = Data.astype(float)
    Data = Data/max_val
    d = int(17 / distance)

    if Data.shape[1]*distance<20:
        Data=cv2.resize(Data, (600, int(Data.shape[1] * distance / 20 * 600)))
        meandata = np.mean(Data)
        colVector = meandata * np.ones((600, 600 - Data.shape[0]))  # 生成 600 行 1 列每个元素都为 meandata 的列向量
        Data=np.transpose(Data)
        Data = np.concatenate((Data, colVector), axis=1)
        plt.imshow(Data, cmap='gray', vmin=-0.5, vmax=0.5)
        plt.axis('off')
        plt.savefig(os.path.join(outputpath, file_name1 + '.png'), bbox_inches='tight', pad_inches=0, dpi=170)
        plt.clf()
    else:

        while (int(20 / header['DISTANCE_INTERVAL']) + start < Data.shape[1]):

            Data1 = Data[start:int(20 / header['DISTANCE_INTERVAL']) + start,:]
            start = start + d
            Data1 = np.transpose(Data1)
            Data1=cv2.resize(Data1,(600,600))

            plt.imshow(Data1, cmap='gray',vmin=-0.1,vmax=0.1)
            plt.axis('off')
            plt.savefig(outputpath+'{}.png'.file_name+format(start),bbox_inches='tight',pad_inches = 0,dpi=170)
            plt.clf()
            if int(20 / header['DISTANCE_INTERVAL']) + start>Data.shape[1]:
                Data = cv2.resize(Data, (600, int(Data.shape[1] * distance / 20 * 600)))
                meandata = np.mean(Data)
                colVector = meandata * np.ones((600, 600 - Data.shape[0]))  # 生成 600 行 1 列每个元素都为 meandata 的列向量
                Data = np.transpose(Data)
                Data = np.concatenate((Data, colVector), axis=1)
                plt.imshow(Data1, cmap='gray', vmin=-0.1, vmax=0.1)
                plt.axis('off')
                plt.savefig(outputpath + f'{start}.png'.format(file_name+start), bbox_inches='tight', pad_inches=0, dpi=170)
                plt.clf()
                break
    end_time=time.time()
print("总共运行时间是:{}秒".format(-(start_time-end_time)))