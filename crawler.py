from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import gdata.youtube
import gdata.youtube.service
import math
"""
IMPORTS
"""
#_____________________

"""
DEFINE CLUSTER CLASS
"""
class Cluster:
    
    def __init__(self,name,mrating,mreactions):
        self.name = name
        self.videos = []
        self.mrating = mrating
        self.mreactions = mreactions
    
    def get_mrating(self):
        return str(self.mrating)

    def get_mreactions(self):
        return str(self.mreactions)

    def add_video(self,video):
        self.videos.append(video)



"""
DEFINE EUCLIDIAN DISTANCE FUNCTION
"""
def euclidian(x1,y1,x2,y2):
    return math.sqrt(math.pow((float(x1)-float(x2)),2)+math.pow((float(y1)-float(y2)),2))



"""
INITIALIZE API KEY
"""
DEVELOPER_KEY = "AIzaSyAYspYcWY0lUmuUTJdn4YEsJA7SuttyZz8" 
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"



"""
TAKE INPUT URL
"""
url = str(raw_input('Please enter URL of YouTube video: '))
v_id = url[len(url)-11:len(url)]


"""
SETUP FIRST QUERY
"""
argparser.add_argument("--q", help="Search term", default=v_id)
argparser.add_argument("--max-results", help="Max results", default=1)
args = argparser.parse_args()
options = args
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


"""
EXECUTE FIRST QUERY
"""
search_response = youtube.search().list(
    q=options.q,
    type="video",
    part="id,snippet",
    maxResults=options.max_results
).execute()


"""
STORE IN 'user'
"""
videos = {}

for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

s = ','.join(videos.keys())

videos_list_response = youtube.videos().list(
    id=s,
    part='id,statistics'
).execute()

user = []
for i in videos_list_response['items']:
    temp_res = dict(v_id = i['id'], v_title = videos[i['id']])
    temp_res.update(i['statistics'])
    user.append(temp_res)


"""
SETUP SECOND QUERY
"""
val = str(user[0]['v_title'])
argparser.add_argument("--p", help="Search term", default=val)
argparser.add_argument("--m", help="Max results", default=50)
args = argparser.parse_args()
options = args
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)


"""
EXECUTE SECOND QUERY
"""
search_response = youtube.search().list(
    q=options.p,
    type="video",
    part="id,snippet",
    maxResults=options.m
).execute()


"""
STORE IN 'res'
"""
videos = {}

for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
        videos[search_result["id"]["videoId"]] = search_result["snippet"]["title"]

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


"""
CHECK FOR NON-EXISTENT KEYS AND ZERO VALUES IN 'res'
"""
for i in range(len(res)):
    if 'viewCount' in res[i].keys():
        if res[i]['viewCount']==0:
            res[i]['viewCount']=1.0
    else:
        res[i]['viewCount']=1.0
    if 'likeCount' in res[i].keys():
        if res[i]['likeCount']==0:
            res[i]['likeCount']=1.0
    else:
        res[i]['likeCount']=1.0
    if 'dislikeCount' in res[i].keys():
        if res[i]['dislikeCount']==0:
            res[i]['dislikeCount']=1.0
    else:
        res[i]['dislikeCount']=1.0
    if 'commentCount' in res[i].keys():
        if res[i]['commentCount']==0:
            res[i]['commentCount']=1.0
    else:
        res[i]['commentCount']=1.0


"""
CREATION AND ASSIGNING OF CLUSTERS
"""
cluster1 = Cluster('cluster1',float(float(res[0]['likeCount'])/(float(res[0]['dislikeCount'])+1)),float(float(res[0]['viewCount'])/(float(res[0]['commentCount'])+1)))
cluster2 = Cluster('cluster2',float(float(res[5]['likeCount'])/(float(res[5]['dislikeCount'])+1)),float(float(res[5]['viewCount'])/(float(res[5]['commentCount'])+1)))
cluster3 = Cluster('cluster3',float(float(res[10]['likeCount'])/(float(res[10]['dislikeCount'])+1)),float(float(res[10]['viewCount'])/(float(res[10]['commentCount'])+1)))
cluster4 = Cluster('cluster4',float(float(res[len(res)-30]['likeCount'])/(float(res[len(res)-30]['dislikeCount'])+1)),float(float(res[len(res)-30]['viewCount'])/(float(res[len(res)-30]['commentCount'])+1)))
cluster5 = Cluster('cluster5',float(float(res[len(res)-10]['likeCount'])/(float(res[len(res)-10]['dislikeCount'])+1)),float(float(res[len(res)-10]['viewCount'])/(float(res[len(res)-10]['commentCount'])+1)))
cluster6 = Cluster('cluster6',float(float(res[len(res)-5]['likeCount'])/(float(res[len(res)-5]['dislikeCount'])+1)),float(float(res[len(res)-5]['viewCount'])/(float(res[len(res)-5]['commentCount'])+1)))
cluster7 = Cluster('cluster7',float(float(res[len(res)-1]['likeCount'])/(float(res[len(res)-1]['dislikeCount'])+1)),float(float(res[len(res)-1]['viewCount'])/(float(res[len(res)-1]['commentCount'])+1)))

