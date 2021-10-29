import scrapy
import re
import json
from copy import deepcopy
from urllib.parse import urlencode
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem


class InstaSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'procentiro'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1635502056:AUlQAAHDTfzNSMrt/OfzNlObPAxG7FdWJneRgjBRn9rIyRNGJ97ZS5AbMamTFFwAo2vKDNe29vhzCOhvi/uEXv8mkSDeJ5E/hMNY1ow8XzmpeTEfn4LJ3+Z1NFTwOAz2tTn3oEzttkHUZ5iYhzT3K6ABYQ=='
    user_for_parse = 'nina.k_chimera'


    def parse(self, response: HtmlResponse):
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login,
                      'enc_password': self.inst_pwd,
                      'X-IG-App-ID': '936619743392459',
                      'X-IG-WWW-Claim': 'hmac.AR08mGMWEKvDF_NFMZjpWTKY5hQERjPKiLqJSZR48Javh2lM'},
            headers={'x-csrftoken': csrf}
        )

    def login(self, response: HtmlResponse):
        print()
        j_data = response.json()
        if j_data['authenticated']:
            yield response.follow(
                f'/{self.user_for_parse}',
                callback=self.user_parse,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)

        variables = {'count': 12}
        url_posts = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/'

        yield response.follow(url_posts,
                              callback=self.user_posts_parse,
                              headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
                                       'X-IG-App-ID':'936619743392459'
                                       },
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)
                                         }
                              )


    def user_posts_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        # print(len(j_data['users']))
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            variables['search_surface'] = 'follow_list_page'
            url_posts = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
            # print(url_posts)
            yield response.follow(url_posts,
                                  callback=self.user_posts_parse,
                                  headers={
                                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
                                      'X-IG-App-ID': '936619743392459'
                                      },
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)}
                                  )
            followers = j_data.get('users')
            for follower in followers:
                item = InstaparserItem(
                    user_id=user_id,
                    username=username,
                    follower_username=follower['username'],
                    full_name=follower['full_name'],
                    is_private=follower['is_private']
                )
                yield item


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
