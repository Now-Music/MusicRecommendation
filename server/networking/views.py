from django.http import HttpResponse
from .recommendation import recommend as rec
import json


def recommend(request):
    # post request의 data 받는 방법
    # request.data.get("데이터이름")
    # body_unicode = request.body.decode('utf-8')
    # print(body_unicode)
    # body = json.loads(body_unicode)
    recObject = rec.Recommend()
    # recObject.set_all(body['message'])
    recObject.set_all()
    result = recObject.get_recommendations()
    print(result)
    return HttpResponse(result)
