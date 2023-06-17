import subprocess
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pydantic import BaseModel

count=0
county=0
visited_url=set()
created_files=set()
domain=""

class ScrapeURL(BaseModel):
    url:str
    scraped_data:str


# class ScrapeWebsite(BaseModel):
#     base_url:str
#     scraped_website:List[ScrapeURL]

class URLRequest(BaseModel):
    url:str



count=0
county=0
visited_url=set()
created_files=set()
domain=""
visited_url_list_copy={}

def scrape_content(visited_url_list,url):
    if url.startswith("https"):
        url_scheme="https://"
    else:
        url_scheme="http://"
    host=urlparse(url).netloc

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    #Getting the page source of the webpage
    text = soup.get_text()
    #getting the text of the pagesource
    visited_url_list.append(ScrapeURL(url=url,scraped_data=text))
    visited_url_list_copy[url]=text
    visited_url.add(url)
    links=get_links(soup,url)
    for link in links:
        href = link.get('href')
        try:
            if href.startswith("http") or href.startswith("/"):
                if href.startswith("/"):

                    href=url_scheme+host+href
                    print("href after adding host:",href)
                #if the url is related to our website,netloc function will return an empty string
                if urlparse(href).netloc==host:
                    global count
                    if count<=1:
                    # print("before",visited_url_list)
                    # visited_url_list=scrape_content(visited_url_list,href)
                        print("h1")
                        if href not in visited_url:
                            t=getting_data_using_lynx(href)
                            print("h3")
                            visited_url_list.append(ScrapeURL(url=href,scraped_data=t))
                                                    # print("before",visited_url_list)
                            visited_url.add(href)
                            visited_url_list_copy[url]=text
                            print("h4")
                            count+=1
                        else:
                            print("h2")
                    else:
                        break

                else:
                    print(href)
                    print("host is",urlparse(href).netloc)
        except Exception as e:
                print(e)
    print(visited_url_list)
    return visited_url_list







def get_links(soup,url):
    links=soup.find_all('a')
    return links



def getting_data_using_lynx(url):
     # Use Lynx to fetch the text contents of the URL
    print("ok")
    cmd = f"lynx -dump {url}"
    print("ok1")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    print("ok2")
    (out, err) = proc.communicate()
    # Decode the output bytes to a UTF-8 string
    print("ok3")
    text = out.decode("utf-8")
    # Remove any HTML tags from the text
    print("ok4")
    text = "".join([c if c.isalnum() or c.isspace() else " " for c in text])
    # filename=url.replace("http://",'').replace('/','_').lstrip('_')
    # current_path=os.getcwd()
    # Creating a file in current working directory for storing the scraped data.
    # file_path=os.path.join(current_path,filename+'.txt')
    # with open(file_path,'w+') as f:
    #     f.write(text)
    return text


scrape_content([],"http://quotes.toscrape.com"))