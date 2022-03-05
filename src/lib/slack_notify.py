# -*- coding: utf-8 -*-
import urllib3

http = urllib3.PoolManager()

def send_slack_message_by_message_body(url, message_body):
    
    try:
        response = http.request(
            'POST',
            url=url,
            headers={'Content-Type': 'application/json'},
            body=message_body,
            timeout=10.0,
        )
        print(response.data)
    except Exception as e:
        raise Exception(f'slack send message by message body error: {str(e)}')
