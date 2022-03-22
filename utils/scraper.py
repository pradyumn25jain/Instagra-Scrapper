import time
import random
from datetime import datetime
from utils.customrequests import Custom_Requests


class Scraper:
    def __init__(self) -> None:
        self.sessionid = '39673737047%3Acf6Ydg9lghnde6%3A23'
        self.h = {'Accept-Language':'en-US,en;q=0.5',"Cookie":"sessionid={}".format(self.sessionid)}
        self.cr = Custom_Requests(use_proxy_param=True, use_session=True)


    def find(self,key, dictionary):
        if isinstance(dictionary, dict):
            for k, v in dictionary.items():
                if k == key:
                    yield v
                elif isinstance(v, dict):
                    for result in self.find(key, v):
                        yield result
                elif isinstance(v, list):
                    for d in v:
                        for result in self.find(key, d):
                            yield result
        else:
            if isinstance(dictionary, list):
                for d in dictionary:
                    for result in self.find(key, d):
                        yield result


    def get_images_from_hashtag_page(self,hashtag="nightsky", scroll_page=3):
        hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
        next_page_url = ""
        goto_next_page = True
        responses = []

        while goto_next_page and scroll_page > 0:
            complete_url = hashtag_url+next_page_url
            response = self.cr.get(complete_url, headers=self.h, parser='json')

            page_info = response['graphql']['hashtag']["edge_hashtag_to_media"]["page_info"]
            if page_info["has_next_page"]:
                end_cursor = page_info["end_cursor"]
                next_page_url = "&max_id={}".format(end_cursor)
            else:
                goto_next_page = False
                
            for i in range(len(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'])):
                name = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode']
                link = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['thumbnail_resources'][-1]['src']
                date = str(datetime.fromtimestamp(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['taken_at_timestamp']).date())
                responses.append((date,link,name+str(scroll_page)))

            scroll_page = scroll_page - 1
            time.sleep(random.randint(10,20))
        return responses