print 'Mratings of clusters: ',cluster1.get_mrating(),',',cluster2.get_mrating(),',',cluster3.get_mrating(),',',cluster4.get_mrating(),',',cluster5.get_mrating(),',',cluster6.get_mrating(),',',cluster7.get_mrating(),'\n'
print 'MReactions of clusters: ',cluster1.get_mreactions(),',',cluster2.get_mreactions(),',',cluster3.get_mreactions(),',',cluster4.get_mreactions(),',',cluster5.get_mreactions(),',',cluster6.get_mreactions(),',',cluster7.get_mreactions(),'\n'

for i in range(len(res)):
    mini = 999999999
    posn=0
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster1.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster1.get_mreactions())
    if dist<mini:
        mini=dist
        posn=1
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster2.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster2.get_mreactions())
    if dist<mini:
        mini=dist
        posn=2
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster3.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster3.get_mreactions())
    if dist<mini:
        mini=dist
        posn=3
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster4.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster4.get_mreactions())
    if dist<mini:
        mini=dist
        posn=4
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster5.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster5.get_mreactions())
    if dist<mini:
        mini=dist
        posn=5
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster6.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster6.get_mreactions())
    if dist<mini:
        mini=dist
        posn=6
    dist = euclidian(float(res[i]['likeCount'])/(float(res[i]['dislikeCount'])+1),cluster7.get_mrating(),float(res[i]['viewCount'])/(float(res[i]['commentCount'])+1),cluster7.get_mreactions())
    if dist<mini:
        mini=dist
        posn=7
    if posn==1:
        cluster1.add_video(res[i])
    elif posn==2:
        cluster2.add_video(res[i])
    elif posn==3:
        cluster3.add_video(res[i])
    elif posn==4:
        cluster4.add_video(res[i])
    elif posn==5:
        cluster5.add_video(res[i])
    elif posn==6:
        cluster6.add_video(res[i])
    elif posn==7:
        cluster7.add_video(res[i])


"""
FIND SPAM PERCENTAGE BASED ON MEAN RATING AND MEAN REACTIONS ACROSS CLUSTERS
"""
def find_percent(video,cluster):
    mean_rating = float(cluster1.get_mrating())+float(cluster2.get_mrating())+float(cluster3.get_mrating())+float(cluster4.get_mrating())+float(cluster5.get_mrating())+float(cluster6.get_mrating())+float(cluster7.get_mrating())
    mean_rating /= 7.0
    mean_reaction = float(cluster1.get_mreactions())+float(cluster2.get_mreactions())+float(cluster3.get_mreactions())+float(cluster4.get_mreactions())+float(cluster5.get_mreactions())+float(cluster6.get_mreactions())+float(cluster7.get_mreactions())
    mean_reaction /= 7.0
    percent = 0
    if float(cluster.get_mrating())>mean_rating:
        if float(cluster.get_mreactions())<mean_reaction:
            if float((float(video['viewCount'])/(float(video['commentCount'])+1)))<float(cluster.get_mreactions()):
                if float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=0
                else:
                    percent+=3
            elif float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=3
            else:
                percent+=5
        else:
            if float((float(video['viewCount'])/(float(video['commentCount'])+1)))<float(cluster.get_mreactions()):
                if float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=5
                else:
                    percent+=7
            elif float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=10
            else:
                percent+=17
    else:
        if float(cluster.get_mreactions())<mean_reaction:
            if float((float(video['viewCount'])/(float(video['commentCount'])+1)))<float(cluster.get_mreactions()):
                if float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=2
                else:
                    percent+=4
            elif float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=3
            else:
                percent+=5
        else:
            if float((float(video['viewCount'])/(float(video['commentCount'])+1)))<float(cluster.get_mreactions()):
                if float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=23
                else:
                    percent+=35
            elif float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))>float(cluster.get_mrating()):
                    percent+=43
            else:
                percent+=47
    if float((float(video['likeCount'])/(float(video['dislikeCount'])+1)))<76:
        percent+=5
    if float((float(video['viewCount'])/(float(video['commentCount'])+1)))>1800:
        percent+=2
    return percent


