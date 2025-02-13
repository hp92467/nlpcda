import numpy as np
import faiss
import json
from sentence_transformers import SentenceTransformer
import logging
import requests


class QueryMatchingSystem:
    def __init__(self, index_path='faiss_index.index', texts_path='similar_words_results_20250116_142217.txt'):
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
            self.model = SentenceTransformer('/home/wyb/hp/pycharm_projects/nlpcda/model/all-MiniLM-L6-v2')
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

    def process_query(self, query_text, top_k=5):
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


class ChatBot:
    def __init__(self, api_url='http://127.0.0.1:6006', timeout=100):
        self.api_url = api_url
        self.timeout = timeout
        self.conversation_history = []

    def add_to_history(self, role, content):
        """Add a message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def get_completion(self, user_input):
        """Send request to the model with conversation history"""
        self.add_to_history("user", user_input)

        headers = {'Content-Type': 'application/json'}
        # 简化请求数据结构
        data = {
            "prompt": user_input,  # 直接发送当前输入
            "max_tokens": 200,
            "temperature": 0.7
        }

        try:
            response = requests.post(
                url=self.api_url,
                headers=headers,
                data=json.dumps(data),
                timeout=self.timeout
            )
            response.raise_for_status()

            # 检查响应是否为JSON格式
            try:
                result = response.json()
            except json.JSONDecodeError:
                return f"API返回了非JSON格式的响应: {response.text[:100]}"

            # 检查响应中是否包含预期的字段
            if isinstance(result, dict):
                model_response = result.get('response')
                if model_response:
                    self.add_to_history("assistant", model_response)
                    return model_response
                else:
                    return f"API响应缺少'response'字段。完整响应: {result}"
            else:
                return f"API返回了意外的响应格式: {result}"

        except requests.exceptions.RequestException as e:
            return f"API请求失败: {str(e)}"
        except Exception as e:
            return f"发生未预期的错误: {str(e)}"

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


class IntegratedSystem:
    def __init__(self, index_path='faiss_index.index', texts_path='similar_words_results_20250116_142217.txt',
                 api_url='http://127.0.0.1:6006'):
        """
        初始化集成系统
        Args:
            index_path: FAISS索引文件路径
            texts_path: 规则文本文件路径
            api_url: DeepSeek API地址
        """
        self.query_matcher = QueryMatchingSystem(index_path, texts_path)
        self.chatbot = ChatBot(api_url)

    def process_user_query(self, query_text, top_k=5):
        """
        处理用户查询
        Args:
            query_text: 用户输入的查询文本
            top_k: 返回的最相似规则数量
        Returns:
            response: 回答
        """
        try:
            # 1. 使用QueryMatchingSystem检索相关规则
            prompt, similar_rules, scores = self.query_matcher.process_query(query_text, top_k)

            # 2. 将检索结果作为上下文发送给DeepSeek
            response = self.chatbot.get_completion(prompt)

            return response

        except Exception as e:
            return f"处理查询时出错: {str(e)}"


def main():
    # 初始化集成系统
    system = IntegratedSystem()

    print("集成系统已启动（输入'quit'退出）")

    while True:
        try:
            # 获取用户输入
            query = input("\n请描述特征量的异常情况: ").strip()

            if query.lower() == 'quit':
                print("退出系统")
                break

            if not query:
                print("请输入有效的查询内容")
                continue

            # 处理查询并获取DeepSeek的回答
            response = system.process_user_query(query)

            # 打印结果
            print("\n回答:")
            print("-" * 50)
            print(response)
            print("-" * 50)

        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")


if __name__ == "__main__":
    main()