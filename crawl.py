from bs4 import BeautifulSoup
import requests
import re
from page import *

'''
 Class getting the pages of a website and its static assets
'''
class Crawl:
    def __init__(self, root):
        self.root_url = root
        self.pages={}
        self.crawl_page(self.root_url)

    '''
     Returns the url only if it is within the domain. If it begins with '/' it is the absolute path from the root url, 
     otherwise it has to begin with the root url to be accepted as we don't crawl other websites.
    '''
    def get_url(self, url, page_url):
        # Absolute path
        if url.startswith('/'):
            return self.root_url + url
        # Link to a full url
        if url.startswith('http'):
            if url.startswith(self.root_url):
                return url
            else:
                return ''
        return ''

    '''
     Keeps only valid URLs from the list returned by soup
    '''
    def apply_url(self, l, page):
        url = self.get_url(l['href'], page)
        # No special chars
        chars = set(';?@=&$,#')
        check = True
        if any((c in chars) for c in url):
            check = False
        if (url != '') & check:
            return url
        return ''

    '''
     Returns the unique list of urls accessible from the page p
     It crawls the alternate versions of the page as well
    '''
    def get_urls_page(self, soup, p):
        l = []
        links = soup.find_all('a', href=True) + soup.find_all('link', href=True, rel='alternate')
        for link in links:
            url = self.apply_url(link,p)
            if url !=  '':
                l.append(url)
        return list(set(l))

    '''
     It returns a unique list of the data (image/style_sheets/scripts) from the list returned by soup,
     keeping only the field p we are interested in
    '''
    def get_data(self, soup_list, p):
        l = []
        if soup_list:
            for s in soup_list:
                l.append(s[p])
            if l:
                return list(set(l))
            return l
        return l

    '''
     Regex to search images
    '''
    def image(self,t):
        return (t and re.compile("image").search(t))

    '''
     Crawls a page and recursively crawls each children if is has not been crawled yet
    '''
    def crawl_page(self, url):
        # Try to get the page
        try:
            page = requests.get(url)
        except requests.exceptions.RequestException: 
            page = None

        # If there is a reply to the request
        if page:
            html_page = page.text
            # Get the html
            soup = BeautifulSoup(html_page,'lxml')
            # Instantiate the new page found and add the static assets
            p = Page(url)
            p.children = self.get_urls_page(soup, url)
            p.style_sheets = self.get_data(soup.find_all('link', rel='stylesheet'), 'href')
            p.scripts = self.get_data(soup.find_all('script', src=True), 'src')
            p.images = self.get_data(soup.find_all('img', src=True ), 'src')
            p.images = p.images + self.get_data(soup.find_all('link', href=True, type=self.image), 'href')
            # Add it to the dictionary
            self.pages[url] = p
            print(url)
            # Crawl the links found in the page
            for c in p.children:
                if c not in self.pages:
                    self.crawl_page(c)

    '''
     Goes through the entries of the dictionary and saves each entry in the file "sitemap.txt"
    '''
    def get_pages(self):
        s = ''
        for entry in self.pages:
            toPrint = self.pages[entry].get_str()
            toPrint = toPrint.encode('utf-8')
            s = s+toPrint
        return s

    '''
     Goes through the entries of the dictionary and saves each entry in the file "sitemap_google.xml"
     Following Google standard
    '''
    def get_google_xml(self):
        s = '<?xml version="1.0" encoding="UTF-8"?> <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">'
        for page in self.pages:
            s = s+'<url><loc>'+page+'</loc>'
            for image in self.pages[page].images:
                s = s+'<image:image><image:loc>'+image+'</image:loc></image:image>'
            s = s+'</url>'
        s = s+'</urlset>'
        return s.encode('utf-8')