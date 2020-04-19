# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import requests
from bs4 import BeautifulSoup

class AtiracrawlerSpider(CrawlSpider):
    name = 'AtiraCrawler'
    allowed_domains = ['atira.com']
    start_urls = ['https://atira.com/']

    rules = (
        Rule(LinkExtractor(allow=r'(/city/)'), callback='parse_city', follow=True),
        Rule(LinkExtractor(allow=r'(/location/)'), callback='parse_locations', follow=True),
        Rule(LinkExtractor(allow=r'(/room/)'), callback='parse_rooms', follow= False)
    )

    # cities
    cities = {}

    # locations as key and their city as value
    locations = {}

    visited_url = {}

    def parse_city(self, response):
        city_name = str(str(response.url).split('/')[4]).capitalize()
        self.cities[city_name] = response.url

        # send request to get data
        city_page = requests.get(response.url, headers={'User-Agent': 'Mozilla/5.0'}).text

        soup = BeautifulSoup(city_page, 'html.parser')
        result = soup.find_all('div', { 'class': 'image-gallery__caption'})

        for e in result:
            # print('++++++++++++++++++++++++++++++++++')
            # print('location and city name')
            # print(e.text.strip() + city_name)
            # print('++++++++++++++++++++++++++++++++++')
            self.locations[e.text.strip()] = city_name
        self.visited_url[response.url] = None
        print('crawling -> '+ response.url)
   
    def parse_locations(self, response):
        self.visited_url[response.url] = None
        print('crawling -> '+ response.url)
        

    def parse_rooms(self, response):
        res = requests.get(response.url, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(res, 'html.parser')

        # price
        price = soup.find('span', {'class': 'room__sidebar--rate-base'}).text.strip()

        # building name
        building_name = soup.find('h5', {'class': 'room__location--title'}).text.strip()

        # room name
        room_name = soup.find('h1', { 'class': 'room__title'}).text.strip()

        # room features
        room_features = soup.find('div', {'class': 'room__features'}).get_text().split('\n')
        self.remove_empty_strings(room_features)

        print('crawling -> '+ response.url)

        # capacity
        capacity = soup.select('#body > div.global-wrapper > main > section.section-room > div.row > div.columns.small-12.medium-4.room-sidebar > div > div.room__sidebar--form-wrapper.loader-wrapper > div.room__sidebar--icons > ul > li:nth-child(1)')[0].text.strip()

        # location
        location = soup.find('div', { 'class': 'address'}).get_text().strip()

        # city of location
        cityOfLocation = self.get_city_of_location(location)

        # print('++++++++++++++++++++')
        # print('Room Name: '+ room_name)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('Building Name: '+ building_name)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('Room Features: ')
        # print(room_features)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('price: '+ price)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('Capacity: '+ capacity)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('Location: '+ location)
        # print('++++++++++++++++++++')
        # print('++++++++++++++++++++')
        # print('City: '+ cityOfLocation)
        # print('++++++++++++++++++++')

        item = scrapy.Item()
        item.fields['city'] = cityOfLocation
        item.fields['buildingName'] = building_name
        item.fields['roomName'] = room_name
        item.fields['price'] = float(price)
        item.fields['capacity'] = int(capacity)
        item.fields['roomFeatures'] = room_features
        item.fields['location'] = location
        self.visited_url[response.url] = None

        yield item.fields
    
    def remove_empty_strings(self, arr):
        while '' in arr or ' ' in arr:
            if '' in arr:
                arr.remove('')
            else:
                arr.remove(' ')
    
    def get_city_of_location(self, l):
        for k in self.locations:
            if k in l:
                return self.locations[k]


