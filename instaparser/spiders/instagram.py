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
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1635581843:AaZQAHEopegV7Bm9Y+QVCPt/vYfiZG5HqgPwj1jjEl9fyEo3ffhfJUh+6ezzdqCUOlveIKIdwqG0hdZ14GCCl4X2SBEws9NddgfKBQVB01LFG9SngsGiTiszXKTZ6gr+J5H4QxdhEStok8q7FIVF5JYigw=='
    user_for_parse = 'irena275'

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
        j_data = response.json()
        if j_data['authenticated']:
            print('залогинились')
            yield response.follow(
                f'/{self.user_for_parse}',
                callback=self.user_parse,
                cb_kwargs={'username': self.user_for_parse}
            )

    def user_parse(self, response: HtmlResponse, username):
        print(f'зашли на страницу исследуемого "{username}"')
        user_id = self.fetch_user_id(response.text, username)
        variables = {'count': 12}
        url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
        url_followings = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'

        yield response.follow(url_followers,
                              callback=self.follower_list_parse,
                              headers={
                                  'User-Agent': 'Instagram 155.0.0.37.107',
                                  'X-IG-App-ID': '936619743392459'
                                  },
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)
                                         }
                              )
        yield response.follow(url_followings,
                              callback=self.following_list_parse,
                              headers={
                                  'User-Agent': 'Instagram 155.0.0.37.107',
                                  'X-IG-App-ID': '936619743392459'
                              },
                              cb_kwargs={'username': username,
                                         'user_id': user_id,
                                         'variables': deepcopy(variables)
                                         }
                              )

    def follower_list_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            variables['search_surface'] = 'follow_list_page'
            url_followers = f'https://i.instagram.com/api/v1/friendships/{user_id}/followers/?{urlencode(variables)}'
            yield response.follow(url_followers,
                                  callback=self.follower_list_parse,
                                  headers={
                                      'User-Agent': 'Instagram 155.0.0.37.107',
                                      'X-IG-App-ID': '936619743392459'
                                  },
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)}
                                  )
            followers = j_data.get('users')
            print(f'получена пачка подписчиков {username}: {len(followers)} шт.')
            for follower in followers:
                if follower['is_private'] == False:
                    yield response.follow(
                        f"/{follower['username']}",
                        callback=self.user_page_parse,
                        cb_kwargs={'username': username, 'is_follower': True}
                    )

    def following_list_parse(self, response: HtmlResponse, username, user_id, variables):
        j_data = response.json()
        if j_data.get('next_max_id'):
            variables['max_id'] = j_data.get('next_max_id')
            url_followings = f'https://i.instagram.com/api/v1/friendships/{user_id}/following/?{urlencode(variables)}'
            yield response.follow(url_followings,
                                  callback=self.following_list_parse,
                                  headers={
                                      'User-Agent': 'Instagram 155.0.0.37.107',
                                      'X-IG-App-ID': '936619743392459'
                                  },
                                  cb_kwargs={'username': username,
                                             'user_id': user_id,
                                             'variables': deepcopy(variables)}
                                  )
            followings = j_data.get('users')
            print(f'получена пачка подписок {username}: {len(followings)} шт.')
            for following in followings:
                if following['is_private'] == False:
                    yield response.follow(
                        f"/{following['username']}",
                        callback=self.user_page_parse,
                        cb_kwargs={'username': username, 'is_follower': False}
                    )

    def user_page_parse(self, response: HtmlResponse, username, is_follower):
        # из HTML страницы юзера инсты получаем кусок JSON, поскольку не получается загрузить json напрямую через response.json()
        # x = response.xpath("//script[starts-with(.,'window._sharedData')]/text()").extract_first()
        x = response.xpath("//script[starts-with(.,'window._sharedData =')]/text()").extract_first()
        json_string = x.strip().split('= ')[1][:-1]
        try:
            data = json.loads(json_string)
            # теперь обрабатываем данные
            user_data = data['entry_data']['ProfilePage'][0]['graphql']['user']
            if is_follower:
                print(f"парсим подписчика {user_data['username']}")
            else:
                print(f"парсим подписку {user_data['username']}")
            posts = user_data['edge_owner_to_timeline_media']['edges']
            non_video_post_count = 0
            posts_like_count = 0
            posts_comment_count = 0
            posts_text = []
            if posts:
                for post in posts:
                    if post['node']['is_video'] == False:
                        non_video_post_count += 1
                        try:
                            post_text = post['node']['edge_media_to_caption']['edges'][0]['node']['text']
                        except:
                            post_text = ''
                        posts_text.append(post_text)
                        post_like_count = post['node']['edge_liked_by']['count']
                        posts_like_count += post_like_count
                        post_comment_count = post['node']['edge_media_to_comment']['count']
                        posts_comment_count += post_comment_count

            item = InstaparserItem(
                username=username,
                is_follower=is_follower,
                _id=user_data['id'],
                follower_or_following=user_data['username'],
                full_name=user_data['full_name'],
                biography=user_data['biography'],
                followers_count=user_data['edge_followed_by']['count'],
                following_count=user_data['edge_follow']['count'],
                first_page_posts_count=len(posts),
                posts_count=user_data['edge_owner_to_timeline_media']['count'],
                posts_text=posts_text,
                non_video_post_count=non_video_post_count,
                posts_like_count=posts_like_count,
                posts_comment_count=posts_comment_count,
                photo=user_data['profile_pic_url_hd']
            )
            # pprint(item)
            return item
        except:
            err_url = response.url
            print(f"не удалось спарсить {err_url}")
            # save failed url in file for later parse
            # self.write_json(err_url)


    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')

    # function to add to JSON
    def write_json(self, new_data, filename='data.json'):
        with open(filename, 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
