# -*- coding: utf-8 -*-
"""
Image Site Downloader

author: p1xckha ( https://github.com/p1xckha )
"""

import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import ssl
import os
import re
import random
from urllib.parse import urljoin

# https://www.useragents.me/
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    ]


class Downloader():
    def __init__(self):
        self._user_agent = random.choice(user_agents)
    
    @property
    def user_agent(self):
        return self._user_agent
    
    @user_agent.setter
    def user_agent(self, user_agent):
        self._user_agent = user_agent
    
    def get_html(self, url):
        try:
            headers = {'User-Agent': self.user_agent}
            req = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(req).read()
            self.currentPage = url
            return html
        except Exception as err:
            print("*** Error: can not read the page ***\n%s\n%s" % (url, err))
            return None
    
    def make_save_dir(self, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def download(self, url, save_dir='.', save_filename=None):
        save_dir = os.path.abspath(save_dir)
        self.make_save_dir(save_dir)
            
        if save_filename == None:
            save_filename = os.path.basename(url) # filename=a.jpg, if url='http://a.com/a.jpg'
        
        
        try:
            data = urllib.request.urlopen(url).read()
            save_path = os.path.join(save_dir, save_filename) # file: a/b.jpg, 01/02.png, etc.
            with open(save_path, mode="wb") as f:
                f.write(data)
            print('downloaded: ', save_path)
        except urllib.error.URLError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
            
    def download_all(self, urls, save_dir='.'):
        for url in urls:
            self.download(url, save_dir)


class MySoup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")
        self.currentPage = ""
        self.urls = None
        
    def get_all_urls(self, baseUrl, extensions=None):
        urls = []
        tags = self('a')
        for tag in tags:
            # make url valid
            url = tag.get('href', None)
            if url is None:
                continue
            elif url.startswith("javascript:"):
                continue
            else:
                url = urljoin(baseUrl, url)
            
            # add url if extension is not specified
            if extensions is None:
                urls.append(url)
                continue
            
            # add url if url ends with either of extensions
            if type(extensions) == type([]):
                for extension in extensions:
                    if url.endswith("." + extension):
                        urls.append(url)
                        break
            elif type(extensions) == type(""):
                if url.endswith("." + extensions):
                    urls.append(url)
        self.urls = urls
        return urls
    
    def get_all_imgs(self):
        urls = []
        tags = self('img')
        for tag in tags:
            pass
    

    
if __name__ == "__main__":
    downloader = Downloader()
    url = 'https://www.reddit.com/'
    
    # get html
    html = downloader.get_html(url)
    soup = MySoup(html)
    
    # get all internal links
    baseUrl = re.search('https?://[^/]+', url)[0]
    all_urls = soup.get_all_urls(baseUrl)
    urls = []
    for url in all_urls:
        if baseUrl in url:
            urls.append(url)
    
    # visit all internal links and save all images linked from 
    save_dir = "test1"
    for url in  urls:
        html = downloader.get_html(url)
        if html is None:
            continue
        baseUrl = re.search('https?://[^/]+', url)[0]
        soup = MySoup(html)
        all_urls = soup.get_all_urls(baseUrl,  ["jpg", "jpeg"])
        downloader.download_all(all_urls, save_dir)




