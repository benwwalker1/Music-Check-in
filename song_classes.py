#import numpy as np
from twilio.rest import Client
from api_keys import *

class Song(object): #object contining info ab songs

    def __init__(self,json_song,service):
        
        if service == 'Spotify':

            self.id = json_song['track']['id'] #unique track id
            self.name = json_song['track']['name'] #name of track
            self.year = json_song['track']['album']['release_date'] #year of track release
            self.link = json_song['track']['external_urls']['spotify'] #url to share track
            self.duration = json_song['track']['duration_ms'] #duration of song in milliseconds
            self.popularity = json_song['track']['popularity'] #popularity value from 0-100 for song
            self.artists = [] #list of track artists
            json_artists = json_song['track']['artists'] #makes list of artists
            for json_artist in json_artists:
                artist_name = json_artist['name']
                self.artists.append(artist_name)
            
        if service == 'Last.fm':

            self.id = json_song['name'] #unique track id
            self.name = json_song['name'] #name of track
            self.link = json_song['url'] #url to share track
            self.artists = [json_song['artist']['name']] #list of track artists
            #note : missing year,duration,pop,and mult artists
            #possible future implmentation w spotify api to recover

        self.count = 0 #number of times it appears in list
        self.sequential_count = 0 #number of times it repeated

    def display(self,json_song,service):
        print('ID: %d' %(self.id))
        print('Name: %s' %(self.name))

class Song_List(object):

    def __init__(self,json_data,service):

        #go through json file and create song objects
        self.songs = []
        
        if service == 'Spotify':
            for json_song in json_data['items']:  #reversed(json_data['items']): to reverse
                self.songs.append(Song(json_song,service))
        if service == 'Last.fm':
            for json_song in json_data['recenttracks']['track']:
                self.songs.append(Song(json_song,service))
        #count through song list and get frequency of songs
        self.generate_sequential_count()
        self.generate_count()

    def generate_count(self):
        test_songs = self.songs
        id_list = []
        max_count = 0
        for song in test_songs:
            id_list.append(song.id)
        for song_index in range(len(test_songs)):
            song = test_songs[song_index]
            song.count = id_list.count(song.id)
            if song.count > max_count:
                max_count = song.count
                max_ = song
        self.max = max_
    def generate_sequential_count(self):
        test_songs = self.songs
        id_list = []
        max_count = 0
        count = 1
        for song_index in range(len(test_songs)):
            song = test_songs[song_index]
            if song_index != len(test_songs)-1:
                next_song = test_songs[song_index+1]
            else:
                next_song = song

            song.sequential_count = count
            if song.id == next_song.id:  
                count = count + 1
            else:
                count = 1        
            if song.sequential_count > max_count:
                max_count = song.sequential_count
                max_ = song
        self.sequential_max = max_
    def notify(self,user_data):
        sequential = user_data['sequential']
        notification_threshold = user_data['notification_threshold']

        if sequential:
            message = "Hi %s! %s has listened to %s, by %s, %d times in a row. Check in on %s?"
        else:
            message = "Hi %s! %s have listened to %s, by %s, %d times today. Check in on %s?"


        if sequential and self.sequential_max.count >= notification_threshold:
            status_messages = self.send_message(message,user_data)
            
            for message in status_messages:
                print(message)
        if not sequential and self.max.count >= notification_threshold:
            status_messages = self.send_message(message,user_data)
            
            for message in status_messages:
                print(message)
        else:
            for person in user_data['people']:
                print('From: %s To: %s  Msg: No Message Sent' %(user_data['name'],person['name']))

    def send_message(self,message,user_data):
        
        people = user_data['people']
        status_messages = []

        for person in people:

            number = person['number']
            to_name = person['name']
            from_pronoun = user_data['pronoun']
            from_name = user_data['name']
            song_name = self.sequential_max.name
            song_artist = self.sequential_max.artists[0]
            song_count = self.sequential_max.count

            output_message = message %(to_name,from_name,song_name,song_artist,song_count,from_pronoun)

            client = Client(TWILIO_KEY, TWILIO_SECRET)
            client.messages.create(to=number, from_="+12176155850", body=output_message)

            status_messages.append('From: %s To: %s Msg: %s' %(from_name,to_name, output_message))

        return status_messages


    def display(self):
        for song in self.songs:
            string = '%s | %s | %s' %(song.name,song.sequential_count,song.count)
            print(string)
