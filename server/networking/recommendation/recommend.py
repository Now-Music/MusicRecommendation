import pandas as pd
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import config


class Recommend:
    def __init__(self):
        print("Recommend instance created")

    def set_all(self):
        self.plylst_data = pd.read_json(config.RECOM_CONFIG['dataPath'] + '/val.json')

        # plylst_data의 'tags' 칼럼은 list형태로 되어있기 때문에, 자연어 처리를 위해 띄어쓰기로 구분된 string으로 변환
        self.plylst_data['tags'] = self.plylst_data['tags'].map(list_to_str)
        # 코사인 유사도 계산을 위해 사용자의 감정 데이터를 추가함
        test_emo_df = pd.DataFrame(config.RECOM_CONFIG['test_emo'], columns=['tags'])
        self.plylst_data = pd.concat([self.plylst_data, test_emo_df])

        # 데이터 셋의 tf-idf 계산
        tfidf = TfidfVectorizer()
        tfidf_matrix = tfidf.fit_transform(self.plylst_data['tags'])

        # 사용자의 감정 문서가 들어간 데이터 셋의 코사인 유사도 계산
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # 테스트 결과 : 태그가 존재하지 않는 데이터들은 제외됨
    # 또한 결과값이 나온다 뿐이지, 추천의 정도가 어떤지는 아직 확인 못함
    # 장르를 분석해서 tags를 추가하는 작업을 해야할지도 모름(단순한 방법은 장르 그대로 tags에 추가하고, "내 감정" 문서에 장르 목록 중 반드시 하나는 들어가게 하는 것
    def get_recommendations(self):
        # 사용자 데이터의 인덱스는 항상 가장 마지막이기 때문에 마지막 idx를 가져온다
        idx = len(self.cosine_sim) - 1

        # 사용자의 감정 데이터와 데이터셋 태그 간의 코사인 유사도를 정렬해서 저장
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # 상위 1개에 대한 플레이리스트 index를 추출
        sim_scores = sim_scores[1:2]
        plylst_id = [idx[0] for idx in sim_scores]

        # 플레이리스트의 노래들 중 랜덤 하나 선택
        songMeta = pd.read_json(config.RECOM_CONFIG['dataPath'] + '/song_meta.json')
        songId = random.choice(self.plylst_data['songs'].iloc[plylst_id].iloc[0])

        # 아티스트 이름과 노래 제목을 json 형태로 return
        return songMeta['artist_name_basket'].iloc[songId][0], songMeta['song_name'].iloc[songId]


def list_to_str(list):
    # 단어가 들어간 list를 띄어쓰기로 구분된 string으로 변환하여 return
    str = ""
    for elem in list:
        str = str + elem + " "
    return str


recom = Recommend()
recom.set_all()
print(recom.get_recommendations())

