import requests
import json

menu_url = 'https://sfmn.shinsegaefood.com/selectTodayMenu2.do'
headers = {
    "Referer": "https://sfmn.shinsegaefood.com/selectTodayMenu.do?storeCd=05859&cafeCd=01&userLang=K&dispBaseCd=0",
}
body = {
    "menuDate": "20220527",
    "storeCd": "05859",
    "cafeCd": "01",
    "dispBaseCd": "0",
    "userLang": "K",
    "mealTypeCd": ""
}

response = requests.post(menu_url, headers=headers, json=body)
response.encoding = 'utf-8'
menu = json.loads(response.text)['model']['model'][0]

print(menu)

with open("kakao_code.json", "r") as fp:
    tokens = json.load(fp)

# url = "https://kapi.kakao.com/v1/api/talk/friends"
# header = {"Authorization": 'Bearer ' + tokens['access_token']}
# print(header)

# result = json.loads(requests.get(url, headers=header).text)
# friends_list = result.get("elements")

# print(friends_list)

url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
headers = {
    "Authorization": "Bearer " + tokens['access_token'],
    "Content-Type": "application/x-www-form-urlencoded"
}

params = {}
# params['receiver_uuids'] = '["abcdefg0001"]'
params['template_object'] = json.dumps({
    "object_type": "feed",
        "content": {
            "title": "오늘의 디저트",
            "description": "아메리카노, 빵, 케익",
            "image_url": "https://mud-kage.kakao.com/dn/NTmhS/btqfEUdFAUf/FjKzkZsnoeE4o19klTOVI1/openlink_640x640s.jpg",
            "image_width": 640,
            "image_height": 640,
            "link": {
                "web_url": "http://www.daum.net",
                "mobile_web_url": "http://m.daum.net",
                "android_execution_params": "contentId=100",
                "ios_execution_params": "contentId=100"
            }
        },
        "item_content" : {
            "profile_text" :"Kakao",
            "profile_image_url" :"https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
            "title_image_url" : "https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
            "title_image_text" :"Cheese cake",
            "title_image_category" : "Cake",
            "items" : [
                {
                    "item" :"Cake1",
                    "item_op" : "1000원"
                },
                {
                    "item" :"Cake2",
                    "item_op" : "2000원"
                },
                {
                    "item" :"Cake3",
                    "item_op" : "3000원"
                },
                {
                    "item" :"Cake4",
                    "item_op" : "4000원"
                },
                {
                    "item" :"Cake5",
                    "item_op" : "5000원"
                }
            ],
            "sum" :"Total",
            "sum_op" : "15000원"
        },
        "social": {
            "like_count": 100,
            "comment_count": 200,
            "shared_count": 300,
            "view_count": 400,
            "subscriber_count": 500
        },
        "buttons": [
            {
                "title": "웹으로 이동",
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net"
                }
            },
            {
                "title": "앱으로 이동",
                "link": {
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
            }
        ]
})

response = requests.post(url, headers=headers, params=params)

if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.content))
