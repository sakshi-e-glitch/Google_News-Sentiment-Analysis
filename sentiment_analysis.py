import pandas as pd
from textblob import TextBlob
df=pd.read_csv("Google_News.csv")
polarity_score=[]

for i in range(0, df.shape[0]):
    score=TextBlob(df.iloc[i][0])
    sentiment_score= score.sentiment[0]
    polarity_score.append(sentiment_score)

df=pd.concat([df, pd.Series(polarity_score)], axis=1)
df.rename(columns={df.columns[1]: "Sentiment"}, inplace= True)
total=len(df.Sentiment)
positive=(len(df[df.Sentiment>0]) / total) *100
negative=(len(df[df.Sentiment<0]) / total) *100
neutral= 100- (positive+negative)
print(df.head())
print(total)
print(positive)
print(negative)
print(neutral)