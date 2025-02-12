from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import uvicorn
import json
import datetime
import torch

# 设置设备参数
DEVICE = "cuda"  # 使用CUDA
DEVICE_ID = "0"  # CUDA设备ID，如果未设置则为空
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE  # 组合CUDA设备信息


# 清理GPU内存函数
def torch_gc():
    if torch.cuda.is_available():  # 检查是否可用CUDA
        with torch.cuda.device(CUDA_DEVICE):  # 指定CUDA设备
            torch.cuda.empty_cache()  # 清空CUDA缓存
            torch.cuda.ipc_collect()  # 收集CUDA内存碎片


# 创建FastAPI应用
app = FastAPI()


# 处理POST请求的端点
@app.post("/")
async def create_item(request: Request):
    global model, tokenizer  # 声明全局变量以便在函数内部使用模型和分词器
    try:
        json_post_raw = await request.json()  # 获取POST请求的JSON数据
        json_post = json.dumps(json_post_raw)  # 将JSON数据转换为字符串
        json_post_list = json.loads(json_post)  # 将字符串转换为Python对象
        prompt = json_post_list.get('prompt')  # 获取请求中的提示
        max_length = json_post_list.get('max_length', 512)  # 获取请求中的最大长度，默认512

        # 构建 messages
        messages = json_post_list.get('messages', [{"role": "user", "content": prompt}])
        # 构建输入
        if hasattr(tokenizer, 'apply_chat_template'):
            input_tensor = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")
        else:
            input_tensor = tokenizer.encode(prompt, return_tensors="pt")
        # 通过模型获得输出
        generation_config = {
            "max_new_tokens": max_length,
            "temperature": json_post_list.get('temperature', 0.7),
            "top_p": json_post_list.get('top_p', 0.9),
            "do_sample": True
        }
        outputs = model.generate(input_tensor.to(model.device), **generation_config)
        result = tokenizer.decode(outputs[0][input_tensor.shape[1]:], skip_special_tokens=True)

        now = datetime.datetime.now()  # 获取当前时间
        time = now.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间为字符串
        # 构建响应JSON
        answer = {
            "response": result,
            "status": 200,
            "time": time
        }
        # 构建日志信息
        log = "[" + time + "] " + '", prompt:"' + prompt[:100] + '", response:"' + repr(result)[:100] + '"'
        print(log)  # 打印日志
        torch_gc()  # 执行GPU内存清理
        return answer  # 返回响应
    except Exception as e:
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        answer = {
            "response": f"请求处理失败: {str(e)}",
            "status": 500,
            "time": time
        }
        return answer


# 主函数入口
if __name__ == '__main__':
    mode_name_or_path = ('/home/wyb/hp/pycharm_projects/nlpcda/deepseek/deepseek-ai/deepseek-llm-7b-chat')
    # 加载预训练的分词器和模型
    tokenizer = AutoTokenizer.from_pretrained(mode_name_or_path, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(mode_name_or_path, trust_remote_code=True, torch_dtype=torch.bfloat16,
                                                 device_map="auto")
    model.generation_config = GenerationConfig.from_pretrained(mode_name_or_path)
    model.generation_config.pad_token_id = model.generation_config.eos_token_id
    model.eval()  # 设置模型为评估模式
    # 启动FastAPI应用
    # 用6006端口可以将autodl的端口映射到本地，从而在本地使用api
    uvicorn.run(app, host='0.0.0.0', port=6006, workers=1)  # 在指定端口和主机上启动应用