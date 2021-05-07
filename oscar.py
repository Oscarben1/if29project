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

for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == "friends_count"):
            #print(key, value)
            indicateurDfFriendsCount[i] = value

print(indicateurDfFriendsCount)

