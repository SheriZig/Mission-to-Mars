# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

# Import Pandas
import pandas as pd
import datetime as dt


# ## set up Chrome 
# executable_path = {'executable_path': ChromeDriverManager().install()}
# browser = Browser('chrome', **executable_path, headless=False)


# Connect to Mongo and establish communication between our code and the database
def scrape_all():
    # Initate headless driver (user will not see the scraping action) for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
# Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : hemisphere_images(browser)
    }

   
    # Stop webdriver and return data
    browser.quit()
    return data


# Refactor to create functions to combine segments of the code into a 
# reusable function.
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None 

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():

    # Add Try/Except error handling
    try: 
        # Define dataframe for Earth/Mars comparison table
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
    
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    

    # Convert dataframe to html
    return df.to_html()

def hemisphere_images(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url)


    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    url = 'https://marshemispheres.com/'

    browser.visit(url)

    html = browser.html

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for image in range (0, 4):
        browser.visit(url)
        home_page = browser.find_by_tag('h3')[image]
        home_page.click()
        html = browser.html
        img_soup = soup(html, 'html.parser')

        image_class = img_soup.find('div', class_='downloads')
        image_url = image_class.find('a').get('href')
        image_full_url = f'https://marshemispheres.com/{image_url}'
        title = img_soup.h2.text
        hemispheres = {'image_url': image_full_url, 'title': title}
        
        #if hemispheres not in hemisphere_image_urls:
        hemisphere_image_urls.append(hemispheres)


    # 4. Print the list that holds the dictionary of each image url and title.
    return hemisphere_image_urls

   
# Tells flask that the code is complete and ready for action
if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())


