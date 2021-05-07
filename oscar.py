import json
import pandas as pd
import numpy as np

# Opening JSON file
tweets = []
for i in range(2):
  for line in open('data/raw'+ str(i) +'.json', 'r', encoding='utf8'):
      tweets.append(json.loads(line))

df = pd.DataFrame(tweets)

print(df.head())
print(df.describe())
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

print(indicateurDfRatio)

tweetsText = np.array([])

for i in range(len(df)):
   tweetsText = np.append(tweetsText, "")

dfText = df['text']

for i in range(len(df)):
    tweetsText[i] = dfText[i]

indicateurDfLongueurTweets = np.zeros(len(df))
for i in range(len(df)):
    indicateurDfLongueurTweets[i] = len(tweetsText[i])

print(indicateurDfLongueurTweets)