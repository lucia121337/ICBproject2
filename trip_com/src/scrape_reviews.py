import time
import pandas as pd
from curl_cffi import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

# URL and Headers
url = "https://kr.trip.com/restapi/soa2/34308/getHotelCommentInfo"
headers = {
    "sec-ch-ua": "\"Google Chrome\";v=\"149\", \"Chromium\";v=\"149\", \"Not)A;Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "w-payload-source": "1.0.9@102!Nudtz1KLhCAbOX4SO6An9PKnG2KLOSqZOlbn+6FaG6OaKSbpKET2OSVbOrK2+ET5+rApbbbpOSknKr42+rG2KlqIbEVbKtb5+rbSOEb2KE4p+rKpOr4nKrq/K5bpOSqL+rk/OSKZKrVpQlVROShDKFO3GVd3hbb=",
    "x-ctx-country": "KR",
    "x-ctx-currency": "KRW",
    "x-ctx-locale": "ko-KR",
    "x-ctx-ubt-pageid": "10320668147",
    "x-ctx-ubt-pvid": "7",
    "x-ctx-ubt-sid": "9",
    "x-ctx-ubt-vid": "1754985737191.9877n1SlbHlt",
    "x-ctx-user-recognize": "NON_EU",
    "x-ctx-wclient-req": "0af33fe7acb74bcfe9f82cf404544b46"
}

def get_payload(page_idx):
    return {
        "hotelId": 58635410,
        "commentFilterOptions": {"pageIndex": page_idx, "pageSize": 10, "repeatComment": 1},
        "sceneTypes": ["CommentList"],
        "head": {"platform": "PC", "cver": "0", "cid": "1754985737191.9877n1SlbHlt", "bu": "IBU", "group": "trip", "aid": "", "sid": "", "ouid": "", "locale": "ko-KR", "timezone": "9", "currency": "KRW", "pageId": "10320668147", "vid": "1754985737191.9877n1SlbHlt", "guid": "", "isSSR": False}
    }

def fetch_page(page_idx):
    payload = get_payload(page_idx)
    # curl_cffi의 impersonate 옵션으로 실제 크롬 브라우저처럼 위장하여 요청
    response = requests.post(url, headers=headers, json=payload, impersonate="chrome")
    if response.status_code != 200:
        print(f"Error fetching page {page_idx}: {response.status_code}")
        return None
    data = response.json()
    try:
        group_list = data.get("data", {}).get("groupList", [])
        if not group_list:
            return []
        comments = []
        for group in group_list:
            comments.extend(group.get("commentList", []))
        return comments
    except Exception as e:
        print(f"Error parsing JSON on page {page_idx}: {e}")
        return None

def main():
    print("Trip.com 리뷰 수집을 시작합니다...")
    all_comments = []
    page_idx = 1
    
    # 1. 한 페이지가 정상적으로 수집되는지 확인
    first_page_comments = fetch_page(page_idx)
    if first_page_comments is None or len(first_page_comments) == 0:
        print("첫 페이지 수집 실패 또는 데이터가 없습니다.")
        return
        
    print(f"첫 페이지 수집 성공: {len(first_page_comments)}개의 리뷰 데이터를 가져왔습니다.")
    
    # 첫 페이지 내용 일부 검증
    sample = first_page_comments[0]
    print(f"샘플 리뷰 확인 - 작성자: {sample.get('userInfo', {}).get('nickname')}, 별점: {sample.get('rating')}, 내용: {str(sample.get('content'))[:20]}...")
    
    all_comments.extend(first_page_comments)
    page_idx += 1
    
    # 2. 첫 페이지 정상 수집 이후 전체 페이지 수집 진행 (안전을 위해 최대 50페이지로 제한)
    while True:
        comments = fetch_page(page_idx)
        if comments is None or len(comments) == 0:
            print(f"수집 완료. 더 이상 데이터가 없습니다. (총 {len(all_comments)}개 수집)")
            break
        
        all_comments.extend(comments)
        print(f"페이지 {page_idx} 수집 완료: 누적 {len(all_comments)}개")
        page_idx += 1
        time.sleep(1) # 차단을 피하기 위한 딜레이
        
        if page_idx > 50:
            print("테스트 및 안전을 위해 50페이지까지만 수집합니다.")
            break
            
    # 3. 수집된 데이터를 csv로 저장
    parsed_data = []
    for c in all_comments:
        parsed_data.append({
            "id": c.get("id"),
            "createDate": c.get("createDate"),
            "checkinDate": c.get("checkinDate"),
            "rating": c.get("rating"),
            "content": c.get("content", "").replace('\n', ' ') if c.get("content") else "",
            "roomName": c.get("roomName"),
            "travelTypeText": c.get("travelTypeText")
        })
        
    df = pd.DataFrame(parsed_data)
    save_path = "../data/trip_com_reviews.csv"
    df.to_csv(save_path, index=False, encoding='utf-8-sig')
    print(f"데이터가 성공적으로 '{save_path}' 경로에 저장되었습니다.")

if __name__ == "__main__":
    main()