"""
ASSIGNING USER ENTERED URL TO A CLUSTER
"""
mini = 999999999
posn=0
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster1.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster1.get_mreactions())
if dist<mini:
    mini=dist
    posn=1
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster2.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster2.get_mreactions())
if dist<mini:
    mini=dist
    posn=2
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster3.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster3.get_mreactions())
if dist<mini:
    mini=dist
    posn=3
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster4.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster4.get_mreactions())
if dist<mini:
    mini=dist
    posn=4
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster5.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster5.get_mreactions())
if dist<mini:
    mini=dist
    posn=5
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster6.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster6.get_mreactions())
if dist<mini:
    mini=dist
    posn=6
dist = euclidian(float(user[0]['likeCount'])/(float(user[0]['dislikeCount'])+1),cluster7.get_mrating(),float(user[0]['viewCount'])/(float(user[0]['commentCount'])+1),cluster7.get_mreactions())
if dist<mini:
    mini=dist
    posn=7
if posn==1:
    cluster1.add_video(user[0])
    val = find_percent(user[0],cluster1)
    print 'Your entered video is ',val,'%  likely to be spam'
elif posn==2:
    val = find_percent(user[0],cluster2)
    cluster2.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'
elif posn==3:
    val = find_percent(user[0],cluster3)
    cluster3.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'
elif posn==4:
    val = find_percent(user[0],cluster4)
    cluster4.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'
elif posn==5:
    val = find_percent(user[0],cluster5)
    cluster5.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'
elif posn==6:
    val = find_percent(user[0],cluster6)
    cluster6.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'
elif posn==7:
    val = find_percent(user[0],cluster7)
    cluster7.add_video(user[0])
    print 'Your entered video is', val,'%  likely to be spam'


"""
DATA FILE WRITE
f = open("search.txt","w")
headers = "Title".ljust(110)+"Views".ljust(15)+"Likes".ljust(15)+"Dislikes".ljust(15)+"Comments".ljust(15)
f.write(headers)
f.write('\n')
for i in range(len(res)):
    #entry = str(i+1).ljust(3)
    entry=''
    name = str(res[i]['v_title'].split()).encode('ascii').replace("u'","").replace("'","")
    name = ''.join(name).replace(",","")
    name = name[1:len(name)-1]
    entry+=name.ljust(110)
    entry+=str(res[i]['viewCount']).ljust(15)
    if res[i].has_key('likeCount'):
        entry+=str(res[i]['likeCount']).ljust(15)
    else :
        entry+=str(0).ljust(15)
        res[i]['likeCount']=0
    if res[i].has_key('dislikeCount'):
        entry+=str(res[i]['dislikeCount']).ljust(15)
    else :
        entry+=str(0).ljust(15)
        res[i]['dislikeCount']=0
    if res[i].has_key('commentCount'):
        entry+=str(res[i]['commentCount']).ljust(15)
    else :
        entry+=str(0).ljust(15)
        res[i]['commentCount']=0
    f.write(entry)
    f.write('\n')
f.flush();
f.close();

"""


"""
MAKE DATA FRAME AND ANALYZE
df = pd.DataFrame.from_dict(res)

f = open("search_means.txt","w")
f.write("Mean views :\n")
f.write(str(df['viewCount'].median()));
f.write("\nMean comments :\n")
f.write(str(df['commentCount'].median()));
f.write("\nMean ratings :\n")
f.write(str(float(df['likeCount'].median())/float(df['dislikeCount'].median())));
f.write("\nMean reactions ratio:\n")
f.write(str(float(df['viewCount'].median())/float(df['commentCount'].median())));
f.flush()
f.close()

"""
