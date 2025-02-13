import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
import logging


class QueryMatchingSystem:
    def __init__(self, index_path='faiss_index.index', texts_path='fault_texts.txt'):
        """
        初始化查询匹配系统
        Args:
            index_path: FAISS索引文件路径
            texts_path: 规则文本文件路径
        """
        # 设置日志
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # 尝试加载模型
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.logger.info("成功加载向量化模型")
        except Exception as e:
            self.logger.error(f"加载向量化模型失败: {str(e)}")
            raise

        # 加载FAISS索引
        try:
            self.index = faiss.read_index(index_path)
            self.logger.info(f"成功加载FAISS索引，包含 {self.index.ntotal} 个向量")
        except Exception as e:
            self.logger.error(f"加载FAISS索引失败: {str(e)}")
            raise

        # 加载规则文本
        try:
            with open(texts_path, 'r', encoding='utf-8') as f:
                self.texts = [line.strip() for line in f.readlines() if line.strip()]
            self.logger.info(f"成功加载规则文本，共 {len(self.texts)} 条")
        except Exception as e:
            self.logger.error(f"加载规则文本失败: {str(e)}")
            raise

    def process_query(self, query_text, top_k=3):
        """
        处理查询文本
        Args:
            query_text: 用户输入的查询文本
            top_k: 返回的最相似规则数量
        Returns:
            combined_prompt: 组合后的prompt
            similar_rules: 找到的相似规则列表
            scores: 相似度分数列表
        """
        try:
            # 1. 将查询文本转换为向量
            query_vector = self.model.encode([query_text])[0]
            query_vector = query_vector.reshape(1, -1).astype(np.float32)

            # 2. 使用FAISS进行相似度搜索
            distances, indices = self.index.search(query_vector, top_k)

            # 3. 获取对应的规则文本
            similar_rules = [self.texts[int(idx)] for idx in indices[0]]

            # 4. 计算相似度分数（将距离转换为相似度分数）
            scores = [1 / (1 + dist) for dist in distances[0]]

            # 5. 生成组合prompt
            combined_prompt = self._generate_prompt(query_text, similar_rules, scores)

            return combined_prompt, similar_rules, scores

        except Exception as e:
            self.logger.error(f"处理查询时出错: {str(e)}")
            raise

    def _generate_prompt(self, query_text, similar_rules, scores):
        """
        生成组合prompt
        Args:
            query_text: 原始查询文本
            similar_rules: 相似规则列表
            scores: 相似度分数列表
        Returns:
            combined_prompt: 组合后的prompt
        """
        prompt_template = """
用户查询：
{query}

相关规则参考：
{rules}

请根据以上信息进行分析并给出建议。
"""
        # 格式化相似规则
        rules_text = ""
        for i, (rule, score) in enumerate(zip(similar_rules, scores), 1):
            rules_text += f"{i}. {rule}\n   (相似度: {score:.4f})\n\n"

        return prompt_template.format(
            query=query_text,
            rules=rules_text
        )


def main():
    # 系统初始化
    try:
        system = QueryMatchingSystem()

        print("查询系统已启动（输入'quit'退出）")

        while True:
            # 获取用户输入
            query = input("\n请输入查询内容: ").strip()

            if query.lower() == 'quit':
                print("退出系统")
                break

            if not query:
                print("请输入有效的查询内容")
                continue

            # 处理查询
            prompt, rules, scores = system.process_query(query)

            # 打印结果
            print("\n生成的Prompt:")
            print("-" * 50)
            print(prompt)
            print("-" * 50)

            # 打印匹配统计
            print("\n匹配统计:")
            for rule, score in zip(rules, scores):
                print(f"相似度: {score:.4f} - {rule[:100]}...")

    except Exception as e:
        print(f"系统运行出错: {str(e)}")


if __name__ == "__main__":
    main()