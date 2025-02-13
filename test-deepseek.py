#
# import requests
# import json
#
#
# def get_completion(prompt, api_url='http://127.0.0.1:6006', timeout=100):
#     headers = {'Content-Type': 'application/json'}
#     data = {
#         "prompt": prompt,
#         "max_tokens": 200,  # 增加生成文本的长度
#         "temperature": 0.7  # 控制生成文本的多样性
#     }
#
#     try:
#         response = requests.post(url=api_url, headers=headers, data=json.dumps(data), timeout=timeout)
#         response.raise_for_status()
#         result = response.json()
#         # print("完整响应:", result)  # 打印完整响应
#         return result.get('response', '未找到 response 字段')
#     except requests.exceptions.RequestException as e:
#         return f"请求失败: {e}"
#     except json.JSONDecodeError as e:
#         return f"JSON 解析失败: {e}"
#
#
# if __name__ == '__main__':
#     prompt = '中国核动力研究设计院简介'
#     result = get_completion(prompt)
#     print("回答:", result)
import requests
import json


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


def main():
    chatbot = ChatBot()
    print("开始对话 (输入 'quit' 结束对话, 输入 'clear' 清除对话历史):")

    while True:
        try:
            user_input = input("\n用户: ").strip()

            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'clear':
                chatbot.clear_history()
                print("对话历史已清除")
                continue
            elif not user_input:
                print("请输入内容")
                continue

            response = chatbot.get_completion(user_input)
            print("\n助手:", response)

        except KeyboardInterrupt:
            print("\n程序已终止")
            break
        except Exception as e:
            print(f"\n发生错误: {str(e)}")


if __name__ == '__main__':
    main()
