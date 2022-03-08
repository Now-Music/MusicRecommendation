import os.path
import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from . import config
# import config


class Recommend:
    def __init__(self):
        print("Recommend instance created")

    def set_all(self, emo_data = 0):

        # plylst_data의 'tags' 칼럼은 list형태로 되어있기 때문에, 자연어 처리를 위해 띄어쓰기로 구분된 string으로 변환
        self.plylst_data = pd.read_json("C:/Users/HwanKim/Desktop/projects/MusicRecommendation/server/networking/recommendation/data/val.json")
        self.plylst_data['tags'] = self.plylst_data['tags'].map(list_to_str)

        # 코사인 유사도 계산을 위해 사용자의 감정 데이터를 추가함
        print("set all: ", emo_data)
        test_emo_df = pd.DataFrame(config.RECOM_CONFIG['test_emo'], columns=['tags'])
        self.plylst_data = pd.concat([self.plylst_data, test_emo_df])

        # 데이터 셋의 tf-idf 계산
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(self.plylst_data['tags'])

        # 사용자의 감정 문서가 들어간 데이터 셋의 코사인 유사도 계산
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 추사 작업
    # 앨범 추가 하세요
    # 선호 장르 작업 : 만약 플레이리스트 유사도가 죄다 0이면 선호 장르를 기준으로 유사도를 측정한다
    def get_recommendations(self):
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

        song_meta = pd.read_json("C:/Users/HwanKim/Desktop/projects/MusicRecommendation/server/networking/recommendation/data/song_meta.json")
        genre_meta = pd.read_json("C:/Users/HwanKim/Desktop/projects/MusicRecommendation/server/networking/recommendation/data/genre_gn_all.json", typ='series')
        # 아티스트 이름, 노래 제목, 장르 정보를 json 형태로 return
        result = []
        for i in songId:
            result.append({
                    'artist_name': song_meta['artist_name_basket'].iloc[i][0],
                    'song_name': song_meta['song_name'].iloc[i],
                    'genre': genre_meta[song_meta['song_gn_gnr_basket'].iloc[i][0]]
                # 앨범 추가 하세요
                })
        return json.dumps(result, indent=4, ensure_ascii=False)


def list_to_str(list):
    # 단어가 들어간 list를 띄어쓰기로 구분된 string으로 변환하여 return
    str = ""
    for elem in list:
        str = str + elem + " "
    return str


# unit test code
# recom = Recommend()
# recom.set_all()
# print(recom.get_recommendations())
