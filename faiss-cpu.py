import numpy as np
import faiss

# 步骤 1: 加载嵌入向量数据
def load_embeddings(file_path):
    """加载 .npy 格式的嵌入向量文件"""
    embeddings = np.load(file_path)
    return embeddings

# 步骤 2: 创建 FAISS 索引
def create_faiss_index(embeddings):
    """根据嵌入向量创建 FAISS 索引"""
    # 获取向量的维度
    dimension = embeddings.shape[1]

    # 创建一个 L2 距离的索引
    index = faiss.IndexFlatL2(dimension)
    return index

# 步骤 3: 将向量添加到索引中
def add_vectors_to_index(index, embeddings):
    """将嵌入向量添加到 FAISS 索引中"""
    index.add(embeddings)
    print(f"成功添加 {embeddings.shape[0]} 个向量到索引中")

# 步骤 4: 相似度查询
def search_similar_vectors(index, query_vector, k=5):
    """使用 FAISS 查询与给定查询向量最相似的 k 个向量"""
    distances, indices = index.search(query_vector, k)
    return distances, indices

# 步骤 5: 保存和加载 FAISS 索引
def save_faiss_index(index, file_path):
    """将 FAISS 索引保存到磁盘"""
    faiss.write_index(index, file_path)
    print(f"FAISS 索引已保存到 {file_path}")

def load_faiss_index(file_path):
    """从磁盘加载 FAISS 索引"""
    index = faiss.read_index(file_path)
    print(f"FAISS 索引已从 {file_path} 加载")
    return index

# 示例用法
if __name__ == "__main__":
    # 1. 加载嵌入向量
    embeddings_file = 'sentence_embeddings.npy'  # 假设嵌入向量文件为 .npy 格式
    embeddings = load_embeddings(embeddings_file)

    # 2. 创建 FAISS 索引
    index = create_faiss_index(embeddings)

    # 3. 添加嵌入向量到 FAISS 索引
    add_vectors_to_index(index, embeddings)

    # 4. 查询最相似的 k 个向量
    query_vector = np.array([embeddings[12]])  # 假设用第一个向量作为查询向量
    k = 5  # 返回 5 个最相似的结果
    distances, indices = search_similar_vectors(index, query_vector, k)
    print("查询结果:")
    print("Distances:", distances)
    print("Indices:", indices)

    # 5. 保存索引
    faiss_index_file = 'faiss_index.index'
    save_faiss_index(index, faiss_index_file)

    # 6. 加载已保存的索引
    loaded_index = load_faiss_index(faiss_index_file)
