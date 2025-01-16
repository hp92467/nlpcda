import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import numpy as np

# 加载嵌入文件
loaded_embeddings = np.load("sentence_embeddings.npy")
# print("加载后的嵌入形状:", loaded_embeddings.shape)

# 使用PCA降维到2维
pca = PCA(n_components=2)
reduced_embeddings = pca.fit_transform(loaded_embeddings)

# 可视化嵌入
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], c='blue', alpha=0.5)
plt.title("PCA 2D Visualization of Sentence Embeddings")
plt.xlabel("PCA Component 1")
plt.ylabel("PCA Component 2")
plt.show()
