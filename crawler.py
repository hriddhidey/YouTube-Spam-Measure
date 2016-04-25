from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import matplotlib as plt
import pandas as pd
import gdata.youtube
import gdata.youtube.service

DEVELOPER_KEY = "AIzaSyAYspYcWY0lUmuUTJdn4YEsJA7SuttyZz8" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#UZW2hs-2OAI
var = "UZW2hs-2OAI"

argparser.add_argument("--q", help="Search term", default=var)
argparser.add_argument("--max-results", help="Max results", default=10)
args = argparser.parse_args()
options = args

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
yt_service = gdata.youtube.service.YouTubeService()

search_response = youtube.search().list(
    q=options.q,
    type="video",
    part="id,snippet",
    maxResults=options.max_results
).execute()

videos = {}

for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

#print "Videos:\n", "\n".join(videos), "\n"
s = ','.join(videos.keys())

videos_list_response = youtube.videos().list(
    id=s,
    part='id,statistics'
).execute()

res = []
for i in videos_list_response['items']:
    temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
    temp_res.update(i['statistics'])
    res.append(temp_res)

#for row in res:
#    print row,'\n'
#df = pd.DataFrame.from_dict(res)
#print df.head(10),'\n'
#print df.describe(),'\n'
#print df['likeCount'].mean()
#print df

#comment_feed = yt_service.GetYouTubeVideoCommentFeed(video_id=var)

#for comment_entry in comment_feed.entry:
 # print comment_entry.ToString()


f = open("data.txt","w")
headers = " ".ljust(3)+"Title".ljust(100)+"Views".ljust(15)+"Likes".ljust(15)+"Dislikes".ljust(15)+"Comments".ljust(15)
f.write(headers)
f.write('\n')
for i in range(len(res)):
    entry = str(i+1).ljust(3)
    name = str(res[i]['v_title'].split()).encode('ascii').replace("u'","").replace("'","")
    name = ''.join(name).replace(",","")
    name = name[1:len(name)-1]
    entry+=name.ljust(100)
    entry+=str(res[i]['viewCount']).ljust(15)
    entry+=str(res[i]['likeCount']).ljust(15)
    entry+=str(res[i]['dislikeCount']).ljust(15)
    entry+=str(res[i]['commentCount']).ljust(15)
    f.write(entry)
    f.write('\n')
#i+=1
f.flush();
f.close();
