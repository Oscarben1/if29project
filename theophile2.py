import os

os.chdir('./Tweet Worldcup/raw')
os.getcwd()

import json

import ORM
from sqlalchemy.sql import exists

#fonction permettant de parser l'intégralité des json et de les stocker dans une base de donnée SQlite
def get_tweet_from_json():
    fichier = open("suivi.txt", "a")
    #boucle pour parcourir les fichier json 1 à 1
    for i in range(2278,2286):
        #boucle pour parcourir les lignes et en extraire les tweets
        for line in open('raw'+ str(i) +'.json', 'r', encoding='utf8'):
            tweet_en_cours=json.loads(line)
            id_user = int(tweet_en_cours["user"]['id'])
            name_user = tweet_en_cours["user"]['name']
            friends_count = int(tweet_en_cours["user"]['friends_count'])
            followers_count = int(tweet_en_cours["user"]['followers_count'])
            text = tweet_en_cours["text"]
            #Parcours de la liste des hashtags et concaténation en 1 string
            hashtags = ""
            for item in (tweet_en_cours["entities"]["hashtags"]):
                if hashtags == "":
                    hashtags = item['text']
                else :
                    hashtags+=", " + item['text']
            # Parcours de la liste des urls et concaténation en 1 string
            urls = ""
            for item in (tweet_en_cours["entities"]["urls"]):

                if urls == "":
                    urls = item["url"]
                else:
                    urls += ", " + item["url"]
            user_mentions = len(tweet_en_cours["entities"]["user_mentions"])
            fav = int(tweet_en_cours["user"]['favourites_count'])
            timestamp= tweet_en_cours["timestamp_ms"]
            #stockage dans la db SQlite via l'ORM SQLAlchemy
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
        fichier.write(str(i)+"\n")

#fonction permettant de créer une table pour les utilisateurs grâce aux tweets stockés dans la db
def create_user_table():
    #récupération des tweets dans lb et parcours tweet
    for rows in ORM.session.query(ORM.Tweet):
        print("ok")
        if ORM.session.query(exists().where(ORM.User.id_user == rows.id_user)).scalar():
            pass
        else :
            print("dans la boucle")
            if (rows.friends_count != 0):
                indicateur_ratio = rows.followers_count / rows.friends_count
            else:
                indicateur_ratio = rows.friends_count
            print(indicateur_ratio)
            longueur_text = len(rows.text)
            print(longueur_text)
            liste_tweets_utilisateur = ORM.session.query(ORM.Tweet).filter(ORM.Tweet.id_user==rows.id_user).all()
            print("liste récupérée")
            liste_urls = ""
            liste_hashtags = ""
            nombre_user_mentions = 0
            for tweet in liste_tweets_utilisateur:
                if tweet.urls != "":
                    liste_urls += ", " + tweet.urls
                if tweet.hashtags != "":
                    liste_hashtags += ", " + tweet.hashtags
                nombre_user_mentions+=int(tweet.user_mentions)
            nombre_urls = len(liste_urls.split(', '))
            #aggressivite
            frequenceFriends=0
            frequenceTweet=1
            if len(liste_tweets_utilisateur)>1:
                liste_timestamp=[]
                for tweet in liste_tweets_utilisateur:
                    liste_timestamp.append(tweet.timestamp)
                liste_timestamp.sort()
                difftime=(liste_tweets_utilisateur[len(liste_tweets_utilisateur)-1].timestamp-liste_tweets_utilisateur[0].timestamp)/ float(3600000) + 0.000000000000001
                frequenceTweet= len(liste_tweets_utilisateur)/ difftime
                frequenceFriends = nombre_urls / difftime
            aggressivite = (frequenceFriends + frequenceTweet)/350
            print("aggressivite")
            print(aggressivite)
            sum_hashtags = ""
            #visibilté
            moyLengthHashtags = 11.6
            moyLengthMention = 11.4
            print("liste_hashtags")
            print(liste_hashtags)
            nombre_hashtags = len(liste_hashtags.split(","))
            avg_hashtags = nombre_hashtags/len(liste_tweets_utilisateur)
            avg_user_mentions = nombre_user_mentions / len(liste_tweets_utilisateur)
            visibilite= ((avg_hashtags*moyLengthHashtags) + (avg_user_mentions*moyLengthMention))/140
            print(visibilite)


def load_tweet():
    tab_tweet={}
    compteur=0
    for rows in ORM.session.query(ORM.Tweet):
        tab_tweet[compteur]=rows
        compteur+=1
        if compteur % 10000 ==0:
            print(compteur)



if __name__ == '__main__':
    load_tweet()
