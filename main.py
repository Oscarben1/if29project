import os

os.chdir('C:\\Users\\oscar\\OneDrive\\Bureau\\IF29\\Tweet Worldcup\\raw')
os.getcwd()

import json
import pandas as pd
import numpy as np

# Opening JSON file
tweets = []
for i in range(300):
    for line in open('raw'+ str(i) +'.json', 'r', encoding='utf8'):
        tweets.append(json.loads(line))
    print(i)
#tableau de chaque tweet
df = pd.DataFrame(tweets)

userId = np.array([])
print("chargés")
#récupération des id utilisateur
for i in range(len(df)):
    userId = np.append(userId, df.iloc[i, :]['user'].get('id_str'))

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

print("indicateur ratio ok")
# création du tableau de texte de tweets
tweetsText = np.array([],dtype = 'object')

for i in range(len(df)):
   tweetsText = np.append(tweetsText,"")
# récupération de la colonne texte dans dfText
dfText = df['text']

#stockage du texte uniquement dans tweetsText
for i in range(len(df)):
    tweetsText[i] = dfText[i]

# création d'un tableau vide =0 de la longueur de df
indicateurDfLongueurTweets = np.zeros(len(df))
#stockage de la longueur du text dans tweetsText dans indicateurDfLongueurTweets
print("longueur des textes")
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

print("Parcours des utilisateurs fini pour agressivite")

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
print("agressivité terminé")
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

print("variable visibilité finie")
#Récupération des id qui concordent avec les valeurs d'agressivité du np array
indicateurAgressivite = np.array([])
idAgressivitetemp = list(users.keys())
idAgressivite = np.array([])

for i in range(len(idAgressivitetemp)):
    idAgressivite = np.append(idAgressivite, str(idAgressivitetemp[i]))

for user in users:
    indicateurAgressivite = np.append(indicateurAgressivite, users[user]['agressivité'])

finalAgressivite = pd.DataFrame()
finalAgressivite['id'] = idAgressivite
finalAgressivite['agressivite'] = indicateurAgressivite
finalAgressivite.set_index('id',  inplace=True)
finalAgressivite.sort_index( inplace=True)


#Récupération des id qui concordent avec les valeurs de visibilité du np array
indicateurVisibilite = np.array([])
idVisibilitetemp = list(users.keys())
idVisibilite = np.array([])

for i in range(len(idVisibilitetemp)):
    idVisibilite = np.append(idVisibilite, str(idVisibilitetemp[i]))

for user in users:
    indicateurVisibilite = np.append(indicateurVisibilite, usersVis[user]['visibilité'])
print("id recupérés pour ag et vis")
finalVisibilite = pd.DataFrame()
finalVisibilite['id'] = idVisibilite
finalVisibilite['visibilite'] = indicateurVisibilite
finalVisibilite.set_index('id',  inplace=True)
finalVisibilite.sort_index( inplace=True)


#INDICATEUR Favourites
indicateurDfFav = np.zeros(len(userdf))
for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == 'favourites_count'):
            indicateurDfFav[i] = value
'''
# recupération de l'indicateur qui va nous donner si oui ou non le tweet est potentiellement sensible
poss = df['possibly_sensitive']
indicateurDfSensible = poss.to_numpy()
'''
finalDf = pd.DataFrame()

finalDf['id'] = userId
finalDf['friends_count'] = indicateurDfFriendsCount
finalDf['followers_count'] = indicateurDfFollowersCount
finalDf['ratio'] = indicateurDfRatio
finalDf['tweetLength'] = indicateurDfLongueurTweets
finalDf['hashtags'] = indicateurNbHashtags
finalDf['URLs'] = indicateurNbURLs
#finalDf['sensible'] = indicateurDfSensible
#finalDf['verified'] = indicateurDfVerified
finalDf['fav'] = indicateurDfFav


finalDf = finalDf.groupby(['id']).mean()
finalDf.sort_index

finalDf = finalDf.merge(finalAgressivite, on='id')
finalDf = finalDf.merge(finalVisibilite, on='id')

finalDf.to_csv('C:\\Users\\oscar\\OneDrive\\Bureau\\IF29\\finalDF.csv', encoding='utf-8')