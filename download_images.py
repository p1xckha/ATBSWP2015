# -*- coding: utf-8 -*-
"""
Image Site Downloader

author: p1xckha ( https://github.com/p1xckha )



Bot class: 
    Download files using Downloader and MySoup

Downloader class:
    this object handle how to download files

MySoup class:
    this is a subclass of BeautifulSoup.

"""
import requests
import urllib.request, urllib.parse, urllib.error
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import re
import time
import pprint
from pathlib import Path


class Downloader():
    '''
    this class is made mainly to download images from a website.
    '''
    def __init__(self):
        # self._base_url = ""
        self.error_urls = []
        self._save_dir = os.path.join(str(Path.home()), 'Downloads')
    
    @property
    def save_dir(self):
        return self._save_dir
    
    @save_dir.setter
    def save_dir(self, save_dir):
        self._save_dir = os.path.abspath(save_dir)
        
    def get_html(self, url):
        try:
            response = requests.get(url)
            html = response.text
            return html
        
        except Exception as err:
            print("*** Error: can not read the page ***\n%s\n%s" % (url, err))
            self.error_urls.append(url)
            return None
    
    def make_save_dir(self, save_dir):
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def download(self, url, save_dir=None, save_filename=None, prefix=None):
        if save_dir is not None:
            self.save_dir = save_dir
        self.make_save_dir(self.save_dir)
            
        if save_filename == None:
            if prefix == None:
                save_filename = os.path.basename(url) 
            else:
                prefix = str(prefix)
                save_filename = prefix + "_" + os.path.basename(url)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                save_path = os.path.join(self.save_dir, save_filename) 
                with open(save_path, mode="wb") as f:
                    f.write(response.content)
                    print('downloaded: ', save_path)

        except urllib.error.URLError as e:
            print(e)
            self.add_error_url(url)
        except FileNotFoundError as e:
            print(e)
            self.add_error_url(url)
        except OSError as e:
            print(e)
            self.add_error_url(url)
            
    def download_all(self, urls, save_dir=None, prefix=None):
        for url in urls:
            self.download(url, save_dir, save_filename=None, prefix=prefix)
    
    def add_error_url(self, url):
        self.error_urls.append(url)
    
    def show_error_urls(self):
        if len(self.error_urls) > 0:
            print("errors:\n")
            pprint.pprint(self.error_urls)
        else:
            print("No error")
    
    def clear(self):
        self.error_urls.clear()



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
            elif url.startswith("#"):
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


class Bot():
    '''
    bot downloads files using Downloader obj and MySoup obj.
    '''
    def __init__(self):
        self.downloader = Downloader()
    
    def get_internal_urls_from_page(self, url):
        html = self.downloader.get_html(url)
        if html is None:
            return None
        soup = MySoup(html)
        return soup.get_internal_urls_from_links()
    
    def download_all_images_from_page(self, url, save_dir=None):        
        print("getting %s" % (url))
        
        # get html
        html = self.downloader.get_html(url)
        soup = MySoup(html)
        if html is None:
            self.downloader.add_error_url(url)
        else:
            # set base_url
            base_url = re.search('https?://[^/]+', url)[0]
            soup.base_url = base_url
            
            # download images
            urls = soup.get_urls_by_ext(['jpg', 'jpeg', 'JPG', 'JPEG'])
            prefix = int(time.time())
            self.downloader.download_all(urls, save_dir, prefix)
    
    def download_all_images_from_pages(self, urls, save_dir=None):
        for url in urls:
            self.download_all_images_from_page(url, save_dir)
    
    def show_error_urls(self):
        self.downloader.show_error_urls()
    
    def clear(self):
        self.downloader.clear()
    
    def get_home_dir(self):
        home_dir = str(Path.home())
        return home_dir

def example():
    bot = Bot()
    home_dir = bot.get_home_dir()
    save_dir = os.path.join(home_dir, 'Downloads\\xxxxxxxx') # placeholder
    url = url = "https://example.com/xxxxxx/yyy/" # placeholder
    urls = bot.get_internal_urls_from_page(url)
    bot.download_all_images_from_pages(urls, save_dir)
    bot.show_error_urls()
    bot.clear()

def simple_example():
    bot = Bot()
    bot.save_dir = os.path.join(str(Path.home()), 'Downloads\\DeleteMe') # placeholder
    url = "https://example.com/xxxxxx/yyy/" # placeholder
    bot.download_all_images_from_page(url)
    bot.show_error_urls()
    bot.clear()
    
if __name__ == "__main__":
    simple_example()

