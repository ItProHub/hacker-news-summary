# image_downloader.py
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import base64
import re



# 获取文章中图片的URL（首先尝试从网页中提取图片）
def extract_image_url(article):
    article_url = article.get('url')
    if article_url:
        return extract_image_url_from_webpage(article_url)
    return None

# 从文章的URL获取页面中的图片
def extract_image_url_from_webpage(article_url):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找页面中的图片标签
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if img_url:
                # 处理相对路径，转换为完整的URL
                if img_url.startswith('http') or img_url.startswith('https'):
                    return img_url
                else:
                    # 将相对路径转换为完整的URL
                    absolute_url = urljoin(article_url, img_url)
                    return absolute_url
    except Exception as e:
        print(f"Error extracting image from {article_url}: {e}")
    return None

# 下载图片并保存到本地，返回保存路径
def download_image(image_url, save_path):
    try:
        # 确保保存目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # 如果是Base64编码的图片（data:image/*）
        if image_url.startswith('data:image'):
            # 提取Base64数据（去掉开头的 'data:image/svg+xml;base64,' 部分）
            base64_data = image_url.split(',')[1]
            
            # 解码Base64内容
            img_data = base64.b64decode(base64_data)
            
            # 写入文件（对于SVG等文本类型的图片，使用'w'模式，否则用'wb'模式）
            with open(save_path, 'wb') as file:
                file.write(img_data)
            print(f"Downloaded image to {save_path} (Base64)")
            return save_path
        
        # 检查URL是否是有效的图片URL（以.jpg, .jpeg, .png, .svg结尾）
        if not re.match(r'.*\.(jpg|jpeg|png|svg|webp|gif|avif)$', image_url, re.IGNORECASE):
            print(f"Skipping invalid image URL: {image_url}")
            return None

        # 下载普通的外部图片URL
        img_data = requests.get(image_url).content
        with open(save_path, 'wb') as file:
            file.write(img_data)
        print(f"Downloaded image to {save_path}")
        return save_path  # 返回图片的保存路径

    except Exception as e:
        print(f"Error downloading image from {image_url}: {e}")
    return None

# 清理文件名，去除非法字符
def clean_filename(url):
    # 清理URL中的特殊字符，使其成为合法的文件名
    filename = re.sub(r'[^\w\-_\. ]', '_', url)
    return filename

# 处理图片URL并下载
def process_image_url(article, image_url):
    # 清理图片URL，生成合法的文件名
    image_filename = clean_filename(image_url)
    image_save_path = f'data/img/{image_filename}'

    # 下载图片并保存到本地
    saved_image_path = download_image(image_url, image_save_path)
    if saved_image_path:
        article['image'] = saved_image_path
    else:
        article['image'] = "/static/default.avif"
