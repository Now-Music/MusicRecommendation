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


# ToDo : "`" 이 문자 포함되면 오류뜸. continue로 넘기거나 범석이형 쪽에서 해결되면 그대로 보내거나
def songdata(request):
    with open("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/song_meta.json", "r", encoding="UTF-8") as json_file:
        datas = json.load(json_file)
        url = "http://192.168.0.11:8080/db/music/all"

        headers = {'Content-Type': 'application/json'} # multipart/form-data
        result = []

        i = 0
        for song in datas:
            # if i < 100:
            #     i += 1
            #     continue
            if i == 262:
                i += 1
                continue
            if i == 500:
                break
            genre = song['song_gn_gnr_basket']
            if type(genre) is not str:
                genre = ""
            if len(song['song_gn_gnr_basket']) == 0:
                genre = ""
            else:
                genre = song['song_gn_gnr_basket'][0]

            if "`" in song['id']:
                song['id'].replace("`", "")
            if "`" in song['song_name']:
                song['song_name'].replace("`", "")
            if "`" in song['artist_name_basket'][0]:
                song['artist_name_basket'].replace("`", "")
            if "`" in song['album_name']:
                song['album_name'].replace("`", "")

            result.append({
                'id': song['id'],
                'title':song['song_name'],
                'artist':song['artist_name_basket'][0],
                'genre':genre,
                'album':song['album_name']
            })
            if genre == "":
                print(result[len(result) - 1])
            if 258 <= i <= 262:
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
