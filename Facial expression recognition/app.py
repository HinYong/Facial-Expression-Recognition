import os
from flask import Flask, jsonify, request
from keras.models import load_model
from data_process import *
from image_process import *

emotion_labels = get_labels('fer2013')  # 获取情感标签
emotion_offsets = (0, 0)

detection_model_path = './model/haarcascade_frontalface_default.xml'  # 人脸检测模型
emotion_model_path = 'model/fer2013_emotion_model.65-0.68.hdf5'  # 训练出来的情绪识别模型

# 载入模型
face_detection = load_detection_model(detection_model_path)  # 返回检测模型，初始化
emotion_classifier = load_model(emotion_model_path, compile=False)  # 加载权值模型文件
emotion_target_size = emotion_classifier.input_shape[1:3]  # 获得输入模型形状

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


# 路由解析，通过用户访问路径调用相应函数
@app.route('/emotion', methods=['POST'])
def recognition():
    # 获取图片文件 name = photo
    img = request.files.get('photo')
    # 定义一个图片存放的位置 存放在static下面
    path = basedir + "/static/img/"
    # 图片名称
    imgName = img.filename
    # 图片path和名称组成图片的保存路径
    file_path = path + imgName
    # 保存图片
    img.save(file_path)
    # image_path是图片的路径
    image_path = basedir + '/static/img/' + imgName

    gray_image = load_image(image_path, grayscale=True)
    gray_image = np.squeeze(gray_image)
    gray_image = gray_image.astype('uint8')

    faces = detect_faces(face_detection, gray_image)  # 获取人脸数据
    # print(len(faces))
    result = {
        'flag': 0
    }
    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)  # 扩充
        gray_face = gray_image[y1:y2, x1:x2]  # 提取图像中人脸的部分（矩形框），并且灰度化
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))  # 重新塑形
        except:
            continue
        gray_face = preprocess_input(gray_face, True)  # 数据归一化
        gray_face = np.expand_dims(gray_face, 0)  # 扩展列
        gray_face = np.expand_dims(gray_face, -1)  # 扩展最后一个参数
        out = emotion_classifier.predict(gray_face)[0]  # 预测，概率
        index = out.argmax()  # 返回最大概率的索引值
        array = []
        for i, percent in enumerate(out):  # 计算每一个情绪识别的概率
            b = round(percent * 100, 3)
            array.append(b)
            # print(b)
        print(array)
        emotion_text = emotion_labels[index]  # 标签
        result = {
            'flag': 1,
            'angry': array[0],
            'disgust': array[1],
            'fear': array[2],
            'happy': array[3],
            'sad': array[4],
            'surprise': array[5],
            'neutral': array[6],
            'emotion_text': emotion_text
        }
    return jsonify(result)


if __name__ == '__main__':
    app.run()  # 启动服务器
