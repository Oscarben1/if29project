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


print(df.head())
print(df.describe())
userdf = df['user']
indicateurDfFriendsCount = np.zeros(len(userdf))
indicateurDfFollowersCount = np.zeros(len(userdf))
indicateurDfRatio = np.zeros(len(userdf))

# parse du nombre d'amis et du nombre de followers
for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == "friends_count"):
            #print(key, value)
            indicateurDfFriendsCount[i] = value
        elif (key == "followers_count"):
            indicateurDfFollowersCount[i] = value

# ratio entre les deux
for i in range(len(indicateurDfFollowersCount)):
    if (indicateurDfFriendsCount[i] != 0):
        indicateurDfRatio[i] = indicateurDfFollowersCount[i] / indicateurDfFriendsCount[i]
    else:
        indicateurDfRatio[i] = indicateurDfFollowersCount[i]

print(indicateurDfRatio)

# création du tableau de texte de tweets
tweetsText = np.array([],dtype = 'object')

for i in range(len(df)):
   tweetsText = np.append(tweetsText,"")
# récupération de la colonne texte dans dfText
dfText = df['text']

#stockage du texte uniquement dans tweetsText
for i in range(len(df)):
    tweetsText[i] = dfText[i]
    print(tweetsText[i])
# création d'un tableau vide =0 de la longueur de df
indicateurDfLongueurTweets = np.zeros(len(df))
#stockage de la longueur du text dans tweetsText dans indicateurDfLongueurTweets
print("longueur des textes")
for i in range(len(df)):
    indicateurDfLongueurTweets[i] = len(tweetsText[i])
    print(len(tweetsText[i]))

# création d'un tableau selon
entitiesdf = df['entities']
indicateurNbHashtags = np.zeros(len(userdf))

for i in range(len(entitiesdf)):
    indicateurNbHashtags[i] = len(entitiesdf[i]['hashtags'])

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

print("agressivités \n" )
print(indicateurAgressivite)
