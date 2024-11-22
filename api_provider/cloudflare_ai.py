import numpy as np
import requests
import json

# 定义一个类来封装 Cloudflare 函数的返回结果
class CfResult:
    """
    封装 Cloudflare API 响应结果的类。

    属性说明:
    result: 完整的 API 响应对象
    success: API 调用是否成功
    errors: 错误列表
    messages: 消息列表
    response: API 返回的结果（主要）
    """
    def __init__(self, result):
        self.result = result
        self.success = result.get('success', False)
        self.errors = result.get('errors', [])
        self.messages = result.get('messages', [])
        self.response = result.get('result', {}).get('response', '')

    def __repr__(self):
        return f"CfResult(success={self.success}, errors={self.errors}, messages={self.messages}, response='{self.response}')"

def llama_3_2_11b_vision(ACCOUNT_ID, AUTH_TOKEN, prompt, binary_data):
    """
    调用 Cloudflare 的 Llama 3.2 11B Vision API 来处理图像识别任务。

    参数:
    - ACCOUNT_ID: Cloudflare 账户 ID
    - AUTH_TOKEN: API 授权令牌
    - prompt: 提供给模型的提示词
    - binary_data: 输入的二进制图像数据

    返回:
    - CfResult对象: 包含 API 响应结果的对象
    """
    # 将二进制数据转换为 Uint8Array
    uint8_array = np.frombuffer(binary_data, dtype=np.uint8)

    # 将 NumPy 数组转换为列表
    uint8_list = uint8_array.tolist()

    # 发送请求
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3.2-11b-vision-instruct",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
            "prompt": prompt,
            "image": uint8_list
        }
    )

    # 解析响应并返回 CfResult 对象
    result = CfResult(response.json())
    return result

def llama_3_1_70b(ACCOUNT_ID, AUTH_TOKEN, prompt):
    """
    调用 Cloudflare 的 Llama 3.1 70B  API 来进行对话。

    参数:
    - ACCOUNT_ID: Cloudflare 账户 ID
    - AUTH_TOKEN: API 授权令牌
    - prompt: 提供给模型的提示词

    返回:
    - CfResult对象: 包含 API 响应结果的对象
    """
    # 发送请求
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/meta/llama-3.1-70b-instruct",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
            "prompt": prompt
        }
    )

    # 解析响应并返回 CfResult 对象
    result = CfResult(response.json())
    return result

def qwen_1_5_14b_chat_awq(ACCOUNT_ID, AUTH_TOKEN, prompt):
    """
    调用 Cloudflare 的 qwen1.5-14b-chat-awq AI模型进行对话。

    参数:
    - ACCOUNT_ID: Cloudflare 账户 ID
    - AUTH_TOKEN: API 授权令牌
    - prompt: 提供给模型的提示词

    返回:
    - CfResult对象: 包含AI模型生成的响应信息。
    """
    # 发送请求
    response = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/qwen/qwen1.5-14b-chat-awq",
        headers={"Authorization": f"Bearer {AUTH_TOKEN}"},
        json={
            "prompt": prompt
        }
    )
    # 解析响应并返回 CfResult 对象
    result = CfResult(response.json())
    return result






# 示例用法
if __name__ == "__main__":
    # 读取配置文件
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # 从配置文件中提取 ACCOUNT_ID 和 AUTH_TOKEN
    CF_ACCOUNT_ID = config['CF_ACCOUNT_ID']
    CF_AUTH_TOKEN = config['CF_AUTH_TOKEN']
    
    # 提示词
    prompt = "Provide a vivid and detailed description of this image. Start with a concise overview of the main subject or scene depicted in the image. Then, delve into the specifics, describing elements such as color schemes, lighting, shapes, and expressions in detail. Finally, offer a summary and analysis of the image, reflecting on its overall impact and meaning."
    image_path = "/Users/macm4/Desktop/Snipaste_2024-11-22_17-25-35.png"  # 替换为你的图片路径

    # 打开图像文件并读取为二进制字符串
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()

    result = llama_3_2_11b_vision(CF_ACCOUNT_ID, CF_AUTH_TOKEN, prompt, binary_data)
    print(result.response)
