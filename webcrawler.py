import requests
import os
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("APIKEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

query = str(input('Enter your data to search for: '))
channels_search_count = int(
    input('How many results do you want? (Limited Maximum Queries by google to 10 (idk why! :| )  ): '))
while channels_search_count <= 0 or channels_search_count > 10:
    channels_search_count = int(input('Wrong number. Try again.'
                                      '\nHow many results do you want? (Limited Maximum Queries by google to 10 (idk why! :| )  )): '))

search_request = youtube.search().list(
    q=query,
    part='snippet',
    type='channel',
    maxResults=channels_search_count,
)

channels_id = []
channels_name = []
response = search_request.execute()
for item in response['items']:
    channels_id.append(item['id']['channelId'])
    channels_name.append(item['snippet']['title'])

result = []
for channel in channels_id:
    request = youtube.channels().list(
        part='statistics',
        id=channel
    )
    response = request.execute()
    # print(response)
    result.append(response['items'][0]['statistics']['subscriberCount'])
for i in range(len(channels_name)):
    print(f'Channel Name: {channels_name[i]}\n'
          f'Subscribers Count: {result[i]}')
