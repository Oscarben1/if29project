import os

os.chdir('./Tweet Worldcup/raw')
os.getcwd()

import json
import pandas as pd
import numpy as np
import ORM
from sqlalchemy.sql import exists
import sqlite3
# Opening JSON file


def get_tweet_from_json():
    tweets = []
    for i in range(2285):
        for line in open('raw'+ str(i) +'.json', 'r', encoding='utf8'):
            tweet_en_cours=json.loads(line)
            id_user = int(tweet_en_cours["user"]['id'])
            name_user = tweet_en_cours["user"]['name']
            friends_count = int(tweet_en_cours["user"]['friends_count'])
            followers_count = int(tweet_en_cours["user"]['followers_count'])
            text = tweet_en_cours["text"]
            #for j in range(len(["entities"]['hashtags']))
            hashtags = ""
            for item in (tweet_en_cours["entities"]["hashtags"]):
                if hashtags=="":
                    hashtags = item['text']
                else :
                    hashtags+=", " + item['text']
            urls = ""
            for item in (tweet_en_cours["entities"]["urls"]):

                if urls == "":
                    urls = item["url"]
                else:
                    urls += ", " + item["url"]
            user_mentions = len(tweet_en_cours["entities"]["user_mentions"])

            fav = int(tweet_en_cours["user"]['favourites_count'])
            timestamp= tweet_en_cours["timestamp_ms"]

            try :

                tweet = ORM.Tweet(
                    id_user=id_user,
                    name_user=name_user,
                    friends_count=friends_count,
                    followers_count=followers_count,
                    text=text,
                    hashtags=hashtags,
                    urls=urls,
                    fav=fav,
                    user_mentions=user_mentions,
                    timestamp=timestamp,
                )
                ORM.session.add(tweet)
                ORM.session.commit()
                ORM.session.flush()
                ORM.session.refresh(tweet)
            except Exception as e:
                print(e)
                print("erreur")
        print(i)


def create_user_table():
    for rows in ORM.session.query(ORM.Tweet):
        print("ok")
        if ORM.session.query(exists().where(ORM.User.id_user == rows.id_user)).scalar():
            pass
        else :
            if (rows.friends_count != 0):
                indicateur_ratio = rows.followers_count / rows.friends_count
            else:
                indicateur_ratio = rows.friends_count
            print(indicateur_ratio)
            longueur_text = len(rows.text)
            print(longueur_text)
            liste_tweets_utilisateur = ORM.session.query(ORM.Tweet).filter(ORM.Tweet.id_user==rows.id_user).all()
            liste_urls = ""
            for tweet in liste_tweets_utilisateur:
                if tweet.urls != "":
                    liste_urls += ", " + tweet.urls
            nombre_tweet = len(liste_urls.split(', '))
            frequenceFriends=0
            frequenceTweet=1
            if len(liste_tweets_utilisateur)>1:
                difftime=(liste_tweets_utilisateur[0].timestamp-liste_tweets_utilisateur[len(liste_tweets_utilisateur)-1].timestamp)/ float(3600000) + 0.000000000000001
                frequenceTweet= len(liste_tweets_utilisateur)/ difftime
                frequenceFriends = nombre_tweet / difftime

            for tweet in liste_tweets_utilisateur:
                if tweet.urls != "":
                    liste_urls += ", " + tweet.urls
            nombre_tweet = len(liste_urls.split(', '))
            aggressivite = (frequenceFriends + frequenceTweet)/350
            print("aggressivite")
            print(aggressivite)





if __name__ == '__main__':
    create_user_table()
