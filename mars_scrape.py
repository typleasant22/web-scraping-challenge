# import dependencies
import os 
from gettext import install
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
import pandas as pd
import urllib.request
import json
from flask import Flask, render_template, redirect
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {
        'executable_path': '/Users/tyannapleasant/.wdm/drivers/chromedriver/mac64/98.0.4758.102/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    scraped_data = {}

    # # NASA - Scraping Most Recent Mars News

    # create a connection to NASA site
    url1 = 'https://redplanetscience.com/'
    browser.visit(url1)

    # Create a Beautiful Soup and HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape the Mars News Site and collect the latest News Title
    nasa_title = soup.find('div', class_='content_title').text
    print(nasa_title)

    # Scrape the Mars News Site and collect the Paragraph Text
    nasa_paragraph = soup.find('div', class_='article_teaser_body').text
    print(nasa_paragraph)

    # add nasa title
    scraped_data['nasa_title'] = nasa_title
    scraped_data['nasa_paragraph'] = nasa_paragraph

    # create a connection to NASA image site
    url2 = 'https://spaceimages-mars.com'
    browser.visit(url2)

    # Create a Beautiful Soup and HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # Find the image url to the full size `.jpg` image.

    nasa_img = soup.find('img', class_='headerimage fade-in')['src']

    # Assign the url string to a variable called `featured_image_url`.
    featured_image_url = f"https://spaceimages-mars.com/{nasa_img}"
    print(featured_image_url)

    # add nasa featured image to scraped_data dictionary
    scraped_data['featured_image_url'] = featured_image_url

    # # Mars Facts - Scraping with Pandas

    # use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    url3 = 'https://galaxyfacts-mars.com'
    tables = pd.read_html(url3)

    # extract only the second table containing 'MARS PLANET PROFILE'
    tables_df = tables[1]

    # adding column names to new dataframe containing mars info
    mars_df = pd.DataFrame({
        'Mars Profile': tables_df[0],
        'Measurements': tables_df[1]
    })

    # convert the data to a HTML table string and removing unwanted newlines
    html_table = mars_df.to_html().replace('\n', '')

    # add mars info df to scraped_data dictionary
    scraped_data['mars_df'] = mars_df

    # # Mars Hemispheres

    # create a connection to GUSS astropedia site
    url4 = 'https://marshemispheres.com/'
    browser.visit(url4)

    # Create a Beautiful Soup and HTML object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # return an iterable list of all the hemisphere links
    results = soup.find_all('div', class_='item')

    # create an empty list for image urls
    hemisphere_image_urls = []

    for result in results:
        hemispheres = {'title': result.find('h3').text, 'img_url': result.img['src']}

        # Append Hemisphere Object to List
        hemisphere_image_urls.append(hemispheres)

    # display hemisphere_image_urls list using json
    print(json.dumps(hemisphere_image_urls, sort_keys=False, indent=4))

    # add mars hemisphere info to scraped_data dictionary
    scraped_data['hemisphere_image_urls'] = hemisphere_image_urls

    # Close the browser after scraping
    browser.quit()

    # return final dictionary
    return scraped_data
    