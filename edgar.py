import json
import pandas as pd

# Opening JSON file
tweets = []
for line in open('data/raw0.json', 'r'):
    tweets.append(json.loads(line))

df = pd.DataFrame(tweets)

print(df.head())