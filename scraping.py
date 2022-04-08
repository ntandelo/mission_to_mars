
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt
import traceback

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data



def mars_news(browser):
    #visit mars website
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')
        #begin scraping titles
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #begin scraping titles
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError as e:
        print(e)
        return None, None

    return news_title, news_p



def featured_image(browser):
    print("Finding featured image")
    #visit url
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_css('button.btn-outline-light')
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    
    try:
        if browser.is_element_present_by_css('img.fancbox-image', wait_time=3):
            print("here it is")
        else:
            print("not here at all")

        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        print(traceback.format_exc())
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    
    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    


    return df.to_html(classes ="table table-striped")

if __name__ == "__main__":
    print(scrape_all())


