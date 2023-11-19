import os
import time
import requests
from tqdm.auto import tqdm
from bs4 import BeautifulSoup

# get file video
video_ids = os.listdir("data")

# sort 
splits = sorted(os.listdir(f"data/{video_ids[0]}"))

# split type of time 
documents = []
for video_id in tqdm(video_ids):
    splits = sorted(os.listdir(f"data/{video_id}"))
    start_timestamp = "00:00:00"
    passage = ""
    for i, s in enumerate(splits):
        with open(f"data/{video_id}/{s}/subtitles.txt") as f:
            out = f.read()
            passage += " " + out
        if len(passage) > 360:
            end_timestamp = s.split("-")[1].split(",")[0]
            start = time.strptime(start_timestamp,"%H:%M:%S")

            end_timestamp = end_timestamp.replace("_", ":")
            end = time.strptime(end_timestamp,"%H:%M:%S")

            start_second = start.tm_sec + start.tm_min*60 + start.tm_hour*3600
            end_second = end.tm_sec + end.tm_min*60 + end.tm_hour*3600

            documents.append({
                "video_id": video_id,
                "text": passage,
                "start_second": start_second,
                "end_second": end_second,
                "url": f"https://www.youtube.com/watch?v={video_id}&t={start_second}s",
            })
            start_timestamp = end_timestamp
            passage = ""

#add titlte and thumbnail from BeautifulSoup
metadata = {}
for _id in tqdm(video_ids):
    r = requests.get(f"https://www.youtube.com/watch?v={_id}")
    soup = BeautifulSoup(r.content, 'lxml')  # lxml package is used here
    try:
        title = soup.find("meta", property="og:title").get("content")
        thumbnail = soup.find("meta", property="og:image").get("content")
        metadata[_id] = {"title": title, "thumbnail": thumbnail}
    except Exception as e:
        print(e)
        print(_id)
        metadata[_id] = {"title": "", "thumbnail": ""}

# merge metaData(title, thumbnail) to document(info video)
for i, doc in enumerate(documents):
    _id = doc['video_id']
    meta = metadata[_id]
    documents[i] = {**doc, **meta}








