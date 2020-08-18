import datetime
from models import *
from models.IGGraphAPI import *
from app import models
from app.database import SessionLocal, engine
from sqlalchemy import exists

username, website, num_posts, followers, following, profile_picture_url, user_biography, page_id, insta_biz_acc, page_name, page_category, post_link, post_caption, media_type, posted_date, all_post_id, all_media_insights, user_insight = gather_insta_data()

#
# for i, post in all_media_insights.items():
#     print(post)

db = SessionLocal()

models.Base.metadata.create_all(bind=engine)

(ret, ), = db.query(exists().where(models.User.username==username))
if ret:
    pass
else:
    db_record1 = models.User(username=username,
                    website=website,
                    num_posts=num_posts,
                    followers=followers,
                    following=following,
                    followers_today=user_insight['Follower Count (day)'],
                    impressions_today=user_insight['Impressions (day)'],
                    views_today=user_insight['Profile Views (day)'],
                    reach_today=user_insight['Reach (day)']
                    )
    db.add(db_record1)

idx = db.query(models.UserPosts).order_by(models.UserPosts.post_id.desc()).first().post_id  # start adding post from the last one
for i, post in all_media_insights.items():
    (ret, ), = db.query(exists().where(models.UserPosts.link==post['link']))
    if ret:
        pass
    else:
        db_record2 = models.UserPosts(username=username,
                    link=post['link'],
                    caption=post['caption'],
                    media_type=post['media_type'],
                    time_posted=post['posted_date'],
                    engagement= post['Engagement (lifetime)'],
                    impressions=post['Impressions (lifetime)'],
                    reach=post['Reach (lifetime)'],
                    saved=post['Saved (lifetime)']
                    )
        db.add(db_record2)
    idx+=1

db.commit()
db.close()
