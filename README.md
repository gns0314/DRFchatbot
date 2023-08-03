# DRF를 이용한 메뉴 추천 메뉴 추천 chatbot 만들기
- 냉장고에 있는 재료로 만들수 있는 메뉴를 추천해주는 웹 서비스

## 목적
- Rest API를 이용하여 서버와 클라이언트를 통신시킨 메뉴 추천 chatbot 웹 만들기


## 개발 환경 및 개발 기간
- 개발 환경
    - Django 4.2.3
    - Python 3.11.4
- 개발 기간
    - 2023년 7월 26일 ~ 2023년 8월 2일

## 기능
- 회원가입
- 로그인
- 로그아웃
- 메뉴 추천 챗봇
- 채팅 내역

## 데이터베이스 모델링
![ERD](https://github.com/gns0314/DRFchatbot/assets/34575297/34502849-f2b8-4285-91a5-340e07ff859e)

## 프로젝트 구조
```
├─chatbot
│  ├─migrations
│  └─__pycache__
├─chat_project
│  └─__pycache__
├─user
│  ├─migrations
│  └─__pycache__
└─venv
```

## URL 구성
| 기능           | URL |
|----------------|-----|
| 인덱스 페이지 |  /  |
| 챗봇 | /chatbot/ |
| 채팅 내역 | /chatbot/list/ |
| 로그인 | /user/login/ |
| 로그아웃 | /user/logout/ |
| 회원가입 | /user/register/ |

## 실행 화면
- 메인 페이지
![메인](https://github.com/gns0314/DRFchatbot/assets/34575297/c52c4ca7-eb62-4829-b9cb-82daef32ac6b)
- 챗봇 
![실행](https://github.com/gns0314/DRFchatbot/assets/34575297/d53b3f29-be40-4708-b855-86ecd2af4f83)
    - 토큰을 이용하여 로그인이 되었는지 체크하고 로그인이 되어있어야 사용 가능합니다.
- 비로그인시 챗봇
![비로그인 처리](https://github.com/gns0314/DRFchatbot/assets/34575297/2421dad0-c43a-49ba-a985-8f9ac41ad4a6)
    - 토큰으로 로그인 유무를 체크하고 토큰이 없다면 로그인이 필요합니다 창을 띄어주고 확인시 로그인 페이지로 돌아갑니다.
- 비로그인시 채팅내역
![비로그인 채팅내역 처리](https://github.com/gns0314/DRFchatbot/assets/34575297/6067cb06-c8d3-4b06-b2e1-0597db101d55)

- 1일 횟수 제한
![5번 처리](https://github.com/gns0314/DRFchatbot/assets/34575297/78962ffc-c5cb-402e-adda-411db7a8a174)
    - 유저별로 count를 저장해 질문시 count가 1 증가하고 count가 5가되면 더 이상 질문을 못하게 됩니다. 그리고 마지막 요청으로부터 24시간이 지나면 횟수가 0번으로 초기화 됩니다.

- 채팅내역
![채팅내역](https://github.com/gns0314/DRFchatbot/assets/34575297/44a9e65e-1b83-4f36-8d09-badf3acdfa06)

- 로그인
![로그인](https://github.com/gns0314/DRFchatbot/assets/34575297/2749a051-62cb-4778-a8e0-050931ad27d4)

- 회원가입
![회원가입](https://github.com/gns0314/DRFchatbot/assets/34575297/74c75c74-e20b-41c0-bbd5-0108a7763fb9)

## 느낀점
Rest API로 직접 서버를 구현하고 FE와 통신 연결까지 해보는 게 너무 생소하고 어려웠지만 많은 것을 알 수 있던 프로젝트였습니다. 
특히 CORS정책이라는 오류를 만나보면서 CORS정책이 있다는 것을 찾아보면서 CORS정책이 무엇인지 알게 되고 해결 방법으로 장고의 Django-CORS-headers 라이브러리를 사용하는 방법을 이용하여 해결할 수 있다는 것을 알게 되어 CORS정책 문제를 해결하면서 CORS정책에 대해 알게 되었습니다.
로그인과 회원가입 시 서버 단에서만 테스트할 때는 세션을 이용하여 손쉽게 하였지만 클라이언트와 서버의 도메인이 달라 해결 방법을 찾는 중 authentication_classes를 제대로 찾아 보니 토큰을 이용하여 해결할 수 있다는 것을 알고 장고의 Token Authentication을 이용한 방식으로 `from rest_framework.authtoken.models import Token`을 이용하여 장고 자체의 토큰을 받아와 서버와 클라이언트 간 토큰으로 인증하여 로그인과 로그인을 한 사용자인지 판별하는 거까지 해결할 수 있었습니다. 또 그 과정에서 Token을 이용한 통신 시 보안적인 측면과 Cross-Origin 요청 처리에 대한 용이성 또 상태를 세션에 저장하지 않기 때문에 서버의 부하를 감소할수 있다는 장점들을 알게되 었습니다. 정말 생소하고 어려웠던 프로젝트였지만 클라이언트 - 서버 간의 통신에 대해 알 수 있었던 프로젝트였습니다.

## 개선점
1. API의 부분과 오류처리가 안된 부분의 오류처리 추가
2. 현재 로그아웃시 서버에서의 토큰 무효화가 아닌 클라이언트에서 하고있는 부분을 서버에도 적용
3. 로그인과 회원가입의 특정 필드에 대한 오류메시지 추가
4. FE의 로그인시에만 로그아웃, 채팅내역, 챗봇이용이 보이는 처리