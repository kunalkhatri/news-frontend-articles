from env import SECRET_KEY
import openai, feedparser, os
import urllib.parse
from datetime import datetime
openai.api_key = SECRET_KEY

def get_ndtv_articles():
    """
    Returns a list of dictionaries representing articles from the NDTV top stories RSS feed.
    Each dictionary contains 'title' and 'link' keys.
    """
    url = "https://feeds.feedburner.com/ndtvnews-top-stories"
    feed = feedparser.parse(url)

    articles = []
    for entry in feed.entries:
        article = {}
        article['title'] = entry.title
        article['link'] = entry.link
        articles.append(article)

    return articles
def generate_chat_response(prompt):
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"rephrase following article for college level reading levels in 200 words '{prompt}'",
        temperature=1,
        max_tokens=1002,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

header = open("header.html","r")
header_html = header.read()

current_datetime = datetime.now().strftime("%a %d %b %y %H:%M")

footer = open("footer.html","r")
footer_html = footer.read()
index_text = []

# Example usage
articles = get_ndtv_articles()
articles_content = []
file_index = 1
for article in articles:
    print (f"Now caching {article['title']}")
    filename = str(file_index) + ".html"
    article_text = generate_chat_response(f"summarise article '{article['link']}' in upto 500 words ")
    articles_content.append([filename,article['title'],article_text,article['link']])
    index_text.append(f"<a href='{filename}'>{article['title']} </a> ")
    file_index = file_index + 1

index = open("articles/index.html","w")
index_header = open("index_header.html","r")
index.write(index_header.read())
index.write(f"<h3>News articles summarised on {current_datetime}</h3>")
for line in index_text:
    index.write(line)
index.close()

file_index = 1
for content in articles_content:
    file = open(os.path.join("articles", content[0]),"w")
    file.write(header_html)
    file.write(f"<h3>{content[1]}</h3><p>")
    file.write(content[2].replace("\n","<br/>"))
    file.write(f"</p><a href='{content[3]}' target='_blank'> Link to original article</a> ")
    file.write(f"<p> Article summarised on {current_datetime} </p> ")
    file.write(footer_html)
    file.close()
    file_index = file_index + 1