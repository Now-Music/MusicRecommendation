from django.http import HttpResponse
from .recommendation import recommend as rec
import json

import pandas as pd
import requests

def recommend(request):
    # post request의 data 받는 방법
    # request.data.get("데이터이름")
    print("recommend request start")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recObject = rec.Recommend()
    emo_data = recObject.create_emo_data(body)
    recObject.set_all(emo_data)
    result = recObject.get_recommendations()

    # 선호 장르 작업 : 만약 플레이리스트 유사도가 죄다 0이면 선호 장르 + 감정 상태를 기준으로 유사도를 측정한다
    if result == "all-similarity zero exception" or result == "all playlist empty exception":
        print("exception")
        new_emo_data = body['emotion'] + body['genre']
        print(new_emo_data)
        recObject.set_all([new_emo_data])
        result = recObject.get_recommendations()

    print(result)
    return HttpResponse(result)


def genredata(request):
    with open("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/genre_gn_all.json", "r", encoding="UTF-8") as json_file:
        datas = json.load(json_file)
        url = "http://192.168.0.11:8080/db/music/genres"

        headers = {'Content-Type': 'application/json'}
        result = []
        for key in datas:
            result.append({'id':key, 'genre': datas[key]})
        requests.post(url, headers=headers, data=json.dumps(result))
        return HttpResponse("succes")


# ToDo : 5000까지 함. 그 뒤로 계속 ㄱㄱ. ip도 바뀌면 바껴야됨
def songdata(request):
    with open("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/song_meta.json", "r", encoding="UTF-8") as json_file:
        datas = json.load(json_file)
        url = "http://172.20.10.9:8080/db/music/all"

        headers = {'Content-Type': 'application/json'} # multipart/form-data
        result = []
        testString = "asd`we`g"
        print("string.replace test", testString.replace("`", " "))
        i = 0
        for song in datas:
            if i < 1000:
                i += 1
                continue
            if i == 5000:
                break
            title = song['song_name']
            artist = song['artist_name_basket'][0]
            genre = song['song_gn_gnr_basket']
            album = song['album_name']
            if type(genre) is not str:
                genre = ""
            if len(song['song_gn_gnr_basket']) == 0:
                genre = ""
            else:
                genre = song['song_gn_gnr_basket'][0]

            if "`" in song["song_name"]:
                title = title.replace("`", "")
                print(i, title)
            if "`" in song["artist_name_basket"][0]:
                artist = artist.replace("`", "")
                print(i, artist)
            if "`" in song["album_name"]:
                album = album.replace("`", "")
                print(i, album)

            result.append({
                'id': song['id'],
                'title':title,
                'artist':artist,
                'genre':genre,
                'album':album
            })
            if i == 261 or i == 421:
                print(result[len(result) - 1])

            i += 1
        print("finish")
        print(len(result))
        requests.post(url, headers=headers, data=json.dumps(result))

        return HttpResponse("sucess")

        # title, artist, genre, album
            # 'title': song_meta['song_name'].iloc[i],
        # 'artist': song_meta['artist_name_basket'].iloc[i][0],
        # 'genre': genre_meta[song_meta['song_gn_gnr_basket'].iloc[i][0]],
        # 'album': song_meta['album_name'].iloc[i]
