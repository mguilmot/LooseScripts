'''
    reads cnet news (tech industry)
    creates html page from the current items.
    Just learning BeautifulSoup
    
    Uses:
    - BeautifulSoup (pip install beautifulsoup)
'''

import requests, bs4

r = requests.get("https://www.cnet.com/topics/tech-industry/2/").text
soup = bs4.BeautifulSoup(r,"html.parser")

html = "<html>\n<head>\n<title>TEST CNET</title>\n<body>"

assets = soup.find_all("div",{"class":"asset"})
for asset in assets:
    # col-3 desc
    try:
        infos = asset.find_all("div",{"class":"col-3 desc "})
        for info in infos:
            url = "<a href='https://www.cnet.com" + info.find_all("a")[0].get("href") + "'>"
            text = info.h4.text.strip() + "</a><br>\n"
            atag = url + text
            html += atag
    except:
        pass
    try:
        infos = asset.find_all("div",{"class":"col-6 assetBody"})
        for info in infos:
            url = "<a href='https://www.cnet.com" + info.find_all("a")[0].get("href") + "'>"
            text = info.h2.text.strip() + "</a><br>\n"
            atag = url + text
            html += atag
    except:
        pass

html += "</body>\n</html>\n"

print(html)

with open("test.html","w") as f:
    f.write(html)
    
