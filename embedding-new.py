import logging
import numpy as np
from sentence_transformers import LoggingHandler, SentenceTransformer

# 打印调试信息到stdout
np.set_printoptions(threshold=100)

logging.basicConfig(
    format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO, handlers=[LoggingHandler()]
)

# 加载预训练的Sentence Transformer模型
model = SentenceTransformer("all-MiniLM-L6-v2")

# 从文件中读取句子
def read_sentences_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences if sentence.strip()]  # 去掉空行

# 加载文件中的句子
file_path = "similar_words_results_20250116_142217.txt"
sentences = read_sentences_from_file(file_path)

# 对句子进行嵌入
sentence_embeddings = model.encode(sentences)

# 输出每个句子的嵌入
for sentence, embedding in zip(sentences, sentence_embeddings):
    print("句子:", sentence)
    print("嵌入:", embedding)
    print("")

# 保存嵌入到.np 文件
np.save("sentence_embeddings.npy", sentence_embeddings)

# 从.np 文件中加载嵌入
loaded_embeddings = np.load("sentence_embeddings.npy")

print("加载后的嵌入形状:", loaded_embeddings.shape)
print("第一个嵌入:", loaded_embeddings[0])  # 查看第一个嵌入
