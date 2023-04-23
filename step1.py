from env import SECRET_KEY
import openai, feedparser, os
import urllib.parse

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
    
    # return "Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo Boogalo booglaoo "
    """
    Generates a chat response from OpenAI given a prompt and returns the response.
    """
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

footer = open("footer.html","r")
footer_html = footer.read()

index = open("articles/index.html","w")
index_header = open("index_header.html","r")

index.write(index_header.read())
# Example usage
articles = get_ndtv_articles()
file_index = 1
for article in articles:
    print (f"Now caching {article['title']}")
    filename = str(file_index) + ".html"
    article_text = generate_chat_response(f"summarise article '{article['link']}' for a 10 year old ")
    file = open(os.path.join("articles", filename),"w")
    file.write(header_html)
    file.write(f"<h3>{article['title']}</h3><p>")
    file.write(article_text.replace("\n","<br/>"))
    file.write(f"</p><a href='{article['link']}' target='_blank'> Link to original article</a> ")
    file.write(footer_html)
    file.close()
    index.write(f"<a href='{filename}'>{article['title']} </a> ")
    file_index = file_index + 1
    
index.close()