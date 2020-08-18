from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base


class User(Base):
    '''User instagram global information'''
    __tablename__ = 'User'
    username = Column(String(100), primary_key=True)
    website = Column(String(200))
    num_posts = Column(Integer)
    followers = Column(Integer)
    following = Column(Integer)

    followers_today = Column(Integer)
    impressions_today = Column(Integer)
    views_today = Column(Integer)
    reach_today = Column(Integer)

    def __init__(self, username, website, num_posts, followers, following, followers_today, impressions_today, views_today, reach_today):
        self.username = username
        self.website = website
        self.num_posts = num_posts
        self.followers = followers
        self.following = following
        self.followers_today = followers_today
        self.impressions_today = impressions_today
        self.views_today = views_today
        self.reach_today = reach_today


class UserPosts(Base):
    '''All of the users instagram posts' basic insights'''
    __tablename__ = 'User_Posts'
    post_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String(100))
    link = Column(String(200))
    caption = Column(String(200))
    media_type = Column(String(200))
    time_posted = Column(Date)

    engagement = Column(Integer)
    impressions = Column(Integer)
    reach = Column(Integer)
    saved = Column(Integer)

    def __init__(self, username, link, caption, media_type, time_posted, engagement, impressions, reach, saved):
        # self.post_id = post_id
        self.username = username
        self.link = link
        self.caption = caption
        self.media_type = media_type
        self.time_posted = time_posted
        self.engagement = engagement
        self.impressions = impressions
        self.reach = reach
        self.saved = saved
