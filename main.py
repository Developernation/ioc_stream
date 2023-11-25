import asyncio
import aiohttp
import os
import json
from app import iocstream as ioc

# shodan config processing
shodan_data = ioc.FeedConfigParser("shodan_config.yml", creds="<shodan_api_key>")
shodan_data.feed_parser("shodan")

# urlhaus config processing
urlhaus_data = ioc.FeedConfigParser("urlhaus_abuse_ch.yml")
urlhaus_data.feed_parser("urlhaus")

loop = asyncio.get_event_loop()

# getting shodan data
shodan_res = loop.run_until_complete(shodan_data.fetch_all())
urlhaus_res = loop.run_until_complete(urlhaus_data.fetch_all())

# adding data to the shodan data structure
shodan_res.append(urlhaus_res)
print(json.dumps(shodan_res))
