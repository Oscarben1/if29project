import os 

os.chdir('C:\\Users\\bilal\\Projetif29\\raw')
os.getcwd()

import json
import pandas as pd
import numpy as np

tweets = []


for i in range(5):
  for line in open('raw'+ str(i) +'.json', 'r', encoding='utf8'):
      tweets.append(json.loads(line))

df = pd.DataFrame(tweets)

# récupération de l'indicateur qui donne si oui ou non le compte est verifié + les fav
userdf = df['user']
quotedf = df['quoted_status']

indicateurDfVerified = np.zeros(len(userdf))
indicateurDfFav = np.zeros(len(userdf))
for i in range(len(userdf)):
    for key, value in userdf[i].items():
        if (key == 'Verified'):
            indicateurDfVerified[i] = value
        elif (key == 'favourites_count'):
            indicateurDfFav[i] = value
            
#recupération de l'indicateur qui va nous donner si oui ou non le tweet est potentiellement sensible           
poss = df['possibly_sensitive']

indicateurDfSensible = poss.to_numpy()
indicateurDfSensible

# recupération du nombre de hashtag

entitydf = df['entities']

NbHashtag = np.zeros(len(userdf))

for i in range (len(entitydf)):
    NbHashtag[i] = len(entitydf[i]['hashtags'])

NbHashtag

#récupération du nombre d'url 

