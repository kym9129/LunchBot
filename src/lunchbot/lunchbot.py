#!/usr/bin/env python
# coding: utf-8

import os
import sys
from random import sample
import json

file_path = os.path.realpath(__file__)
directory_path = os.path.dirname(file_path)
sys.path.append(os.path.join(directory_path, '../../src/lib'))
sys.path.append(os.path.join(directory_path, '../../src/pf'))

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from slack_notify import send_slack_message_by_message_body

scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
json_file_name = f'''{directory_path}/spreadsheet_access_key.json''' # 구글 api에서 받은 json파일 연결
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = '구글시트 공유 url 삽입'
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('시트명')

# 엑셀 모든 데이터 가져오기
list_of_lists = worksheet.get_all_values()

# 중복 없이 그냥 랜덤으로 3개 선택
idx1, idx2, idx3 = sample(range(1, len(list_of_lists)-1), 3)

menu_list = []
menu_list.append(list_of_lists[idx1])
menu_list.append(list_of_lists[idx2])
menu_list.append(list_of_lists[idx3])

slack_url = 'https://hooks.slack.com/services/웹훅주소' 

text_list = []
for menu in menu_list:
    # 컬럼 : 가게이름 / 메뉴 / 가격
    restaurant = menu[0]
    menu_name = menu[1]
    price = menu[2]
    text = f'- {restaurant} / *{menu_name}* / {price}원'
    text_list.append(text)
text_list_str = '\n'.join(text_list)


# 메세지 바디 만들기
slack_body = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "오늘의 메뉴 예언",
				"emoji": True
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text_list_str
			},
			"accessory": {
				"type": "image",
				"image_url": "https://pds.joins.com/news/component/joongang_sunday/2011/10/08212015.jpg",
				"alt_text": "alt text for image"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "맛집 정보 추가하기 :point_right::skin-tone-2::point_right::skin-tone-2:"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"text": "맛집 목록",
					"emoji": True
				},
				"value": "click_me_123",
				"url": spreadsheet_url,
				"action_id": "button-action"
			}
		},
		{
			"type": "divider"
		}
	]
}

# 슬랙 전송
send_slack_message_by_message_body(slack_url, json.dumps(slack_body))
