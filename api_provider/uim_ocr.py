import base64
import json
import requests

def ocr_request(api_server, image_binary):
    """
    发送OCR请求到指定的API服务器，并返回识别结果。

    参数:
        api_server (str): API服务器的IP地址和端口号，例如 '127.0.0.1:1224'。
        image_binary (bytes): 图片的二进制数据。

    返回:
        str: OCR识别的结果，每个识别出的文字项占一行。
    """

    # 将图片的二进制数据转换为Base64字符串
    base64_data = base64.b64encode(image_binary).decode('utf-8')

    # 构建请求体
    ocr_req = {
        'base64': base64_data,
        'options': {
            'data.format': 'dict'
        }
    }

    # 发送POST请求到API服务器
    url = f"http://{api_server}/api/ocr"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(ocr_req))

    # print(response)
    res_data = json.loads(response.text)
    # print(res_data)
    # 解析响应
    if  res_data['code'] == 100:
        # 处理返回的数据，去重并拼接成字符串
        seen = set()
        result = ""
        for item in res_data['data']:
            if item['text'] not in seen:
                result += item['text'] + '\n'
                seen.add(item['text'])
        return result.strip()  # 去除末尾多余的换行符
    else:
        raise Exception(f"HTTP Error: {response.status_code}")
    
if __name__ == "__main__":

    image_path = '/Users/macm4/Desktop/截屏2024-11-21 20.58.41.png'

    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()

    ocrstr = ocr_request('127.0.0.1:1224', binary_data)

    print(ocrstr)