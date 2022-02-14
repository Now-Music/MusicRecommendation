import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

dataPath = '../resources/data'

# 불용어 목록 list로 변환
def stopWordsListGenerization():
    filePath = dataPath + '/korean_stop_words.txt'

    with open(filePath) as f:
        lines = f.readlines()

    lines = [line.rstrip('\n') for line in lines]

    return lines

# 데이터 셋 전처리
def loadData():
    data = pd.read_json(dataPath + '/val.json')
    # 'tags'가 list로 되어있음. 이를 띄어쓰기가 된 string으로 바꿔야함
    # 빈 list는 빈 string ''로 바꿔야 함
    stopWords = stopWordsListGenerization()
    tfidf = TfidfVectorizer(stop_words=stopWords)
    # tfidf_matrix = tfidf.fit_transform(data['tags'])
    # print(tfidf_matrix.shape)

loadData()
