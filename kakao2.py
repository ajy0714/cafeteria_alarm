import requests
import json
from bs4 import BeautifulSoup

menuDate='2022-05-23'

url = 'https://sfmn.shinsegaefood.com/selectTodayMenu2.do'
headers = {"Referer": "https://sfmn.shinsegaefood.com/selectTodayMenu.do?storeCd=05859&cafeCd=01&userLang=K&dispBaseCd=0"}
body = {
    "storeCd": "05859",
    "cafeCd": "01",
    "userLang": "K",
    "dispBaseCd": "0",
    "mealTypeCd": "",
    "menuDate": menuDate.replace('-','')
}

response = requests.post(url, headers=headers, json=body)
response.encoding = 'utf-8'
REP_MENU_CD = json.loads(response.text)['model']['model'][0]['REP_MENU_CD']


menu_url = 'https://sfmn.shinsegaefood.com/selectTodayMenuDetail.do' #메뉴에 대한 구체적인 정보를 받아올 때 사용
headers = {"Referer": "https://sfmn.shinsegaefood.com/selectTodayMenu.do?storeCd=05859&cafeCd=01&userLang=K&dispBaseCd=0"}

#params 규칙은 아직 잘 모르겠다. 우선, 삼환빌딩 구내식당만 해당됨.
#repMenuCd를 오늘의 메뉴를 클릭하고, 일자별로 클릭했을 때 selectTodayMenu2.do로 request를 보내서 받아오는 형태인 듯
params = {
    "storeCd": "05859",
    "dispBaseCd": "0",
    "userLang": "K",
    "mealTypeCd": "20",
    "dinnerTypeCd": "001",
    "menuDate": menuDate,
    "repMenuCd": REP_MENU_CD,
    "cafeCd": "01"
}

response = requests.get(menu_url, headers=headers, params=params)
response.encoding = 'utf-8'

#받아온 데이터를 파싱하기 위해 soup라는 객체에 내용 담기
soup = BeautifulSoup(response.text, 'html.parser')

thumbnail_img=soup.find('img')
thumbnail_img=thumbnail_img['src']
material=soup.select('.tit_material')
calorie=soup.select('.txt_kcal')

items=[]
content_description=''
for i in range(len(material)):
    dict = {}
    dict['item']=material[i].text
    dict['item']=dict['item'].replace(' ','')
    dict['item_op']=calorie[i].text
    items.append(dict)

    if (i>0):
        content_description = content_description + dict['item'] + ', '

content_description=content_description[:-2]

print(items[0]['item'])

#카카오 API에게 요청을 던질 내용 작성
data = {}
data['template_id'] = 77323
# params['receiver_uuids'] = '["abcdefg0001"]' #향후 친구에게 보내기 기능 사용할 때
data['template_args']  = json.dumps({
    "img_url": "https://sfmn.shinsegaefood.com/"+thumbnail_img,
    "itemTitle_1": items[0]['item'],
    "itemDesc_1": items[0]['item_op'],
    "itemTitle_2": items[1]['item'],
    "itemDesc_2": items[1]['item_op'],
    "itemTitle_3": items[2]['item'],
    "itemDesc_3": items[2]['item'],
    "itemTitle_4": items[3]['item'],
    "itemDesc_4": items[3]['item_op'],
    "itemTitle_5": items[4]['item'],
    "itemDesc_5": items[4]['item_op'],
    "title": menuDate+' 메뉴 : '+soup.select('.tit_foodName')[0].text,
    "description": content_description,
    "total_key": "총 kcal량",
    "total_value": soup.select('.txt_kcal_total')[0].text
})


# data['template_args'] = json.dumps({
#     # "object_type": "feed",
#     "content": {
#         "title": menuDate+' 메뉴 : '+soup.select('.tit_foodName')[0].text,
#         "description": content_description,
#         "image_url": "https://sfmn.shinsegaefood.com/"+thumbnail_img,
#         "image_width": 640,
#         "image_height": 640,
#         "link": {
#             "web_url": "http://www.daum.net",
#             "mobile_web_url": "http://m.daum.net",
#             "android_execution_params": "contentId=100",
#             "ios_execution_params": "contentId=100"
#         }
#     },
#     "item_content": {
#         # "profile_text": menu['REP_MENU_NM'],
#         # "profile_image_url": "https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
#         # "title_image_url": "https://mud-kage.kakao.com/dn/Q2iNx/btqgeRgV54P/VLdBs9cvyn8BJXB3o7N8UK/kakaolink40_original.png",
#         # "title_image_text": "Cheese cake",
#         # "title_image_category": "Cake",
#         "items": items,
#         "sum": "Total",
#         "sum_op": soup.select('.txt_kcal_total')[0].text
#     },
#     # "social": {
#     #     "like_count": 100,
#     #     "comment_count": 200,
#     #     "shared_count": 300,
#     #     "view_count": 400,
#     #     "subscriber_count": 500
#     # },
#     # "buttons": [
#     #     {
#     #         "title": "웹으로 이동",
#     #         "link": {
#     #             "web_url": "http://www.daum.net",
#     #             "mobile_web_url": "http://m.daum.net"
#     #         }
#     #     },
#     #     {
#     #         "title": "앱으로 이동",
#     #         "link": {
#     #             "android_execution_params": "contentId=100",
#     #             "ios_execution_params": "contentId=100"
#     #         }
#     #     }
#     # ]
# })


#카카오 api에 요청
with open("kakao_code.json", "r") as fp:
    tokens = json.load(fp)

headers = {
    "Authorization": "Bearer " + tokens['access_token'],
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post("https://kapi.kakao.com/v2/api/talk/memo/send", headers=headers, data=data)

if response.json().get('result_code') == 0:
    print('메시지를 성공적으로 보냈습니다.')
else:
    print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.content))


# 친구에게 보내기 기능
# url = "https://kapi.kakao.com/v1/api/talk/friends"
# header = {"Authorization": 'Bearer ' + tokens['access_token']}
# print(header)

# result = json.loads(requests.get(url, headers=header).text)
# friends_list = result.get("elements")

# print(friends_list)