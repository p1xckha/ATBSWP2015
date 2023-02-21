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
        except OSError as e:
            print(e)
            
    def download_all(self, urls, save_dir='.'):
        for url in urls:
            self.download(url, save_dir)


class MySoup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")
        self.links = None # list of link object
        self.imgs = None # list of img object
        self._base_url = ""
    
    @property
    def base_url(self):
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url
    
    def get_all_links(self):
        links = [] # list of link object
        tags = self('a')
        for link in tags:
            # make url valid
            url = link.get('href', None)
            if url is None:
                continue
            elif url.startswith("javascript:"):
                continue
            else:
                url = urljoin(self.base_url, url)
                link['href'] = url
                links.append(link)
        
        self.links = links
            
    def get_all_urls_from_links(self):
        if self.links is None:
            self.get_all_links()
            
        urls = list(map(lambda link: link.get('href'), self.links))
        return urls
    
    def get_all_imgs(self):
        imgs = []
        tags = self('img')
        for img in tags:
            url = img.get('src', None)
            if url is None:
                continue
            elif url.startswith("javascript:"):
                continue
            else:
                url = urljoin(base_url, url)
                img['src'] = url
            imgs.append(img)
        self.imgs = imgs
        
    def get_all_urls_from_imgs(self):
        if self.imgs is None:
            self.get_all_imgs()
        
        urls = list(map(lambda img: img.get('src'), self.imgs))
        return urls
    

    
if __name__ == "__main__":
    downloader = Downloader()
    url = 'https://www.reddit.com/'
    
    # get html
    html = downloader.get_html(url)
    soup = MySoup(html)
    
    # get all internal links
    base_url = re.search('https?://[^/]+', url)[0]
    soup.base_url = base_url
    
    urls = soup.get_all_urls_from_imgs()
    save_dir = 'test2'
    downloader.download_all(urls, save_dir)



