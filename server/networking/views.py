from django.http import HttpResponse


# 경로 문제 해결해

#from networking.recommendation.recommend import Recommend

from sibal import Sibal

def recommend(request):
    # recObject = Recommend()
    # recObject.set_all()
    s = Sibal()
    return HttpResponse("sibal")
