# MusicRecommendation
감정 인식 기반으로 음악 추천해주는 프로그램

1. django 서버(Spring 서버와 감정인식 프로그램과의 통신용 서버)
2. 자연어 처리 - 코사인 유사도 측정
3. Youtube API 필요한가?(이건 윤종이형이랑 정해야 할듯

Notion url : https://www.notion.so/9ba03a04be704b90a06c92b01934c468

## 1. 요구사항 분석


### 1.1. 얼굴 인식

#### 1.1.1. 어플리케이션을 실행하는 디바이스에서 카메라를 통해 사진 촬영을 한다.
#### - 카메라를 촬영할 디바이스 : Mac

#### 1.1.2. 촬영한 사진을 Spring으로 전송한다.
#### - Base64로 encoding
#### - HTTP 통신
#### - Spring은 추후에 로그인 및 DB 연동할 예정

#### 1.1.3. Spring에서 python(감정 인식) container로 로드밸런싱
#### - Spring 서버와의 HTTP 통신을 위해 Django 프레임워크 사용

#### 1.1.4. python container에서 감정 인식 진행
#### - Tensorflow(나 이거 언제 뭘 위해 쓰는지 모름. 공부하자)
#### - OpenCV : 영상 처리를 위한 라이브러리
#### - 기타등등 내용 추가 필요(감정 인식 로직 등).

