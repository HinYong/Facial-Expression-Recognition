from keras.callbacks import CSVLogger, ModelCheckpoint, EarlyStopping
from keras.callbacks import ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator

from cnn_model import mini_XCEPTION
from data_process import *

# 参数设置
batch_size = 32  # 批训练个数
num_epochs = 1000  # 训练轮数
input_shape = (48, 48, 1)  # 48*48的灰度图片
validation_split = 0.2
verbose = 1
num_classes = 7  # 类别个数
patience = 50
base_path = './training_models/'  # 根目录


# 用于生成一个batch的图像数据，支持实时数据提升
data_generator = ImageDataGenerator(
    featurewise_center=False,  # 将输入数据的均值设置为0，逐特征进行
    featurewise_std_normalization=False,  # 将输入除以数据标准差，逐特征进行
    rotation_range=10,  # 随机旋转的度数范围
    width_shift_range=0.1,  # 图片宽度的某个比例，数据提升时图片水平偏移的幅度
    height_shift_range=0.1,  # 图片高度的某个比例，数据提升时图片竖直偏移的幅度
    zoom_range=0.1,  # 随机缩放范围
    horizontal_flip=True  # 随机水平翻转
)

model = mini_XCEPTION(input_shape, num_classes)  # 模型定义（输入形状，分类个数）
# 定义优化器adam
# 定义损失函数为categorical_crossentropy多类的对数损失
# 评估指标accuracy
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
# 打印出模型概况，它实际调用的是keras.utils.print_summary
model.summary()

dataset_name = 'fer2013'  # 训练集名称
print('Training data_name:', dataset_name)

# callbacks,回调
# 训练日志文件路径
log_file_path = base_path + dataset_name + '_training.log'
# 把训练轮结果数据流到日志文件的回调函数。append：true文件存在则增加，false覆盖存在的文件
csv_logger = CSVLogger(log_file_path, append=False)
# 当被检测的数量不再提升，则停止训练，val_loss为被监测的数据，patience为没有进步的训练轮数，在这之后训练就会被停止。
early_stop = EarlyStopping(monitor='val_loss', patience=patience)
# 这个回调函数监测val_loss，当val_loss在(patience/4)训练轮之后还没有进步，那么学习速率就会被降低，factor为学习速率降低因数。
# 新的学习速率 = 学习速率 * 因数
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=int(patience / 4), verbose=1)
# 模型文件名字
model_names = base_path + dataset_name + '_emotion_model' + '.{epoch:02d}-{accuracy:.2f}.hdf5'
# 每个训练周期后保存模型，models_names保存路径，val_loss监测数据，verbose详细信息模式，save_best_only最佳模型不覆盖
model_checkpoint = ModelCheckpoint(model_names, 'val_loss', verbose=1, save_best_only=True)
# 回调函数
callbacks = [model_checkpoint, csv_logger, early_stop, reduce_lr]

# 载入数据设置
# data_loader = DataManager(dataset_name, image_size=input_shape[:2])  # DataManager对象定义
faces_data, emotions_labels = load_fer2013()  # 获取数据
faces_data = preprocess_input(faces_data)  # 数据归一化
num_samples, num_classes = emotions_labels.shape
train_data, val_data = split_data(faces_data, emotions_labels, validation_split)  # 获取训练集、验证集
train_faces, train_emotions = train_data  # 人脸以及情绪的训练集
# 训练模型
model.fit_generator(data_generator.flow(train_faces, train_emotions, batch_size),
                    steps_per_epoch=len(train_faces) / batch_size,
                    epochs=num_epochs, verbose=1, callbacks=callbacks,
                    validation_data=val_data)
# 使用fit_generator节省内存
# data_generator.flow采集数据和标签数组，生成批量增强数据。
# steps_per_epoch为在一个epoch完成并开始下一个epoch前从generator产生的总步数（批次样本）。它通常等于数据集的样本数量除以批量大小。
# epochs为训练模型的迭代总轮数。
# verbose: 日志显示模式。0：安静模式, 1：进度条, 2：每轮一行。
# callbacks: 在训练时调用的一系列回调函数。
# validation_data: 用于验证的样本。

