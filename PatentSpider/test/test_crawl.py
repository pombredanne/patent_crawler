import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

ua = UserAgent()
headers = {
    "user-agent": ua.random
}
target_url = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=0&f=S&l=50&TERM1=H01L&FIELD1=CPCL&co1=AND&TERM2=&FIELD2=&d=PTXT"


def grab_patent_links(url, headers):
    res = requests.get(url, headers=headers)
    source = res.content
    print(clean_html(source))
    tree = etree.HTML(source)
    a_path = "//td[@valign='top']/a"
    a_nodes = tree.xpath(a_path)
    url = []
    print(a_nodes)
    for a in a_nodes:
        a_url = a.attrib['href']
        if a_url not in url:
            url.append("http://patft.uspto.gov/"+a_url)
    return url


print(grab_patent_links(target_url, headers))
