import numpy as np
import csv


# 加载 .npy 文件
def npy_to_csv(npy_file, csv_file):
    # 加载 .npy 数据
    data = np.load(npy_file)

    # 保存为 CSV 文件
    np.savetxt(csv_file, data, delimiter=',', fmt='%s')  # fmt='%s' 适用于文本数据，如果是数值数据可以调整格式
    print(f"已成功将 {npy_file} 转换为 {csv_file}")


# 示例用法
if __name__ == "__main__":
    npy_file = 'sentence_embeddings.npy'  # 替换为你的 .npy 文件路径
    csv_file = 'sentence_embeddings.csv'  # 输出的 CSV 文件路径

    npy_to_csv(npy_file, csv_file)
