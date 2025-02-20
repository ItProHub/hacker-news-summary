import os

class HTMLGenerator:
    def __init__(self, articles):
        self.articles = articles  # 文章数据

    def generate_html(self):
        # 创建HTML页面结构，只有头部和样式
        html_content = """
        <div class="articles">
        """
        
        # 为每篇文章生成HTML结构
        for article in self.articles:
            theme = article.get('theme', 'No Theme')  # 如果没有title则使用默认值
            image = article.get('image', '')  # 如果没有图片则不显示
            summary = article.get('summary', 'No summary available.')  # 使用get方法来避免KeyError
            article_url = article.get('url', '#')  # 获取文章的URL，默认使用#
            author = article.get('by', 'Unknown')  # 作者
            created_at = article.get('time', 'Unknown')  # 创建时间，通常是时间戳，需要格式化
            # 可以将时间戳转为人类可读的时间格式
            from datetime import datetime
            created_time = datetime.utcfromtimestamp(created_at).strftime('%Y-%m-%d %H:%M:%S') if isinstance(created_at, int) else created_at

            article_html = f"""
            <div class="article">
                <img src="{image}" alt="Article Image">
                <div class="article-content">
                    <a href="{article_url}" class="article-title" target="_blank">{theme}</a>
                    <p class="article-description">{summary}</p>
                    <p><strong>Author:</strong> {author}</p>
                    <p><strong>Published at:</strong> {created_time}</p>
                </div>
            </div>
            """
            html_content += article_html

        # 结束articles div部分
        html_content += """
        </div>
        """

        # 检查HTML文件是否存在，如果存在，则读取文件内容并追加新文章
        file_path = 'hacker_news_summary.html'
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                existing_content = file.read()

            # 找到 </body> 标签之前的位置，将新文章内容插入到 <div class="articles"> 里
            insert_position = existing_content.find('</div>')  # 定位到结束 <div class="articles"> 的位置
            new_html = existing_content[:insert_position] + html_content + existing_content[insert_position:]
        else:
            new_html = html_content

        # 将更新后的HTML内容写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_html)

        print("HTML page updated successfully!")
