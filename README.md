# Web Crawler for GoCardless

## Specs
Design a web crawler outputting a site map showing the static assets of each page of a given URL. 

## Design decisions

### Programming Language
Python is a really powerful scripting language which offers many packages to handle various programming tasks. In this situation, the main challenge is to parse the HTML file to get the desired fields. We have to find all the links to other pages from a given page and we have to find all its static assets. BeautifulSoup is a good HTML parser which facilitates searching special tags. To retrieve the pages, we can simply use the Requests HTTP library and then feed BeautifulSoup with them.

### Choices of static assets
Images, scripts and css stylesheets are considered as static assets. I have worked in a Jupyter Notebook to make some tests and design the solution. You can find it in the folder under the name "WebCrawler.ipynb" as well as a pdf. It explains each step of the design.

### Output of the programme
The results are stored in a file, in this format:

########https://gocardless.com/about/jobs/inside-account-executive-spain/########

||Number of links: 60
	 - https://gocardless.com/about/jobs/head-of-operations/
	 - https://gocardless.com/fr-fr/
	 - https://gocardless.com/about/jobs/european-marketing-manager/
	 - ...

||Number of CSS stylesheets: 1
	 - /bundle/main-83fa229a41c5c6dfb1ef.css

||Number of scripts: 1
	 - /bundle/main-83fa229a41c5c6dfb1ef.js

||Number of images: 19
	 - /images/flags/CA-flag-icon@2x.png
	 - /images/flags/BE-flag-icon@2x.png
	 - /images/flags/NL-flag-icon@2x.png
	 - ...

We create a valid Google XML site map as well, following their protocol:

<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" 
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" 
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url> 
    <loc>http://www.example.com/foo.html</loc> 
    <image:image>
       <image:loc>http://example.com/image.jpg</image:loc>
       <image:caption>Dogs playing poker</image:caption>
    </image:image>
    <video:video>
      <video:content_loc>
        http://www.example.com/video123.flv
      </video:content_loc>
      <video:player_loc allow_embed="yes" autoplay="ap=1">
        http://www.example.com/videoplayer.swf?video=123
      </video:player_loc>
      <video:thumbnail_loc>
        http://www.example.com/thumbs/123.jpg
      </video:thumbnail_loc>
      <video:title>Grilling steaks for summer</video:title>  
      <video:description>
        Cook the perfect steak every time.
      </video:description>
    </video:video>
  </url>
</urlset>

I learned how site maps were actually useful for web browsers in this assignment so I thought it would be reasonable to output a valid format.

## Run it!
It has been written in Python 2.7. You can download the following packages from your terminal:

$ pip install requests
$ pip install beautifulsoup4

Run the script:
$ python Web_Crawler.py --url "https://gocardless.com" --dir "/Users/prisca/Documents/"

The default value for the url is  "https://gocardless.com" and for the directory it is the current directory.

Whilst the program is running, it prints in the console every new page it founds. 

## Why I liked it:
I don't write many web-based applications so I spent some time looking for examples and trying to understand better the big picture. Then I looked at different specific problems I would face, like parsing a html file, getting the valid url, etc. I've tried to do it in a "clean" way, even though I might have missed many details. I enjoyed seeing all the possibilities those libraries can offer. It is nice to start from scratch to do this kind of small project and put the components together.