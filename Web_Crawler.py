#!/usr/bin/python
import sys
from optparse import OptionParser
from crawl import *
import os

##### Web Crawler ####

'''
 The given program crawls a given URL and outputs a site map showing the static assets for each page, 
 not following the links to other websites. BeautifulSoup is used in order to parse the html code of a website. 
 The sitemap is given in two different formats: a sitemap.txt (prints each page with its static assets) and a 
 sitemap_google.xml following the sitemap protocol of Google.

 It can be called with the -url and -dir option for the url to crawl and the directory to store the files respectively.
 Example of usage: python Web_crawler.py --url "https://gocardless.com" --dir "/home"
'''

global root_url
global folder_name

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--dir", type="string", dest="foldername", default="")
    parser.add_option("--url", type="string", dest="root_url", default="https://gocardless.com")
    (options, args) = parser.parse_args(sys.argv)
    
    crawler = Crawl(options.root_url)

    # Check if the path given is a folder
    if (options.foldername!="") and (not os.path.isdir(options.foldername)):
        print('The folder path given is not correct. Outputs will be saved in the current directory.')
        options.foldername = ""

    # Write the output files
    file = open(options.foldername+"/sitemap.txt","w")
    file.write(crawler.get_pages())
    file.close()

    file = open(options.foldername+"/sitemap_google.xml","w")
    file.write(crawler.get_google_xml())
    file.close()