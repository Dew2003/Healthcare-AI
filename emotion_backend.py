from fer import FER
import numpy as np
from ytmusicapi import YTMusic
import requests


emotion_detector = FER()


ytmusic = YTMusic()


motivational_quotes = {
    "happy": [
        "Keep smiling, because life is beautiful!",
        "Happiness is the best makeup.",
        "Every day may not be good, but there is something good in every day.",
        "Stay positive, work hard, make it happen!"
    ],
    "sad": [
        "Tough times never last, but tough people do.",
        "This too shall pass.",
        "Stars can't shine without darkness.",
        "You have to fight through some bad days to earn the best days."
    ],
    "angry": [
        "Holding onto anger is like drinking poison and expecting the other person to die.",
        "For every minute you are angry, you lose sixty seconds of happiness.",
        "Anger is one letter short of danger.",
        "Stay calm; anger won't solve anything."
    ],
    "surprised": [
        "Life is full of surprises, embrace it!",
        "Sometimes the most unexpected moments become the best memories.",
        "Surprises are the joy of life.",
        "Expect the unexpected!"
    ],
    "neutral": [
        "Every moment is a fresh beginning.",
        "This is your reminder to relax and take it easy.",
        "Don’t stress too much. Just do your best.",
        "The best way to predict your future is to create it."
    ]
}

def detect_emotion(image_array):
   
    emotions = emotion_detector.detect_emotions(image_array)
    if emotions:
        top_emotion = emotions[0]['emotions']
        dominant_emotion = max(top_emotion, key=top_emotion.get)
        return dominant_emotion
    return None

def get_motivational_content(emotion):
    
    return np.random.choice(motivational_quotes.get(emotion, motivational_quotes['neutral']))

def get_youtube_music_video(emotion):
   
    emotion_to_search_query = {
        "happy": "funny videos",
        "sad": "uplifting music",
        "angry": "calm music",
        "surprised": "unexpected fun videos",
        "neutral": "relaxing music"
    }

    search_query = emotion_to_search_query.get(emotion, "funny videos")
    search_results = ytmusic.search(search_query, filter='videos')

    if search_results:
        first_result = search_results[0]
        video_title = first_result['title']
        video_url = f"https://www.youtube.com/watch?v={first_result['videoId']}"
        return video_title, video_url

    return None, None

def get_giphy_gif(emotion, api_key):
    
    emotion_to_search_query = {
        "happy": "funny",
        "sad": "cheer up",
        "angry": "calm down",
        "surprised": "wow",
        "neutral": "relaxing"
    }
    
    search_query = emotion_to_search_query.get(emotion, "funny")
    url = f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={search_query}&limit=1"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            gif_url = data['data'][0]['images']['downsized_medium']['url']
            return gif_url
    return None

def enhanced_emotion_recommendations(emotion, giphy_api_key):
    
    
    quote = get_motivational_content(emotion)
    

    video_title, video_url = get_youtube_music_video(emotion)
    
    gif_url = get_giphy_gif(emotion,"LiEMMadcsQ2D6IagiZnpWBBJzjo8oFR9")
    
    return {
        "quote": quote,
        "video_title": video_title,
        "video_url": video_url,
        "gif_url": gif_url
    }
