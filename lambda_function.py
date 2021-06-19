import requests
import json
from song_classes import *
from api_keys import *


USER_AGENT = 'Dataquest'



user_1 = {
        'username': 'test_username',
        'name': 'test_name',
        'pronoun': 'them',
        'password_hash': 'testing123',
        'notification_threshold': 5,
        'sequential': True,
        'people': [
            {'name':'Friend1','number':'+18000000000'},
            {'name':'Friend2','number':'+18000000000'},
            {'name':'Friend3','number':'+18000000000'}
        ]
}

user_2 = {
        'username': 'test_username',
        'name': 'test_name',
        'pronoun': 'them',
        'password_hash': 'testing123',
        'notification_threshold': 5,
        'sequential': True,
        'people': [
            {'name':'Friend1a','number':'+18000000000'},
            {'name':'Friend2a','number':'+18000000000'},
            {'name':'Friend3a','number':'+18000000000'}
        ]
}


users = [user_1,user_2]

def lambda_handler(event, context):
    
    headers = {
        'user-agent': USER_AGENT
    }
    
    for user in users:
        
        username = user['username']
        
        payload = {
            'api_key': LASTFM_KEY,
            'method': 'user.getRecentTracks',
            'format': 'json',
            'user': username,
            'limit': 50,
            'extended': 1
        }
        
        r = requests.get('https://ws.audioscrobbler.com/2.0/', headers=headers, params=payload)
        json_data = r.json()
        songs = Song_List(json_data,'Last.fm')
        
        
        songs.notify(user)
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }



