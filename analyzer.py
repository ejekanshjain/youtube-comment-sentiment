import pandas as pd
import nltk
nltk.data.path.append('C:/Users/HP/AppData/Roaming/nltk_data')
nltk.download()
import datetime
from datetime import datetime

from youtube_api import YouTubeDataAPI
import os
import googleapiclient.discovery

from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import matplotlib.pyplot as plt

import pycountry

# settings
import warnings
warnings.filterwarnings("ignore")


def data(region,category,video):
    region = region
    categoryId = category
    video_name = video

    country = pycountry.countries.get(name=region).alpha_2

    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "AIzaSyAiv4C3h8Ei3hWmQyRYs6Gh-y5PxFjAa8k"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)


    # popular = youtube.videos().list(part="contentDetails,snippet,statistics",regionCode=country,chart="mostPopular",videoCategoryId=
    #                                 categoryId).execute()


    popular = []
    view_max = 0
    like_max = 0

    request = youtube.search().list(q=video_name, part='id', maxResults=50, type='video').execute()
    print(request)
    for i in range(len(request)):
        video_id = request['items'][i]['id']['videoId']
        pop = youtube.videos().list(part="contentDetails,snippet,statistics", regionCode=country, id=video_id,
                                    videoCategoryId=
                                    categoryId).execute()
        #     req = youtube.commentThreads().list(part="snippet",videoId=video_id,textFormat="plainText").execute()
        print(pop)
        view = int(pop['items'][0]['statistics']['viewCount'])
        like = int(pop['items'][0]['statistics']['likeCount'])
        if (view_max < view):
            view_max = view
            like_max = like
            popular.append(pop)
            title = pop['items'][0]['snippet']['title']
            channel_title =  pop['items'][0]['snippet']['channelTitle']

            video_id = pop['items'][0]['id']
            # print(pop)
            # print(channel_title)
            word = pop['items'][0]['snippet']['description'].replace(" ", "")
            d = list(x for x in word.split("\n"))

            for x in d:
                x = list(x.split('-'))
                # print(x)
                if (x[0] == 'YouTubeMusic' ):

                    video = x[1]
                    # print(video)


                elif(x[0] == 'Gaana'):

                    video = x[1]
                    # print(x)
                    # print('n',str(x))
                else:
                    video = d[0][1]
                    # print(video)

            video_link = video

    req = youtube.commentThreads().list(part="snippet",videoId=video_id,textFormat="plainText").execute()
    # print(req)
    threads = []
    comments = []
    dates = []
    likes = []
    for item in req["items"]:
        threads.append(item)
        comment = item["snippet"]["topLevelComment"]
        text = comment["snippet"]["textDisplay"]
        date = comment["snippet"]['publishedAt']
        like = comment["snippet"]['likeCount']

        comments.append(text)
        dates.append(date)
        likes.append(like)

    data = list(zip(comments, dates, likes))
    data2 = pd.DataFrame(data)
    data2.columns = ['comments', 'dates', 'likes']


    sentiments = []
    sid = SentimentIntensityAnalyzer()
    scores = {}

    for sentence in comments:
        sentiment = sid.polarity_scores(sentence)

        sentiments.append([sentence, sentiment['neg'], sentiment['pos'],
                           sentiment['neu'], sentiment['compound']])

    df = pd.DataFrame(sentiments)
    df.columns = ['sentence', 'pos', 'neg', 'neu', 'compound']
    total = df.sum(axis=0, skipna=True)



    print(video_id)

    return total,channel_title,video_id



# data('India','Music','Teri Mitti')
