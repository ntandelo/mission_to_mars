


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager



# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site


# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)



# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')



# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


df.to_html()


browser.quit()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

subbrowser = Browser('chrome', **executable_path, headless=False)

hemisphere_image_urls = []

for link in browser.links.find_by_partial_text('Hemisphere Enhanced'):
    # link.click()
    
    subbrowser.visit(link._element.get_attribute("href"))
    html = subbrowser.html
    mars_soup = soup(html, 'html.parser')
    allinks = mars_soup.find_all("a", target="_blank")
    title = mars_soup.find("h2", class_='title').text

    imgurl = "https://marshemispheres.com/" + allinks[2].get('href')
    print("For page=", link._element.get_attribute("href"), " link=", imgurl, "title= ", title)
    # browser.back()
    
    hemisphere_image_urls.append({"img_url": imgurl, "title": title})

hemisphere_image_urls

subbrowser.quit()
browser.quit()



# Make sure to click every one and go back
# button1 = browser.links.find_by_partial_text('Hemisphere Enhanced').click()

# button2 = browser.find_by_id('wide-image-toggle').click()
# # button3 = browser.links.find_by_partial_text('Sample').click()
# # browser.is_element_present_by_css('img', wait_time=1)


# browser.back()
# # imgurl.find('a').get('src')


# imgurl

# # 
# imgurl = mars_soup.select_one('img.wide-image')
# img_url_jpg = mars_soup.find('img', class_='wide-image').get('src')
# title = mars_soup.find('h2', class_='title').get('src')
# title

#splashy > div.wrapper > div.container > div.content > section > h2.title.__web-inspector-hide-shortcut__
#product-section > div.collapsible.results > div:nth-child(1) > a > img
# <a href="/search/map/Mars/Viking/cerberus_enhanced" class="itemLink product-item"><h3>Cerberus Hemisphere Enhanced</h3></a>







