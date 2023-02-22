# -*- coding: utf-8 -*-
"""
Image Site Downloader

author: p1xckha ( https://github.com/p1xckha )
"""
import requests
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import re
import time


class Downloader():
    '''
    this class is made mainly to download images from a website.
    '''
    def __init__(self):
        self._base_url = ""
    
    def get_html(self, url):
        try:
            response = requests.get(url)
            html = response.text
            return html
        
        except Exception as err:
            print("*** Error: can not read the page ***\n%s\n%s" % (url, err))
            return None
    
    def make_save_dir(self, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def download(self, url, save_dir='.', save_filename=None, prefix=None):
        save_dir = os.path.abspath(save_dir)
        self.make_save_dir(save_dir)
            
        if save_filename == None:
            if prefix == None:
                save_filename = os.path.basename(url) 
            else:
                prefix = str(prefix)
                save_filename = prefix + "_" + os.path.basename(url)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                save_path = os.path.join(save_dir, save_filename) 
                with open(save_path, mode="wb") as f:
                    f.write(response.content)
                    print('downloaded: ', save_path)

        except urllib.error.URLError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
        except OSError as e:
            print(e)
            
    def download_all(self, urls, save_dir='.', prefix=None):
        for url in urls:
            self.download(url, save_dir, save_filename=None, prefix=prefix)
    
    def filename_suggestion(self, filename):
        #TODO
        pass


class MySoup(BeautifulSoup):
    def __init__(self, html):
        super().__init__(html, "html.parser")
        self._links = None # list of link object
        self._imgs = None # list of img object
        self._base_url = "" 
    
    @property
    def base_url(self):
        return self._base_url
    
    @base_url.setter
    def base_url(self, base_url):
        self._base_url = base_url
    
    @property
    def links(self):
        return self._links
    
    def set_links(self):
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
        
        self._links = links
    
    
    @property
    def imgs(self):
        return self._imgs
    
    def set_imgs(self):
        imgs = []
        tags = self('img')
        for img in tags:
            src = img.get('src', None) 
            data_src = img.get('data-src', None) 
            
            if src is None and data_src is None:
                continue
            elif src.startswith("javascript:"):
                continue
            elif src.startswith('/'):
                src = urljoin(self.base_url, src)
                img['src'] = src
            
            if data_src is not None:
                if data_src.startswith("/"):
                    data_src = urljoin(self.base_url, data_src)
                    img['data-src'] = data_src
                
            imgs.append(img)
        self._imgs = imgs
    
    
    def get_urls_from_links(self):
        if self.links is None:
            self.set_links()
            
        urls = list(map(lambda link: link.get('href'), self.links))
        return urls
    
    def get_urls_from_imgs(self):
        if self.imgs is None:
            self.set_imgs()
        
        img_url = lambda img: img['data-src'] if 'data-src' in img.attrs else img['src']
        urls = list(map(img_url, self.imgs))
        return urls
    
    def get_internal_urls_from_links(self):
        urls = []
        if self.links is None:
            self.set_links()
            if self.links is None:
                return urls
        
        for link in self.links:
            url = link.get('href', None)
            if self.base_url in url:
                urls.append(url)
        
        # remove same url and make urls unique
        urls = list(set(urls))
        
        return urls
    
    def get_urls_by_ext(self, extensions):
        urls = []
        
        if self.imgs is None:
            self.set_imgs()
        
        if self.links is None:
            self.set_links()
        
        if type(extensions) == type(""):
            extensions = [extensions]
            
        for url in self.get_urls_from_imgs():
            for extension in extensions:
                if url.endswith('.' + extension):
                    urls.append(url)
                    break
        
        for url in self.get_urls_from_links():
            for extension in extensions:
                if url.endswith('.' + extension):
                    urls.append(url)
                    break
        
        # remove same url and make urls unique
        urls = list(set(urls))
        
        return urls
    
    
def this_example_cannot_run_without_replacing_placeholders():
    downloader = Downloader()
    url = 'https://example.com/xxxxxxx/' # replace with real url
    
    # get html
    html = downloader.get_html(url)
    soup = MySoup(html)
    tag = soup.find('div', {'class': "posts-wrapper"}) # replace with real class name
    soup = MySoup(tag.prettify()) # tag -> soup
    
    # set base_url
    base_url = re.search('https?://[^/]+', url)[0]
    soup.base_url = base_url
    
    # get article urls
    internal_urls = soup.get_internal_urls_from_links()
    save_dir = 'C:\\Users\\t0\\Downloads\\midori'
    
    # download the jpg images in the articles
    for url in internal_urls:
        print(url)
        html = downloader.get_html(url)
        if html is None:
            continue
        
        soup = MySoup(html)
        tag = soup.find('div', {'class': "nv-content-wrap entry-content"}) # replace with real class name
        soup = MySoup(tag.prettify()) # tag -> soup
        soup.base_url = base_url
        urls = soup.get_urls_by_ext(['jpg', 'JPEG'])
        prefix = int(time.time())
        downloader.download_all(urls, save_dir, prefix)


def print_all_links():
    downloader = Downloader()
    url = 'https://www.reddit.com/'

    # get html
    html = downloader.get_html(url)
    soup = MySoup(html)
    
    # set base_url
    base_url = re.search('https?://[^/]+', url)[0]
    soup.base_url = base_url

    if html is None:
        exit(-1)
    
    urls = soup.get_internal_urls_from_links()
    print(urls)

    
if __name__ == "__main__":
    print_all_links()



