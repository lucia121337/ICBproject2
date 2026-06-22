import requests
import pandas as pd
from datetime import datetime

class NaverAPIClient:
    def __init__(self, client_id: str, client_secret: str):
        self.headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

    def _get_request(self, url: str, params: dict):
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def _post_request(self, url: str, body: dict):
        response = requests.post(url, headers=self.headers, json=body)
        response.raise_for_status()
        return response.json()

    # 1. 데이터랩 검색어 트렌드
    def get_datalab_search_trend(self, start_date: str, end_date: str, keywords: list):
        url = "https://openapi.naver.com/v1/datalab/search"
        
        keyword_groups = []
        for kw in keywords:
            keyword_groups.append({
                "groupName": kw,
                "keywords": [kw]
            })

        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "keywordGroups": keyword_groups
        }
        
        return self._post_request(url, body)

    # 2. 데이터랩 쇼핑 트렌드
    def get_datalab_shopping_trend(self, start_date: str, end_date: str, category_name: str, category_param: str):
        url = "https://openapi.naver.com/v1/datalab/shopping/categories"
        
        # 쇼핑 트렌드는 키워드 대신 카테고리 코드를 사용하므로,
        # 이 대시보드에서는 단순화를 위해 임의의 카테고리를 넣거나 키워드를 카테고리명으로 취급할 수 있도록 설정
        # (실제 API는 카테고리 ID를 요구함. 예: 50000000)
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": "date",
            "category": [
                {"name": category_name, "param": [category_param]}
            ]
        }
        
        return self._post_request(url, body)

    # 일반 검색 API 헬퍼 함수
    def _search_api(self, endpoint: str, query: str, display: int = 100):
        url = f"https://openapi.naver.com/v1/search/{endpoint}.json"
        params = {
            "query": query,
            "display": display,
            "start": 1,
            "sort": "date" # 최신순 정렬
        }
        return self._get_request(url, params)

    # 3. 블로그 검색
    def search_blog(self, query: str, display: int = 100):
        return self._search_api("blog", query, display)

    # 4. 뉴스 검색
    def search_news(self, query: str, display: int = 100):
        return self._search_api("news", query, display)

    # 5. 카페글 검색
    def search_cafearticle(self, query: str, display: int = 100):
        return self._search_api("cafearticle", query, display)

    # 6. 쇼핑 검색
    def search_shopping(self, query: str, display: int = 100):
        return self._search_api("shop", query, display)
