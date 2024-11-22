import json
import api_provider.cloudflare_ai as cloudflare_ai
import api_provider.uim_ocr as uim_ocr
import api_provider.val_town_ai as val_town_ai

# 读取配置文件
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# 从 ./config.json 配置文件中提取 ACCOUNT_ID 和 AUTH_TOKEN
CF_ACCOUNT_ID = config['CF_ACCOUNT_ID']
CF_AUTH_TOKEN = config['CF_AUTH_TOKEN']
ValTown_Url = config['ValTown_Url']

# 示例调用
if __name__ == "__main__":

    # 打开图像文件并读取为二进制字符串
    image_path = '/Users/macm4/Desktop/截屏2024-11-21 20.56.01.png'

    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()

    # 调用 OCR API
    ocrstr = uim_ocr.ocr_request('127.0.0.1:1224', binary_data)

    # prompt = "Given the OCR result of the image:【" + ocrstr + "】, This is a screenshot. According to the OCR results, generate keywords (including but not limited to website address, topic, user ID, webpage title, technical terms, etc.), with an output format of, keyword: explanation. One line, one."
    
    prompt = "这是一张屏幕截图的OCR识别结果：【" + ocrstr + "】,我需要构建这张图片的索引，请根据OCR，提取出任何可能有用的词汇，短语，名词，链接，项目，代码，用户名等等不要做解释。"
    # print(prompt)

    # 描述图片提示词
    # prompt = "Provide a vivid and detailed description of this image. Start with a concise overview of the main subject or scene depicted in the image. Then, delve into the specifics, describing elements such as color schemes, lighting, shapes, and expressions in detail. Finally, offer a summary and analysis of the image, reflecting on its overall impact and meaning. 中文输出。"
    # 详细提示词
    # prompt = "Please provide a vivid and detailed description of this image. Begin with a concise overview of the main subject or scene depicted. Then, delve into the specifics:1. Color Schemes: Describe the dominant colors and how they interact.2. Lighting: Explain the sources of light and how they affect the mood and atmosphere.3. Shapes and Composition: Detail the arrangement of objects and how they contribute to the overall composition.4. Expressions and Emotions: If there are people or animals, describe their facial expressions and body language.5. Textures and Materials: Mention any notable textures or materials visible in the image.6. Background and Context: Describe the background and any contextual elements that add depth to the scene.Finally, offer a summary and analysis of the image, reflecting on its overall impact and meaning. Consider the emotional response it evokes and any symbolic or thematic elements."
    # 调用 cloudflare API 
    # result = cloudflare_ai.llama_3_2_11b_vision(CF_ACCOUNT_ID, CF_AUTH_TOKEN, prompt, binary_data)
    # output = cloudflare_ai.qwen_1_5_14b_chat_awq(CF_ACCOUNT_ID, CF_AUTH_TOKEN,"帮我翻译成中文：" + result.response)
    result = val_town_ai.chatgpt_4o_mini(ValTown_Url, prompt, binary_data)
    # print(result.response + "\n中文翻译：\n" + output.response)
    print(result.response)