import numpy as np

# 加载 .npy 文件
data = np.load('sentence_embeddings.npy')

# 查看加载的数据
print("数据形状:", data.shape)  # 输出数组的维度
print("数据类型:", data.dtype)  # 输出数据的类型
print("数据内容（前几个元素）:", data[:5])  # 输出数据的前五个元素
# print("数据内容:", data)# 输出数据的所有元素
