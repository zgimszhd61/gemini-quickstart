import os
import google.generativeai as genai
from PyPDF2 import PdfReader
import requests

# 使用API密钥进行身份验证
genai.configure(api_key="")

def askGemini(content):
    question = "将以下内容简化并使之易于中国人理解：{}".format(content)
    # 使用gemini-pro模型
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    print(response.text)

def main(url):
    response = requests.get(url)
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    pdf_path = 'temp.pdf'
    reader = PdfReader(pdf_path)
    texts = []
    number_of_pages = len(reader.pages)
    print(f'页数: {number_of_pages}')
    for page in reader.pages:
        text = page.extract_text()
        if text:  # 确保只添加有文本的页面
            texts.append(text)
    os.remove(pdf_path)  # 处理完后删除临时文件
    full_text = ' '.join(texts).replace('\n', ' ')  # 移除不必要的换行，并合并文本
    print(full_text[:1000])  # 打印前1000个字符以检查
    askGemini(full_text)

# 调用主函数，输入PDF URL
main("https://arxiv.org/pdf/2405.00578.pdf")
