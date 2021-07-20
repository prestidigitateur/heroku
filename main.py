from flask import Flask
import requests
from bs4 import BeautifulSoup

VERGE_URL = "https://www.theverge.com/rss/index.xml"

class Post:
    def __init__(self, author, title, link, published, content):
        self.author = author
        self.title = title
        self.link = link
        self.published = published
        self.content = content

class VergeNet:
    def __init__(self):
        self.posts: [Post] = []

    def fetch(self):
        # import datetime, time
        # dt = time.time()
        # now = datetime.timedelta
        resp = requests.get(VERGE_URL).text
        soup = BeautifulSoup(resp, "lxml")
        tit = soup.find_all("title")
        link = soup.find_all("link")
        author = soup.find_all("author")
        pub = soup.find_all("published")
        content = soup.find_all("content")
        titles = [item.getText() for item in tit]
        links = [item.get("href") for item in link]
        author = [item.getText() for item in author]
        pub = [item.getText() for item in pub]
        content = [item.getText() for item in content]
        for n in range(len(author)):
            self.posts.append(Post(author[n], titles[n+1], links[n+1], pub[n], content[n]))


n = VergeNet()
n.fetch()
ret_string=""
for post in n.posts:
    ret_string+=f'<div><p>{post.author} {post.published}</p><a href="{post.link}"><h1>{post.title}</h1></a><p>{post.content}</p></div>'

app = Flask(__name__)

@app.route('/')
def hi():
    return(ret_string)

if __name__=="__main__":
    app.run()