from bs4.element import SoupStrainer
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
import time


def can_fetch(robots_parser, url):
  return robots_parser.can_fetch('*', url)

#Given website start_url is where we start scraping from.
def crawl_website(start_url):
# Read files from seed website. Define location of the website so we don't crawl other websites.
# Try printing this parsed_start_url in the Shell.
  parsed_start_url = urlparse(start_url)
  base_domain = parsed_start_url.netloc

# Read robots.txt file. Define the location of the robots.txt file. Define a Parser that parses the robots.txt file. 
# Give the location of the file to the parser. Read the file. 
  robots_url = urljoin(start_url, 'robots.txt')
  robots_parser = RobotFileParser()
  robots_parser.set_url(robots_url)
  robots_parser.read()

# Make sure we don't visit links we've already visited. 
# Sets are good for storage - they reject duplicates.   
  visited_urls = set()
  urls_to_visit = [start_url]
  url_count = 0

#Introduce the bot to the website. 
  headers = {
    'Code-Collector': 'WebCrawler/1.0 (Simple web crawler that identifies and collects code for a prototype of a                multimodal neural network. mailto: chris@nexusbios.co.'
  }

  while urls_to_visit:
    url = urls_to_visit.pop(0)
    url_count += 1
    print(f"Visiting: {url}") # When in the program do we visit url? Where do we visit the next link in urls_to_visit? 

# If we already visited the link or we can't get the robots.txt file?, go to the next link.
    if url in visited_urls or not can_fetch(robots_parser, url):
      continue
    visited_urls.add(url)

# Request files from the server. 
    try:
      response = requests.get(url, headers=headers, timeout=5) # Review
      response.raise_for_status()
    except requests.exceptions.RequestException as e:
      print(f"Error fetching {url}: {e}")
      continue

# Gets the content of the html_file (locates and opens the file?), and reads the file. Saves contents to soup.
    soup = BeautifulSoup(response.content, 'html.parser') # Review 

# Collects all the links from the link were currently on. Sends links we haven't visited to urls_to_visit.
    links = soup.find_all('a', href=True)
    for link in links:
      href = link['href']
      full_url = urljoin(url, href)
      parsed_link_url = urlparse(full_url)
      if parsed_link_url.netloc == base_domain and full_url not in visited_urls: 
        urls_to_visit.append(full_url)

    images = soup.find_all('img', src=True)
    
    if not os.path.exists("downloaded_images"):
      os.makedirs("downloaded_images")
      
    for image in images:
      image_url = image['src']
      full_image_url = urljoin(url, image_url)
      try: 
        response = requests.get(full_image_url, headers=headers, timeout=5) # Tries to download the image.
        response.raise_for_status()
        with open(os.path.join("downloaded_images", os.path.basename(full_image_url)), "wb") as f:
          f.write(response.content) # Writes the actual image data to the file
        print(f"Downloaded image: {full_image_url}")
      except requests.exceptions.RequestException as e:
        print(f"Error downloading {full_image_url}: {e}")
          
    time.sleep(1)

start_url = "https://blog.codinghorror.com/"
crawl_website(start_url)
# Search each repository, search for program files for a line of code. Download the file. Move on to the next repository.
# How do I search every GitHub repository for code I want, and download the program files?
# Search box where you can enter code, and it returns all of the source code files with that code.