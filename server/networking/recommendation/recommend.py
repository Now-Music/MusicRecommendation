import os.path
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from . import config
# import config  # unit test mode


class Recommend:
    def __init__(self):
        print("Recommend instance created")

    def create_emo_data(self, data):
        result = set_weather(data['weather'])
        result += set_emotion(data['emotion'])
        result += set_state(data['state'])
        result += set_user_age(data['user_age'])
        # 추출된 단어 목록들에 대해 랜덤 10개만 감정 데이터로 사용
        result = random.sample(result, 10)
        print("networking/recommend/set_all() :" + result)
        return [list_to_str(result)]

    def set_all(self, emo_data = 0):
        print("networking/recommend/set_all() start")
        # plylst_data의 'tags' 칼럼은 list형태로 되어있기 때문에, 자연어 처리를 위해 띄어쓰기로 구분된 string으로 변환
        self.plylst_data = pd.read_json("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/val.json")
        self.plylst_data['tags'] = self.plylst_data['tags'].map(list_to_str)

        # 코사인 유사도 계산을 위해 사용자의 감정 데이터를 추가함
        # print("set all: ", emo_data)
        if emo_data == 0: # 파라미터로 넘어온게 없을 경우
            test_emo_df = pd.DataFrame(config.RECOM_CONFIG['test_emo'], columns=['tags'])
            self.plylst_data = pd.concat([self.plylst_data, test_emo_df])
        else: # 파라미터로 사용자의 감정 데이터가 넘어온 경우
            test_emo_df = pd.DataFrame(emo_data, columns=['tags'])
            self.plylst_data = pd.concat([self.plylst_data, test_emo_df])

        # 데이터 셋의 tf-idf 계산
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(self.plylst_data['tags'])

        # 사용자의 감정 문서가 들어간 데이터 셋의 코사인 유사도 계산
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    def get_recommendations(self):
        print("networking/recommend/get_recommendations() start")
        # 사용자 데이터의 인덱스는 항상 가장 마지막이기 때문에 마지막 idx를 가져온다
        idx = len(self.cosine_sim) - 1

        # 사용자의 감정 데이터와 데이터셋 태그 간의 코사인 유사도를 정렬해서 저장
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 상위 10개에 대한 플레이리스트 index를 추출
        sim_scores = sim_scores[1:10]
        # 사용자 감정과 모든 플레이리스트 간의 유사도가 0일 경우
        if sim_scores[0][1] == 0:
            return "all-similarity zero exception"

        plylst_id = [idx[0] for idx in sim_scores]

        # 플레이리스트의 노래들 중 랜덤 하나 선택
        songId = 0
        found_id = False
        for i in plylst_id:
            if len(self.plylst_data['songs'].iloc[i]) != 0:
                plylst_size = len(self.plylst_data['songs'].iloc[i])
                songId = random.sample(self.plylst_data['songs'].iloc[i], 10 if 10 <= plylst_size else plylst_size)
                found_id = True
                break

        # 상위 10개 플레이리스트의 노래 id data가 모두 empty인 경우
        if not found_id:
            return "all playlist empty exception"

        song_meta = pd.read_json("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/song_meta.json")
        genre_meta = pd.read_json("C:/Users/HwanKim/OneDrive/바탕 화면/projects/MusicRecommendation/server/networking/recommendation/data/genre_gn_all.json", typ='series')
        # 아티스트 이름, 노래 제목, 장르 정보를 json 형태로 return
        result = []
        for i in songId:
            result.append(i)
        return json.dumps({'id_list': result}, indent=4, ensure_ascii=False)
            # 'title': song_meta['song_name'].iloc[i],
        # 'artist': song_meta['artist_name_basket'].iloc[i][0],
        # 'genre': genre_meta[song_meta['song_gn_gnr_basket'].iloc[i][0]],
        # 'album': song_meta['album_name'].iloc[i]


def list_to_str(list):
    # 단어가 들어간 list를 띄어쓰기로 구분된 string으로 변환하여 return
    str = ""
    for elem in list:
        str = str + elem + " "
    return str


# Thunderstorm Drizzle Rain Snow Clouds Clear
def set_weather(weather):
    result = []
    if weather == "Thunderstorm":
        result = ["슬픔", "우울", "눈물", "이벌", "분노", "화남", "비", "소나기", "여름"]
    elif weather == "Drizzle":
        result = ["이슬", "소나기", "봄비", "봄", "따뜻함", "꽃"]
    elif weather == "Rain":
        result = ["슬픔", "우울", "눈물", "분노", "화남", "비", "소나기", "여름", "이슬", "소나기", "봄비", "봄", "따뜻함", "꽃"]
    elif weather == "Snow":
        result = ["눈", "첫눈", "크리스마스", "선물", "연인", "사랑", "연애"]
    elif weather == "Clear":
        result = ["연인", "사랑", "연애", "봄", "따뜻함", "꽃"]
    return result


# neutral happy surprise sad angry
def set_emotion(emotion):
    result = []
    if emotion == "happy":
        result = ["행복", "웃음", "즐거음", "신남", "선물", "연인", "사랑", "연애"]
    elif emotion == "sad":
        result = ["슬픔", "우울", "눈물", "이벌"]
    elif emotion == "angry":
        result = ["분노", "화남", "이벌"]
    return result


#  rest exercise study travel
def set_state(state):
    result = []
    if state == "rest":
        result = ["휴식", "느긋함", "나른함", "수면"]
    elif state == "exercise":
        result = ["운동", "활발함", "땀", "신남", "노력", "성취", "목표"]
    elif state == "study":
        result = ["공부", "스터디", "성공", "신남", "노력", "성취", "목표"]
    elif state == "travel":
        result = ["여행", "힐링", "캠핑", "축제"]
    return result


def set_user_age(user_age):
    result = []
    if 0 <= user_age <= 29:
        result = ["젊음", "청춘", "여행", "낭만", "연인", "사랑", "연애"]
    elif 44 <= user_age:
        result = ["가족", "황혼"]
    return result

# unit test code
# recom = Recommend()
# result = recom.create_emo_data({'weather': 'Clean', 'emotion': 'happy', 'state': 'travel', 'user_age': 25})
# recom.set_all(result)
# print(recom.get_recommendations())
