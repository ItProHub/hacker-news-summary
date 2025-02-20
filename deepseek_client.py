# deepseek_client.py
import os
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
  base_url="https://api.deepseek.com",
)

def analyze_article_with_deepseek(article_content):    
    """
    使用 DeepSeek API 分析文章内容，判断主题是否与 IT 或软件开发相关，并生成概要。
    :param article_content: 文章的完整内容
    :return: 主题和概要，如果主题与 IT 或软件开发相关；否则返回 None, None
    """
    try:
        article_content = article_content.replace('```', ' ') # prompt注入
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个专业的文章分类和摘要生成助手。请帮我分析如下文章，如果文章内容是关于IT或软件开发的，那么请告诉我文章的主题和概要，生成的概要控制在50个字左右。返回格式为：主题: xxx 概要: xxx。如果文章内容不是关于IT或软件开发的，那么请直接返回空。"},
                {"role": "user", "content": article_content}
            ],
            max_tokens=1000,
            temperature=0.5,
            stream=False
        )
        # 解析 DeepSeek 的响应
        result = response.choices[0].message.content
        # 假设 DeepSeek 返回的结果包含主题和概要
        if '主题' in result and '概要' in result:
            theme = result.split('主题:')[1].split('概要:')[0].strip()
            summary = result.split('概要:')[1].strip()
            return theme, summary
        else:
            return None, None
    except Exception as e:
        print(f"调用 DeepSeek API 时出错: {e}")
        return None, None
