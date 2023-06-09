import pandas as pd
import numpy as np
import cv2

dataset_path = './data/fer2013/fer2013.csv'
image_size = (48, 48)


def load_fer2013():  # 载入fer2013文件，放入内存
    data = pd.read_csv(dataset_path)  # 使用CSV读取方式读取dataset——path路径下的CSV文件
    pixels = data['pixels'].tolist()  # pixes是fer2013的人脸数据，为48*48的像素点，转为列表
    width, height = 48, 48
    faces = []
    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.asarray(face).reshape(width, height)  # 将数组转换为48*48的二维矩阵
        face = cv2.resize(face.astype('uint8'), image_size)  # 根据需求缩放
        faces.append(face.astype('float32'))  # 转化数据类型，添加在数组后边
    faces = np.asarray(faces)  # 转化为数组
    faces = np.expand_dims(faces, -1)  # 扩展最后一个参数
    emotions = pd.get_dummies(data['emotion']).values  # 获得标签值
    return faces, emotions


def get_labels(dataset_name):  # 获取文件标签
    if dataset_name == 'fer2013':
        return {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
                4: 'sad', 5: 'surprise', 6: 'neutral'}
    else:
        raise Exception('Invalid dataset name')


def split_data(x, y, validation_split=0.2):  # 分离训练集与验证集，validation为分出的验证比例
    num_samples = len(x)  # x的长度,x与y的长度是一致的
    num_train_samples = int((1 - validation_split) * num_samples)  # 计算需要用于训练的样本数
    # 训练样本
    train_x = x[:num_train_samples]
    train_y = y[:num_train_samples]
    # 验证样本
    val_x = x[num_train_samples:]
    val_y = y[num_train_samples:]
    # 存入两个元组并返回
    train_data = (train_x, train_y)
    val_data = (val_x, val_y)
    return train_data, val_data


def preprocess_input(x, v2=True):  # 数据归一化
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x
