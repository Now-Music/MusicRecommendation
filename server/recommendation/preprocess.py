import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataPath = '../resources/data'
test_emo_doc = ["행복 연애 사랑 여행 봄"]  # DataFrame으로 변환하기 위해 1차원 배열에 string이 들어가있어야 함


def stop_words_list_generation():
    # 불용어 목록을 list로 변환
    filePath = dataPath + '/korean_stop_words.txt'

    with open(filePath) as f:
        lines = f.readlines()
    lines = [line.rstrip('\n') for line in lines]
    return lines


def list_to_str(list):
    # 단어가 들어간 list를 띄어쓰기로 구분된 string으로 변환하여 return
    str = ""
    for elem in list:
        str = str + elem + " "
    return str


################ 데이터 셋 전처리 load_data() 함수의 내용이었음 ################
data = pd.read_json(dataPath + '/val.json')

# data의 'tags' 칼럼은 list형태로 되어있기 때문에, 자연어 처리를 위해 띄어쓰기로 구분된 string으로 변환
data['tags'] = data['tags'].map(list_to_str)
# 코사인 유사도 계산을 위해 사용자의 감정 데이터를 추가함
test_emo_df = pd.DataFrame(test_emo_doc, columns=['tags'])
data = pd.concat([data, test_emo_df])

# 한국어 불용어 사전이 TfidVectorizer에 적용 안됨
# 근데 stop_words를 넣어주지 않아도 함수는 작동하는 것 같음
# stopWords = stop_words_list_generation()

# 데이터 셋의 tf-idf 계산
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data['tags'])

# 사용자의 감정 문서가 들어간 데이터 셋의 코사인 유사도 계산
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
##########################################################################


# 테스트 결과 : 태그가 존재하지 않는 데이터들은 제외됨
# 또한 결과값이 나온다 뿐이지, 추천의 정도가 어떤지는 아직 확인 못함

# 다음 작업 내용
# 1. 리팩토링
# 2. 장르를 분석해서 tags를 추가하는 작업을 해야할지도 모름(단순한 방법은 장르 그대로 tags에 추가하고, "내 감정" 문서에 장르 목록 중 반드시 하나는 들어가게 하는 것
# 3. 상위 열개에 대한 플레이리스트가 나오면, 플레이리스트의 노래들 메타데이터 가져오는 코드 필요
def get_recommendations_test(cosine_sim = cosine_sim):
    # 사용자 데이터의 인덱스는 항상 가장 마지막이기 때문에 마지막 idx를 가져온다
    idx = len(cosine_sim) - 1

    # 사용자의 감정 데이터와 데이터셋 태그 간의 코사인 유사도를 정렬해서 저장
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 상위 10개에 대한 index와 플레이리스트 제목을 return
    sim_scores = sim_scores[1:11]
    plylst_indices = [idx[0] for idx in sim_scores]
    return data['plylst_title'].iloc[plylst_indices]


print(get_recommendations_test(cosine_sim))
