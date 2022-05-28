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
    "Authorization": "Bearer " + "hgsf8UksJj4SDyvXyUSPf7efu5usaxtj3d1q6oOyCinJXgAAAYEAxV_m",
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "template_object": json.dumps({
        "object_type": "text",
        "text": menu['MENU_DESC'],
        "link": {
            "web_url": "https://www.google.co.kr/search?q=drone&source=lnms&tbm=nws",
            "mobile_web_url": "https://www.google.co.kr/search?q=drone&source=lnms&tbm=nws"
        }
    })
}

response = requests.post(url, headers=headers, data=data)
if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))
