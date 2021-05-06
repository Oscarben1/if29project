import json
import pandas as pd

# Opening JSON file
tweets = []
for i in range(10):
  for line in open('data/raw'+ str(i) +'.json', 'r', encoding='utf8'):
      tweets.append(json.loads(line))

df = pd.DataFrame(tweets)

#print(df.head())
print(df.describe())