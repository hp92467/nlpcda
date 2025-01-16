from sklearn.manifold import TSNE
import numpy as np
import matplotlib.pyplot as plt

# 加载嵌入文件
loaded_embeddings = np.load("sentence_embeddings.npy")
# print("加载后的嵌入形状:", loaded_embeddings.shape)

# 使用t-SNE降维到2维
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings_tsne = tsne.fit_transform(loaded_embeddings)

# 可视化嵌入
plt.figure(figsize=(10, 8))
plt.scatter(reduced_embeddings_tsne[:, 0], reduced_embeddings_tsne[:, 1], c='green', alpha=0.5)
plt.title("t-SNE 2D Visualization of Sentence Embeddings")
plt.xlabel("t-SNE Component 1")
plt.ylabel("t-SNE Component 2")
plt.show()
