import json
import pandas as pd
import numpy as np

# Opening JSON file
tweets = []
for i in range(2):
  for line in open('data/raw'+ str(i) +'.json', 'r', encoding='utf8'):
      tweets.append(json.loads(line))
#tableau de chaque tweet
df = pd.DataFrame(tweets)

userId = np.array([])

#récupération des id utilisateur
for i in range(len(df)):
    userId = np.append(userId, df.iloc[i, :]['user'].get('id_str'))

print(userId)
print(type(userId))

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


#Récupération des id qui concordent avec les valeurs d'agressivité du np array
indicateurAgressivite = np.array([])
idAgressivitetemp = list(users.keys())
idAgressivite = np.array([])

for i in range(len(idAgressivitetemp)):
    idAgressivite = np.append(idAgressivite, str(idAgressivitetemp[i]))

print(idAgressivite)

for user in users:
    indicateurAgressivite = np.append(indicateurAgressivite, users[user]['agressivité'])

print(indicateurAgressivite)

finalAgressivite = pd.DataFrame()
finalAgressivite['id'] = idAgressivite
finalAgressivite['agressivite'] = indicateurAgressivite
finalAgressivite.set_index('id',  inplace=True)
finalAgressivite.sort_index( inplace=True)

print(finalAgressivite)



#INDICATEURS VERIFIED et Favorites
indicateurDfVerified = np.zeros(len(userdf))
indicateurDfFav = np.zeros(len(userdf))
for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == 'Verified'):
            indicateurDfVerified[i] = value
        elif (key == 'favourites_count'):
            indicateurDfFav[i] = value

# recupération de l'indicateur qui va nous donner si oui ou non le tweet est potentiellement sensible
poss = df['possibly_sensitive']
indicateurDfSensible = poss.to_numpy()

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

print(finalDf.shape)
finalDf = finalDf.groupby(['id']).mean()
print(finalDf.shape)
finalDf.sort_index

finalDf = finalDf.merge(finalAgressivite, on='id')

print(finalDf)