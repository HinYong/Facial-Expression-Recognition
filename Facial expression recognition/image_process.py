import cv2
from keras.preprocessing import image


def load_image(image_path, grayscale=False, target_size=None):
    # 载入图像，图像路径,灰度化，塑形
    pil_image = image.load_img(image_path, grayscale, target_size)
    return image.img_to_array(pil_image)  # 图片转化为数组


def load_detection_model(model_path):
    # 检测模型,opencv自带的人脸识别模块
    detection_model = cv2.CascadeClassifier(model_path)  # 级联分类器
    return detection_model


def detect_faces(detection_model, gray_image_array):
    # 检测人脸,探测模型,图像灰度数组，指定每个图像比例下图像大小减少的参数，指定每个候选矩形必须保留多少个邻居。
    # 在输入图像中检测不同大小的对象。检测到的对象作为矩形列表返回。
    return detection_model.detectMultiScale(gray_image_array, 1.3, 5)


def apply_offsets(face_coordinates, offsets):
    x, y, width, height = face_coordinates  # 人脸坐标
    x_off, y_off = offsets  # 扩充
    return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)

