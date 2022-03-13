from django.http import HttpResponse
from .recommendation import recommend as rec
import json


def recommend(request):
    # post request의 data 받는 방법
    # request.data.get("데이터이름")
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    recObject = rec.Recommend()
    print(body)
    emo_data = recObject.create_emo_data(body)
    recObject.set_all(emo_data)
    result = recObject.get_recommendations()

    # 선호 장르 작업 : 만약 플레이리스트 유사도가 죄다 0이면 선호 장르 + 감정 상태를 기준으로 유사도를 측정한다
    if result == "all-similarity zero exception":
        print("all-similarity zero exception")
        recObject.set_all(["아빠"])
        result = recObject.get_recommendations()
    print(result)
    return HttpResponse(result)
