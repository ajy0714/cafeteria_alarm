import requests
import json

# 카카오톡 메시지 API
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "refresh_token",
    "client_id" : "356c3c5dff69df645d994133a139af1c",
    # "redirect_url" : "https://localhost:3000",
    "refresh_token" : "q0Yp52KInnY4bCKZZuq1VN9Iwu7nP2nZJWjuCnnBCisM0wAAAYD7gOyu"
}
response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

# kakao_code.json 파일 저장
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)