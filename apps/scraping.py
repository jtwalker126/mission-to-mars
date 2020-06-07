# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
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

def hemisphere_images():
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    urls = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced', 
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
        'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
        ]
    hemisphere_data = []

    for url in urls:
        hemisphere={}
        browser.visit(url)
        html = browser.html
        img_soup = BeautifulSoup(html, 'html.parser')
        img_url_rel = img_soup.select_one('img.wide-image').get("src")
        img_url = f'https://astrogeology.usgs.gov/{img_url_rel}'
        title = img_soup.find("h2", class_='title').get_text()
        hemisphere = {'title': title, 'img_url': img_url}
        hemisphere_data.append(hemisphere)

    browser.quit()
    return hemisphere_data


def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    
    # try except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_='content_title').get_text()

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    return news_title, news_p

# ### Featured Images
def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

def mars_facts():
    #error handling
    try:
        # use 'read_html' to scape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    return df.to_html()

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())