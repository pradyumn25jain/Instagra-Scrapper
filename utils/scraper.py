import time
import random
from datetime import datetime
import json
from utils.customrequests import Custom_Requests
import re


class Scraper:
    def __init__(self) -> None:
        self.sessionid = '1477942758%3AMPFy11IRHfBL2d%3A18'
        # self.h = {'Accept-Language':'en-US,en;q=0.5',"Cookie":"sessionid={}".format(self.sessionid)}
        self.h = {'Accept-Language':'en-US,en;q=0.5'}
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

    def loadJson(self,a):
        try:
            return json.loads(a)
        except:
            return []

    def get_images_from_hashtag_page3(self,hashtag="nightsky", scroll_page=3):
        hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
        next_page_url = ""
        responses = []

        while scroll_page > 0:
            complete_url = hashtag_url+next_page_url
            response = self.cr.get(complete_url, headers=self.h, parser='None')
            try:
                response =  json.loads(response)
                next_page_url = "&max_id={}".format(response['graphql']['hashtag']["edge_hashtag_to_media"]["page_info"]["end_cursor"])
                try:
                    for i in range(len(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'])):
                        name = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode']
                        link = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['thumbnail_resources'][-1]['src']
                        date = str(datetime.fromtimestamp(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['taken_at_timestamp']).date())
                        responses.append((date,link,name+str(scroll_page)))
                except:
                    pass
            except:
                try:
                    print("skipped ",scroll_page)
                    try:
                        rx = r'(\{[^{}]+\})'
                        matches = re.findall(rx, response)
                    except:
                        response = response.decode('utf-8')
                        rx = r'(\{[^{}]+\})'
                        matches = re.findall(rx, response)

                    matches = [self.loadJson(a) for a in matches]
                    next_page_url = "&max_id={}".format(matches[0]['end_cursor'])
                except:
                    return response,responses
            scroll_page = scroll_page - 1
            time.sleep(random.randint(10,25))
        return responses


    # def get_images_from_hashtag_page2(self,hashtag="nightsky", scroll_page=3):
    #     hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
    #     next_page_url = ""
    #     goto_next_page = True
    #     responses = []

    #     while goto_next_page and scroll_page > 0:
    #         complete_url = hashtag_url+next_page_url
    #         try:
    #             response = self.cr.get(complete_url, headers=self.h, parser='None')
    #             response =  json.loads(response)
    #             page_info = response['graphql']['hashtag']["edge_hashtag_to_media"]["page_info"]
    #         except: 
    #             page_info 
    #             return responses

    #         page_info = response['graphql']['hashtag']["edge_hashtag_to_media"]["page_info"]
    #         if page_info["has_next_page"]:
    #             end_cursor = page_info["end_cursor"]
    #             next_page_url = "&max_id={}".format(end_cursor)
    #         else:
    #             goto_next_page = False
    #         try:       
    #             for i in range(len(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'])):
    #                 name = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['shortcode']
    #                 link = response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['thumbnail_resources'][-1]['src']
    #                 date = str(datetime.fromtimestamp(response['graphql']['hashtag']['edge_hashtag_to_media']['edges'][i]['node']['taken_at_timestamp']).date())
    #                 responses.append((date,link,name+str(scroll_page)))

    #             scroll_page = scroll_page - 1
    #             time.sleep(random.randint(10,20))
    #         except:
    #             scroll_page = scroll_page - 1
    #             time.sleep(random.randint(10,20))
    #     return responses


    # def get_images_from_hashtag_page(self,hashtag="toonapp", scroll_page=3):
    #     hashtag_url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
    #     next_page_url = ""
    #     responses = []

    #     while scroll_page > 0:
    #         complete_url = hashtag_url+next_page_url
    #         response = self.cr.get(complete_url, headers=self.h, parser='json')
    #         return response

    #         try:
    #             end_cursor = response['data']['recent']['next_max_id']
    #             next_page_url = "&max_id={}".format(end_cursor)
    #         except:
    #             return responses

    #         for section in range(len(response['data']['recent']['sections'])):
    #             for media in range(len(response['data']['recent']['sections'][section]['layout_content']['medias'])):
    #                 try:
    #                     # link 
    #                     link = response['data']['recent']['sections'][section]['layout_content']['medias'][media]['media']['image_versions2']['candidates'][0]['url']
    #                     # date
    #                     date = str(datetime.fromtimestamp(response['data']['recent']['sections'][section]['layout_content']['medias'][media]['media']['taken_at']).date())
    #                     # name 
    #                     name = response['data']['recent']['sections'][section]['layout_content']['medias'][media]['media']['id']
    #                     responses.append((date,link,name))
    #                 except:
    #                     continue
    #         scroll_page = scroll_page - 1
    #         time.sleep(random.randint(5,15))
    #     return responses


