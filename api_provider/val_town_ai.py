import requests
import base64
import json

# 定义一个类来封装 Cloudflare 函数的返回结果
class ValTownResult:
    """
    封装 val.twon API 响应结果的类。

    属性说明:
    response: API 返回的结果（主要）
    timestamp: API 返回的时间戳
    """
    def __init__(self, result):
        self.result = result
        self.response = result.get('response', '')
        self.timestamp = result.get('timestamp', None)

    def __repr__(self):
        return (f"ValTownResult("
                f"response='{self.response}', "
                f"timestamp='{self.timestamp}')")

def chatgpt_4o_mini(ValTown_Url, prompt, binary_data=None):
    """
    调用 Val.town 的 ChatGPT 4.0 Mini 模型进行对话
    
    参数:
    - ValTown_Url: valtown API 的 URL（详见 readme.md 中 2.1节）
    - prompt: 提供给模型的提示词
    - binary_data: 输入的二进制图像数据   
    
    """
    payload = {
        "prompt": prompt
    }

    if binary_data:
        encoded_image = base64.b64encode(binary_data).decode('utf-8')
        payload["image"] = f"data:image/png;base64,{encoded_image}"

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(ValTown_Url, json=payload, headers=headers)

    if response.status_code == 200:
        return ValTownResult(response.json())
    else:
        return ValTownResult(None, response.text)


# 示例用法
if __name__ == "__main__":
    
    # 读取配置文件
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    # 从配置文件中提取 ValTown_Url
    ValTown_Url = config['ValTown_Url']  

    prompt = "提供此图像的生动而详细的描述。从图像中描述的主要主题或场景的简明概述开始。然后，深入研究细节，详细描述配色方案、照明、形状和表达式等元素。最后，提供图像的摘要和分析，反映其整体影响和含义。用中文回答。"
    image_path = "/Users/macm4/Desktop/Snipaste_2024-11-22_17-25-35.png"  # 替换为你的图片路径

    # 打开图像文件并读取为二进制字符串
    with open(image_path, "rb") as image_file:
        binary_data = image_file.read()

    result = chatgpt_4o_mini(ValTown_Url, prompt, binary_data)
    print(result.response)

