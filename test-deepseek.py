# import requests
# import json
#
# def get_completion(prompt):
#     headers = {'Content-Type': 'application/json'}
#     data = {"prompt": prompt}
#     response = requests.post(url='http://127.0.0.1:6006', headers=headers, data=json.dumps(data))
#     return response.json()['response']
#
# if __name__ == '__main__':
#     print(get_completion('请为我生成一篇一百字作文，关于亲情的'))
import requests
import json


def get_completion(prompt, api_url='http://127.0.0.1:6006', timeout=100):
    headers = {'Content-Type': 'application/json'}
    data = {
        "prompt": prompt,
        "max_tokens": 200,  # 增加生成文本的长度
        "temperature": 0.7  # 控制生成文本的多样性
    }

    try:
        response = requests.post(url=api_url, headers=headers, data=json.dumps(data), timeout=timeout)
        response.raise_for_status()
        result = response.json()
        print("完整响应:", result)  # 打印完整响应
        return result.get('response', '未找到 response 字段')
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"
    except json.JSONDecodeError as e:
        return f"JSON 解析失败: {e}"


if __name__ == '__main__':
    prompt = '请为我生成一篇作文，关于亲情的。要求内容丰富一千字以上。'
    result = get_completion(prompt)
    print("生成的作文:", result)