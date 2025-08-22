import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Example: Search for videos about "Python Programming"
request = youtube.search().list(
    q="Python programming",
    part="snippet",
    maxResults=10
)
response = request.execute()

# Print video titles
for item in response["items"]:
    print("Title:", item["snippet"]["title"])
    print("Channel:", item["snippet"]["channelTitle"])
    print("-" * 50)
