'''
    reads google news Belgium
    creates html page from the current items.
    Just learning BeautifulSoup
    
    Uses:
    - BeautifulSoup (pip install beautifulsoup)
'''

import requests
import bs4

# Opening google news and getting the page
rss = requests.get("https://news.google.be/news?cf=all&hl=nl&pz=1&ned=nl_be&topic=n&output=rss")
soup = bs4.BeautifulSoup(rss.text,"html.parser")

# Reading the items, adding them to our string
items = soup.find_all('item')
news = ""
for item in items:
    text = item.title.text
    url = item.link.text.split("url=")[-1]
    news += "<a href=" + url + ">" + text + "</a><br>\n"

# Create the html page
html = "<html>\n<head>\n<title>TEST NEWS</title>\n</head>\n<body>\n" + news + "</body>\n</html>"
with open("test.html","w") as f:
    f.write(html)
