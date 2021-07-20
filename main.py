from flask import Flask
import requests
from bs4 import BeautifulSoup

VERGE_URL = "https://www.theverge.com/rss/index.xml"

class Post:
    def __init__(self, author, title, link, published):
        self.author = author
        self.title = title
        self.link = link
        self.published = published

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
        titles = [item.getText() for item in tit]
        links = [item.get("href") for item in link]
        author = [item.getText() for item in author]
        pub = [item.getText() for item in pub]
        for n in range(len(author)):
            self.posts.append(Post(author[n], titles[n+1], links[n+1], pub[n]))


n = VergeNet()
n.fetch()
ret_string=""
for post in n.posts:
    ret_string+=f'<div><p>{post.author}</p><p>{post.published}</p><h1>{post.title}</h1><a href="{post.link}">Link</a></div>'

app = Flask(__name__)

@app.route('/')
def hi():
    return(ret_string)

if __name__=="__main__":
    app.run()