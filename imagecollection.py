import hashlib
import os
import random
import time
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


# Read the robots.txt file/check if we're allowed to access the url. 
def can_fetch(robots_parser, url):
  return robots_parser.can_fetch('Image Collector', url)

# Website start_url is where we start scraping from.
# Define location of the website so we don't go on other websites.
def crawl_website(start_url):
  parsed_start_url = urlparse(start_url)
  base_domain = parsed_start_url.netloc
  

# Get the html content from the web page. Use soup to get the image elements from the web page.
# Read robots.txt file. Define the location of the robots.txt file. Define a Parser that parses the robots.txt file. 
# Give the location of the file to the parser. Read the file. 
  robots_url = urljoin(start_url, 'robots.txt')
  robots_parser = RobotFileParser()
  robots_parser.set_url(robots_url)
  robots_parser.read()

# Make sure we don't visit links we've already visited. 
# Sets are good for storage - they reject duplicates.  
# Initialize a list with the starting url.
  visited_urls = set()
  urls_to_visit = [start_url]
  url_count = 0
  downloaded_images = set()
  image_counter = 1 
  if not os.path.exists("downloaded_images"):
    os.makedirs("downloaded_images")
# Introduce the bot to the website for the HTTP requests. 
  headers = {
    'User-Agent': 'Coding Horror Image Collector - Scraper/1.0 (Simple web scraper that collects all of the images from the Coding Horror Blog. mailto: chris@nexusbios.co.)'
  }

  def generate_filename(image_url, image_counter):
    url_hash = hashlib.md5(image_url.encode()).hexdigest()
    return f"{url_hash}_{image_counter}.jpg"
  
  while urls_to_visit:
    url = urls_to_visit.pop(0)
    visited_urls.add(url)
    print(f"Visiting: {url}")
  
# Locate all images in the html file. Use the requests library to interact with the html. 
    try: 
      response = requests.get(url, headers=headers, timeout=5)
      response.raise_for_status()
# Create a folder for the images.  
# Collect all the links from the website. Append links to urls_to_visit. 
# Get image_url from url first? 
# Download each image on the page. 
    
      soup = BeautifulSoup(response.content, 'html.parser')
      images = soup.find_all('img', src=True)
    
      for image in images:
        src = image['src']
        full_image_url = urljoin(url, src)
        image_url_response = requests.get(full_image_url, headers=headers, timeout=5)
        image_url_response.raise_for_status()
        filename = generate_filename(full_image_url, image_counter)
        if filename not in downloaded_images:
          filepath = os.path.join("downloaded_images", filename) 
          with open(filepath, "wb") as f:
            f.write(image_url_response.content)
          downloaded_images.add(filename)
          image_counter += 1
          print(f"Downloaded image: {full_image_url} as {filename}")
          time.sleep(random.uniform(1, 5))
      
      link = soup.find('a', class_="older-posts", href=True)
      if link:
        next_page = urljoin(url, link['href'])
        if next_page not in visited_urls and next_page not in urls_to_visit:
            urls_to_visit.append(next_page)

    except requests.RequestException as e:
      print(f"Error occured while processing {url}: {e}")
      
    
# <a class="older-posts" href="/page/2/">Older Posts <span aria-hidden="true">&rarr;</span></a>     
# Go to the next page after we're done collecting all the images on page one. 

# Initiate crawling process. 
start_url = "https://blog.codinghorror.com/"
crawl_website(start_url)
# Search each repository, search for program files for a line of code. Download the file. Move on to the next repository.
# How do I search every GitHub repository for code I want, and download the program files?
# Search box where you can enter code, and it returns all of the source code files with that code.
