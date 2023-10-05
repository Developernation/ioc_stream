import os 
import asyncio
import json
from typing import Dict, Any
import aiohttp
import yaml
import os

SHODAN_API_KEY = "<your api key>"

creds_ = dict(shodan_creds=SHODAN_API_KEY) 

# def get_config(config_path:str = os.path.join('configs','feed_config.yml')) -> Dict[Any,Any]: 
#     with open(config_path, 'r') as config_file:
#         config_data = yaml.safe_load(config_file)
#         return config_data

class FeedConfigParser():

    def __init__(self,config_filename:str):
        self.__req_feeds = None 
        self.__config_filename = config_filename
    
    def get_config(self) -> Dict[Any,Any]: 
        config_path = os.path.join('configs',self.__config_filename)
        with open(config_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
            return config_data

    def shodan_parser(self):
        self.__req_feeds = []
        shodan_data = self.get_config()
        shodan_feeds = shodan_data.get('shodan').get('feeds') 
        for feed in shodan_feeds:
            feed['params']['key'] = creds_[shodan_data.get('shodan').get('key')]
            self.__req_feeds.append(
                    {   
                    'feed':'shodan',
                    'feed_name':feed.get('feed_name'),
                    'full_url':f"{feed.get('url')}{feed.get('endpoint')}",
                    'params':feed.get('params')
                    }
                 )
        return self.__req_feeds 

    # async function to make a single request
    async def fetch(self, url, params, feed_name ,session):
        async with session.get(url, params=params, ssl=True) as response:
            status = response.status
            data = await response.json()
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            data_length = len(data)
            data_dict = {
                "url": url,
                "status": status, 
                "data_length": data_length, 
                "feed_name": feed_name, 
                "data": data
                }
            with open(f'{feed_name}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return 
    
    # async function to make multiple requests
    async def fetch_all(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.fetch(feed.get('full_url'),feed.get('params'),session) 
                for feed in  self.__req_feeds
                ]
            results = await asyncio.gather(*tasks)
            return json.dumps(results)


# def parse_config(config_data: Dict[str, Any]):
#     req_feeds = {}
#     for cfg_key in config_data.keys():
#         if cfg_key == 'shodan':
#             shodan_vals = config_data.get('shodan')['feed']
#             endpoint_url = f"{shodan_vals.get('url')}{shodan_vals.get('endpoint')}"
#             headers = shodan_vals.get('headers')
#             shodan_vals['params']['key'] = creds_.get(headers['key'])
#             params = shodan_vals['params']
#             req_feeds.update({f"{cfg_key}-{shodan_vals['feed_id']}":{'url':endpoint_url,'params':params}})
#     return req_feeds

if __name__ == '__main__':
    config_data = FeedConfigParser('shodan_config.yml')
    config_data.shodan_parser()
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(config_data.fetch_all())
    print(res)
    #results = asyncio.run(config_data.fetch_all())


        # resp = requests.get(full_url,headers=headers,params=shodan_vals['params'])
        # resp_data = resp.text
        # print(resp_data)




# port:3389,3306,5985,389 os:"Windows" org:"ReliableSite.Net LLC"
# org = "query=port%3A135+org%3A%22Infium%22"

# query = 'port:135 org:"Infium"'


    
#'port%3A3389%2C3306%2C5985%2C389+os%3A"Windows"+org%3A"ReliableSite.Net+LLC"'

# Wrap the request in a try/ except block to catch errors
# try:
#         # Search Shodan
#         results = api.search(query)

#         # Show the results
#         print('Results found: {}'.format(results['total']))
#         for result in results['matches']:
#                 print('IP: {}'.format(result['ip_str']))
#                 #print(result['data'])
#                 print('***************')
# except shodan.APIError as e:
#         print('Error: {}'.format(e))