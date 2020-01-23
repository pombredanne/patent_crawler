import requests
from fake_useragent import UserAgent
from lxml import etree
from lxml.html.clean import clean_html

# sample patent 
target_url = "http://patft.uspto.gov//netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&p=1&u=%2Fnetahtml%2FPTO%2Fsearch-bool.html&r=50&f=G&l=50&co1=AND&d=PTXT&s1=H01L.CPCL.&OS=CPCL/H01L&RS=CPCL/H01L"

ua = UserAgent()
headers = {
    "user-agent": ua.random
}

def parse_patent_claims(url):
    res = requests.get(url, headers=headers)
    source = clean_html(res.content.decode(res.encoding))
    tree = etree.HTML(source)
    text_path = "//body//br"
    text_nodes = tree.xpath(text_path)
    # grab text from br that contains claims, start from "Claim" and end at "Description"
    claims = []
    start = False
    for br in text_nodes:
        if br.tail == "The invention claimed is: ":
            start = True
        elif br.tail == "RELATED APPLICATIONS\n":
            break
        elif start and br.tail:
            claims.append(br.tail)
    print("The patent claims of this patent are:")
    for i in claims:
        print(i)
    return claims
parse_patent_claims(target_url)
