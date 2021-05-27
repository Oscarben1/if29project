import os

os.chdir('C:\\Users\\oscar\\OneDrive\\Bureau\\IF29\\Tweet Worldcup\\raw')
os.getcwd()

import json
import pandas as pd
import numpy as np

# Opening JSON file
tweets = []
for i in range(20):
  for line in open('raw'+ str(i) +'.json', 'r', encoding='utf8'):
      tweets.append(json.loads(line))

df = pd.DataFrame(tweets)
print(df.head())
print(df.describe())
#Creation de l'indicateur de followers et abonnements et du ratio
userdf = df['user']
indicateurDfFriendsCount = np.zeros(len(userdf))
indicateurDfFollowersCount = np.zeros(len(userdf))
indicateurDfRatio = np.zeros(len(userdf))

for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == "friends_count"):
            #print(key, value)
            indicateurDfFriendsCount[i] = value
        elif (key == "followers_count"):
            indicateurDfFollowersCount[i] = value

for i in range(len(indicateurDfFollowersCount)):
    if (indicateurDfFriendsCount[i] != 0):
        indicateurDfRatio[i] = indicateurDfFollowersCount[i] / indicateurDfFriendsCount[i]
    else:
        indicateurDfRatio[i] = indicateurDfFollowersCount[i]

tweetsText = np.array([])

for i in range(len(df)):
   tweetsText = np.append(tweetsText, "")

dfText = df['text']

for i in range(len(df)):
    tweetsText[i] = dfText[i]

indicateurDfLongueurTweets = np.zeros(len(df))

for i in range(len(df)):
    indicateurDfLongueurTweets[i] = len(tweetsText[i])

#Création de l'indicateur nombre de hahtag
entitiesdf = df['entities']
indicateurNbHashtags = np.zeros(len(userdf))

for i in range(len(entitiesdf)):
    indicateurNbHashtags[i] = len(entitiesdf[i]['hashtags'])

#Création de l'indicateur nombre de URLs
indicateurNbURLs = np.zeros(len(userdf))
for i in range(len(entitiesdf)):
    indicateurNbURLs[i] = len(entitiesdf[i]['urls'])

#Aggressiveness
# "users" stockera les données nécessaire au calcul de l'agressivité pour chaque profile
users = {}
# On execute la requête et pour chacun des tweets, on conserve les données qui nous intéressent
for i in range(len(df)):
    # Si l'utilisateur n'a pas encore été rencontré, on l'ajoute à notre dictionnaire users
    if df.iloc[i, :]['user'].get('id') not in users:
        users[df.iloc[i, :]['user'].get('id')] = {}
        users[df.iloc[i, :]['user'].get('id')]['timestamp'] = []
        users[df.iloc[i, :]['user'].get('id')]['outgoinglinks'] = []
        users[df.iloc[i, :]['user'].get('id')]['outgoinglinks'].append(len(df.iloc[i, :]['entities'].get('urls')))
        users[df.iloc[i, :]['user'].get('id')]['timestamp'].append(int(df.iloc[i, :]['timestamp_ms']))

    # Sinon on ajoute l'id d'utilisateur au dictionnaire users
    else:
        users[df.iloc[i, :]['user'].get('id')]['timestamp'].append(int(df.iloc[i, :]['timestamp_ms']))
        users[df.iloc[i, :]['user'].get('id')]['outgoinglinks'].append(len(df.iloc[i, :]['entities'].get('urls')))

print("Parcours des utilisateurs fini")

# On détermine l'agressivité de chacun des profiles
for user in users:
    users[user].get('timestamp').sort(reverse=True)
    timestamp = users[user].get('timestamp')
    users[user].get('outgoinglinks').sort(reverse=True)
    outgoinglinks = users[user].get('outgoinglinks')
    users[user]['frequenceTweet'] = 1
    users[user]['frequenceFriends'] = 0
    nbOutgoingLinks = 0
    # S'il y a plus d'un tweet de retenu, on additionne les écarts entre chaque tweet
    if len(timestamp) > 1:
        diffTime = timestamp[0] - timestamp[len(timestamp) - 1]
        # On convertit le temps en h
        diffTime = diffTime / float(3600000) + 0.000000000000001
        users[user]['frequenceTweet'] = len(timestamp) / diffTime
        for i in range(len(outgoinglinks)):
            nbOutgoingLinks += outgoinglinks[i]
        users[user]['frequenceFriends'] = nbOutgoingLinks / diffTime

    users[user]['agressivité'] = (users[user]['frequenceFriends'] + users[user]['frequenceTweet']) / 350


indicateurAgressivite = np.array([])

for user in users:
    indicateurAgressivite = np.append(indicateurAgressivite, users[user]['agressivité'])

print(indicateurAgressivite)

#VISIBILITY
moyLengthHashtags = 11.6
moyLengthMention = 11.4

# "usersVis" stockera les données nécessaire au calcul de l'agressivité pour chaque profile
usersVis = {}
# On execute la requête et pour chacun des tweets, on conserve les données qui nous intéressent
for i in range(len(df)):
    # Si l'utilisateur n'a pas encore été rencontré, on l'ajoute à notre dictionnaire users
    if df.iloc[i, :]['user'].get('id') not in usersVis:
        usersVis[df.iloc[i, :]['user'].get('id')] = {}
        usersVis[df.iloc[i, :]['user'].get('id')]['hashtags'] = []
        usersVis[df.iloc[i, :]['user'].get('id')]['user_mentions'] = []
        usersVis[df.iloc[i, :]['user'].get('id')]['user_mentions'].append(len(df.iloc[i, :]['entities'].get('user_mentions')))
        usersVis[df.iloc[i, :]['user'].get('id')]['hashtags'].append(len(df.iloc[i, :]['entities'].get('hashtags')))

    # Sinon on ajoute l'id d'utilisateur au dictionnaire users
    else:
        usersVis[df.iloc[i, :]['user'].get('id')]['hashtags'].append(len(df.iloc[i, :]['entities'].get('hashtags')))
        usersVis[df.iloc[i, :]['user'].get('id')]['user_mentions'].append(len(df.iloc[i, :]['entities'].get('user_mentions')))

print("Parcours des utilisateurs fini pour visibilité")

for user in usersVis:
    nbTotalHashtags = usersVis[user].get('hashtags')
    nbTotalUser_mentions = usersVis[user].get('user_mentions')
    avgHashtags = sum(nbTotalHashtags) / len(nbTotalHashtags)
    avgUser_mentions = sum(nbTotalUser_mentions) / len(nbTotalUser_mentions)
    visibilité = ((avgHashtags * moyLengthHashtags) + (avgUser_mentions * moyLengthMention)) / 140
    usersVis[user]['visibilité'] = visibilité

