import os 
import asyncio
import json
import logging
from typing import List, Dict, Any
import aiohttp
import yaml
import os

logging.basicConfig(level=logging.WARNING,format='%(process)d-%(levelname)s-%(message)s')

class FeedConfigParser():

    def __init__(self,config_filename:str, creds: str = None) -> None:
        self.__req_feeds = None 
        self.creds = creds
        self.__config_filename = config_filename
    
    def get_config(self) -> Dict[Any,Any]: 
        config_path = os.path.join('configs',self.__config_filename)
        with open(config_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
            logging.debug(config_data)
            return config_data

    def feed_parser(self,vendor: str,) -> List[Dict]:
        self.__req_feeds = []
        data = self.get_config()
        feeds = data.get(vendor).get('feeds') 
        for feed in feeds:
            if feed.get('params'): 
                feed['params']['key'] = self.creds       
            self.__req_feeds.append(
                {   
                'feed':vendor,
                'feed_name':feed.get('feed_name'),
                'full_url':f"{feed.get('url')}{feed.get('endpoint')}",
                'params':feed.get('params')
                }
                )
        logging.debug(self.__req_feeds)
        return self.__req_feeds 

    # async function to make a single request
    async def fetch(self, url, params, feed_name ,session):
        async with session.get(url, params=params, ssl=True) as response:
            status = response.status
            response.encoding = 'utf-8'
            data = await response.json(content_type='application/json')

            data_length = len(data)
            data_dict = {
                "url": url,
                "status": status, 
                "data_length": data_length, 
                "feed_name": feed_name, 
                "data": data
                }
            return data_dict
    
    # async function to make multiple requests
    async def fetch_all(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch(feed.get('full_url'),feed.get('params'),feed.get('feed_name'),session) 
                for feed in  self.__req_feeds
                ]
            results = await asyncio.gather(*tasks)
            return results
