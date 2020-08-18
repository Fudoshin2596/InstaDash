import json
import datetime
import requests
from APIBuilder import *


# ---------------------------INSTAGRAM USER CLASS---------------------------- #


class InstaUser():
    def __init__(self, debug):
        self.params = getCreds()  # get creds
        self.params['debug'] = debug  # set debug

    def getUserPages(self):
        """ Get facebook pages for a user
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['access_token'] = self.params['access_token']  # access token

        url = self.params['endpoint_base'] + 'me/accounts'  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def get_pageid(self):
        response = self.getUserPages()
        print("\n---- FACEBOOK PAGE INFO ----\n") # section heading
        print("Page Name:") # label
        print(response['json_data']['data'][0]['name']) # display name
        print("\nPage Category:") # label
        print(response['json_data']['data'][0]['category']) # display category
        print("\nPage Id:") # label
        print(response['json_data']['data'][0]['id']) # display id
        return response['json_data']['data'][0]['id']

    def getInstagramAccount(self):
        """ Get instagram account
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['access_token'] = self.params['access_token']  # tell facebook we want to exchange token
        endpointParams['fields'] = 'instagram_business_account'  # access token

        url = self.params['endpoint_base'] + self.params['page_id']  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def getAccountInfo(self):
        """ Get info on a users account
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields=business_discovery.username({ig-username}){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}&access_token={access-token}
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['fields'] = 'business_discovery.username(' + self.params['ig_username'] + '){username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}'  # string of fields to get back with the request for the account
        endpointParams['access_token'] = self.params['access_token']  # access token

        url = self.params['endpoint_base'] + self.params['instagram_account_id']  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def getUserMedia(self):
        """ Get users media
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username'  # fields to get back
        endpointParams['access_token'] = self.params['access_token']  # access token

        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/media'  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def setUMParam(self):
        response = self.getUserMedia()
        self.params['latest_media_id'] = response['json_data']['data'][0]['id']  # store latest post id
        if 'VIDEO' == response['json_data']['data'][0]['media_type']:  # media is a video
            self.params['metric'] = 'engagement,impressions,reach,saved,video_views'
        else:  # media is an image
            self.params['metric'] = 'engagement,impressions,reach,saved'

    def getAllPosts(self):
        response = self.getUserMedia()
        dic_of_posts = {}
        for num, post in enumerate(response['json_data']['data']):
            self.params[f'media{num}_id'] = post['id']
            dic_of_posts[f'media{num}_id'] = post['id']
            if 'VIDEO' == post['media_type']:  # media is a video
                self.params['metric'] = 'engagement,impressions,reach,saved,video_views'
            else:  # media is an image
                self.params['metric'] = 'engagement,impressions,reach,saved'
        return dic_of_posts

    def getMediaInsights(self, post_num=0):
        """ Get insights for a specific media id
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['metric'] = self.params['metric']  # fields to get back
        endpointParams['access_token'] = self.params['access_token']  # access token

        if post_num > 0:
            url = self.params['endpoint_base'] + self.params[f'media{post_num}_id'] + '/insights'  # endpoint url
        else:
            url = self.params['endpoint_base'] + self.params['latest_media_id'] + '/insights'  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def ViewMediaInsights(self):
        response = self.getMediaInsights()  # get insights for a specific media id
        for insight in response['json_data']['data']:  # loop over post insights
            print("\t" + insight['title'] + " (" + insight['period'] + "): " + str(insight['values'][0]['value']))  # display info

    def getUserInsights(self):
        """ Get insights for a users account
        API Endpoint:
            https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}
        Returns:
            object: data from the endpoint
        """
        endpointParams = dict()  # parameter to send to the endpoint
        endpointParams['metric'] = 'follower_count,impressions,profile_views,reach'  # fields to get back
        endpointParams['period'] = 'day'  # period
        endpointParams['access_token'] = self.params['access_token']  # access token

        url = self.params['endpoint_base'] + self.params['instagram_account_id'] + '/insights'  # endpoint url

        return makeApiCall(url, endpointParams, self.params['debug'])  # make the api call

    def ViewUserInsights(self):
        response = self.getUserInsights()  # get insights for a user
        for insight in response['json_data']['data']:  # loop over user account insights
            print("\t" + insight['title'] + " (" + insight['period'] + "): " + str(insight['values'][0]['value']))  # display info

            for value in insight['values']:  # loop over each value
                print("\t\t" + value['end_time'] + ": " + str(value['value']))  # print out counts for the date

    def ViewUser(self):
        account_info = self.getAccountInfo()
        username = account_info['json_data']['business_discovery']['username']  # display username
        try:
            website = account_info['json_data']['business_discovery']['website']  # display users website
            profile_picture_url = account_info['json_data']['business_discovery']['profile_picture_url']  # display profile picutre url
            user_biography = account_info['json_data']['business_discovery']['biography']  # display users about section
        except KeyError:
            website = "n/a"
            profile_picture_url = "n/a"
            user_biography = "n/a"
        num_posts = account_info['json_data']['business_discovery']['media_count']  # display number of posts user has made
        followers = account_info['json_data']['business_discovery']['followers_count']  # display number of followers the user has
        following = account_info['json_data']['business_discovery']['follows_count']  # display number of people the user follows

        insta_account_info = self.getInstagramAccount()
        page_id = insta_account_info['json_data']['id']  # display the page id
        insta_biz_acc = insta_account_info['json_data']['instagram_business_account']['id']  # display the instagram account id

        user_page_info = self.getUserPages()
        page_name = user_page_info['json_data']['data'][0]['name']  # display name
        page_category = user_page_info['json_data']['data'][0]['category']  # display category

        user_media_info = self.getUserMedia()  # get users media from the api
        post_link = user_media_info['json_data']['data'][0]['permalink']  # link to post
        try:
            post_caption = user_media_info['json_data']['data'][0]['caption']  # post caption
        except KeyError:
            post_caption = "n/a"
        media_type = user_media_info['json_data']['data'][0]['media_type']  # type of media
        posted_date = user_media_info['json_data']['data'][0]['timestamp']  # when it was posted

        all_post_id = self.getAllPosts()

        all_media_insights = {}
        for i in range(len(self.getAllPosts())):
            media_insight_info = self.getMediaInsights(post_num=i)  # get insights for a specific media id
            all_media_insights[f'media_insight_{i}'] = {str(k['title'] + " (" + k['period'] + ")"): int(v['values'][0]['value']) for k in media_insight_info['json_data']['data'] for v in media_insight_info['json_data']['data']}   # loop over post insights
            all_media_insights[f'media_insight_{i}']['link'] = user_media_info['json_data']['data'][i]['permalink']
            all_media_insights[f'media_insight_{i}']['media_type'] = user_media_info['json_data']['data'][i]['media_type']
            all_media_insights[f'media_insight_{i}']['posted_date'] = user_media_info['json_data']['data'][i]['timestamp']
            try:
                all_media_insights[f'media_insight_{i}']['caption'] = user_media_info['json_data']['data'][i]['caption']
            except KeyError:
                all_media_insights[f'media_insight_{i}']['caption'] = "n/a"

        user_insight_info = self.getUserInsights()  # get insights for a user
        user_insight = {str(k['title'] + " (" + k['period'] + ")"): int(v['values'][0]['value']) for k in user_insight_info['json_data']['data'] for v in user_insight_info['json_data']['data']}    # display info
        # for value in insight['values']:  # loop over each value
        #     stat2 = str(value['end_time'] + ": " + str(value['value']))  # print out counts for the date
        #     user_insight.append([stat1, stat2])

        return username, website, num_posts, followers, following, profile_picture_url, user_biography, page_id, insta_biz_acc, page_name, page_category, post_link, post_caption, media_type, posted_date, all_post_id, all_media_insights, user_insight


# ---------------------------INSTAGRAM USER --------------------------------- #

def gather_insta_data(debug='no'):
    User = InstaUser(debug)
    User.setUMParam()
    username, website, num_posts, followers, following, profile_picture_url, user_biography, page_id, insta_biz_acc, page_name, page_category, post_link, post_caption, media_type, posted_date, all_post_id, all_media_insights, user_insight = User.ViewUser()

    return username, website, num_posts, followers, following, profile_picture_url, user_biography, page_id, insta_biz_acc, page_name, page_category, post_link, post_caption, media_type, posted_date, all_post_id, all_media_insights, user_insight
