"""
This basic example loads a pre-trained model from the web and uses it to
generate sentence embeddings for a given list of sentences.
"""

import logging

import numpy as np

from sentence_transformers import LoggingHandler, SentenceTransformer
import numpy as np

#### Just some code to print debug information to stdout
np.set_printoptions(threshold=100)

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, handlers=[LoggingHandler()]
)
#### /print debug information to stdout


# Load pre-trained Sentence Transformer Model. It will be downloaded automatically
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed a list of sentences
sentences = [
    "离心泵出口压力频繁波动（±0.5 MPa），振动信号加速度级 > 6 g，基频和二倍频幅值显著。",
    "泵轴不对中（角向不对中）。",
    "检查联轴器的对中，重新调整精度，控制径向误差在公差范围内。",
]
sentence_embeddings = model.encode(sentences)

# The result is a list of sentence embeddings as numpy arrays
for sentence, embedding in zip(sentences, sentence_embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")

# 保存嵌入到文件（.npy 格式）
np.save("sentence_embeddings.npy", sentence_embeddings)

# 加载嵌入文件
loaded_embeddings = np.load("sentence_embeddings.npy")

print("Loaded Embeddings Shape:", loaded_embeddings.shape)
print("First Embedding:", loaded_embeddings[0])  # 查看第一个嵌入