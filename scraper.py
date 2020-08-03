import recipe_scrapers
import requests
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from models import LinksBacklog, Recipe

import logging
logging.basicConfig(
    level=logging.INFO,
    filename='./scraper-data/scraper.log'
)

class Scraper:
    def __init__(self, website_url):
        self.website_url = website_url

    def get_base_url(self, url):
        '''
        Returns base_url from a given url
        :param url: Pass the url
        :return: base_url
        '''
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        return base_url

    def get_domain(self, url):
        '''
        Returns domain domain from a given url
        :param url: Pass the url
        :return: domain name
        '''
        parts = urlsplit(url)
        base = "{0.netloc}".format(parts)
        tld = base.replace("www.", "")
        return tld

    def get_links_from_url(self, url):
        '''
        Retrieves all local links on a given url
        :param url: Pass the url
        :return: list of links
        '''
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            parsed_links = soup.find_all('a', href=True)
            website_domain = self.get_domain(self.website_url)
            website_base_url = self.get_base_url(self.website_url)
            links = []
            links.append(url)

            for link in parsed_links:
                anchor = link.get('href')
                if anchor.startswith('/'):
                    absolute_url = website_base_url + anchor
                    links.append(absolute_url)
                elif self.get_domain(anchor) == website_domain:
                    links.append(anchor)
                else:
                    logging.info('External url: ' + anchor)

            return links
        except requests.exceptions.RequestException as e:
            logging.error(e, exc_info=True)
            return []
        # except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema):
        #     logging.error(e, exc_info=True)
        #     return []

    def save_links_from_url(self, url):
        '''
        Saves all links on a given url in the db to be processed later
        :param url: Pass the url
        :return:
        '''
        links = self.get_links_from_url(url)
        for link in links:
            LinksBacklog.create_link(
                    url=link,
                    domain=self.get_domain(link)
                )

    def process_recipe_from_url(self, url):
        '''
        Saves recipe info in DB from a given url
        :param url: Pass the url
        :return:
        '''
        try:
            scraper = recipe_scrapers.scrape_me(url)
            recipe_obj = {
                'title': scraper.title(),
                'ingredients': scraper.ingredients(),
                'instructions': scraper.instructions(),
                'total_time': scraper.total_time(),
                'yields': scraper.yields(),
                'external_url': url,
                'host_image_url': scraper.image(),
                'host_author': scraper.author(),
                'host_ratings': scraper.ratings(),
                'language': scraper.language()
            }
            Recipe.create(**recipe_obj)
        except Exception as e:
            logging.error(e, exc_info=True)
            return str(e)

    def start(self):
        '''
        Starts scraping recipes from a given website
        :param website_url: Pass the url of the website
        :return:
        '''
        logging.info('Starting scraping: ' + self.website_url)
        page = 1
        current_url = self.website_url
        domain = self.get_domain(self.website_url)
        self.save_links_from_url(self.website_url)

        while 1:
            links = LinksBacklog.get_links_to_scrape(domain, page)
            if len(links) == 0:
                break

            for link in links:
                logging.info('processing url: ' + link.url)
                self.save_links_from_url(link.url)
                self.process_recipe_from_url(link.url)
                LinksBacklog.mark_link_as_scraped(link.id)
                sleep(3)

            # break # only for development
            page += 1

scraper = Scraper('https://www.allrecipes.com')
scraper.start()
