import requests
import json
import os
import uuid
from datetime import datetime
from deepseek_client import analyze_article_with_deepseek
from image_downloader import extract_image_url, process_image_url  # 导入图片下载模块

# 获取Hacker News上的文章ID，支持分页
def get_hacker_news_article_ids(limit=30):
    url = f'https://hacker-news.firebaseio.com/v0/newstories.json?print=pretty'
    response = requests.get(url)
    all_article_ids = response.json()  # 所有文章ID
    return all_article_ids[:limit]

# 获取每篇文章的详细内容
def get_article_details(article_id):
    url = f'https://hacker-news.firebaseio.com/v0/item/{article_id}.json?print=pretty'
    response = requests.get(url)
    return response.json()

# 确保目录存在
def ensure_articles_directory():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/img'):
        os.makedirs('data/img')

# 生成唯一的文件名（使用UUID）
def generate_unique_filename(extension):
    return f"{uuid.uuid4().hex}{extension}"

# 保存文章到以日期命名的文件
def save_articles(articles):
    # 确保articles目录存在
    ensure_articles_directory()

    # 保存更新后的文章内容
    file_path = f'data/articles.json'
    with open(file_path, 'w') as f:
        json.dump(articles, f, indent=4)

# 读取并加载现有的文章
def load_existing_articles(file_path='articles/articles.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return []        

def process_new_articles(limit=20):
    # 加载之前保存的文章
    existing_articles = load_existing_articles()

    # 获取现有的文章URL集合
    existing_urls = {article['url'] for article in existing_articles}

    # 每次获取一定数量的最新文章ID
    new_article_ids = get_hacker_news_article_ids(limit=limit)

    # 获取新文章的详细内容
    new_articles = []
    for article_id in new_article_ids:
        article = get_article_details(article_id)

        # 如果该文章已经存在，则跳过 DeepSeek 调用
        if article['url'] in existing_urls:
            print(f"Article {article['url']} already processed, skipping DeepSeek analysis.")
            # 查找该文章并复制已生成的主题和总结
            existing_article = next(a for a in existing_articles if a['url'] == article['url'])
            article = existing_article
        else:            
            # 获取文章的图片并下载
            image_url = extract_image_url(article)
            if image_url:
                # 使用image_downloader模块下载图片
                process_image_url(article, image_url)

            # 获取文章的主题和概要
            theme, summary = analyze_article_with_deepseek(article['title'])
            article['theme'] = theme
            article['summary'] = summary

        new_articles.append(article)

    # 在这里可以处理新的文章，例如保存文章内容，生成HTML等
    print(f"Found {len(new_articles)} new articles.")
    return new_articles

def main():
    limit = 5  # 每次获取30篇文章
   
    new_articles = process_new_articles(limit=limit)

    if new_articles:
        save_articles(new_articles)
        print(f"Saved {len(new_articles)} new articles for {datetime.now().strftime('%Y-%m-%d')}")

if __name__ == "__main__":
    main()
