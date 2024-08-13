import requests
from bs4 import BeautifulSoup
import os

home_url = "https://www.cnn.com"

def get_links_from_url(url, container_class, base_url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    containers = soup.find_all('div', class_=container_class)
    
    links = []
    
    for container in containers:
        for a_tag in container.find_all('a', href=True):
            link = a_tag['href']
            full_link = requests.compat.urljoin(base_url, link)
            links.append(full_link)
            
    res = []
    [res.append(x) for x in links if x not in res]
    return res

def get_links_from_sports_page(sports_url):
    containers = ['container__field-links container_lead-plus-headlines-with-images__field-links', 'container__field-links container_lead-plus-headlines__field-links', 'container__field-links container_vertical-strip__field-links']

    all_links = []
    for container in containers:
        links = get_links_from_url(sports_url, container, home_url)
        all_links.extend(links)

    return all_links


def get_content(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content_list = []
    
    script_tag = soup.find('script', type='application/ld+json')
    if script_tag:
        json_content = script_tag.string
        if '"articleBody":' in json_content:
            start = json_content.find('"articleBody":') + len('"articleBody":')
            end = json_content.find('","', start)
            article_body = json_content[start:end].strip(' "')
            content_list = [article_body]
    
    return content_list

def get_filename_from_url(url):
    parts = url.split('/')
    filename = parts[-2] if parts[-1] == 'index.html' else parts[-1].replace('.html', '')
    return filename


def scrape_and_save_content(save_dir, urls):
    os.makedirs(save_dir, exist_ok=True)
    
    all_links = []
    for url in urls:
        all_links += get_links_from_sports_page(url)
    
    for link in all_links:
        content = get_content(link)
        if content and any(content):
            filename = os.path.join(save_dir, f"{get_filename_from_url(link)}.txt")
            with open(filename, 'w', encoding="utf-8") as file:
                for item in content:
                    file.write(f"- {item}\n")
            print(f"Content saved to {filename}")
        else:
            print(f"-")
 
