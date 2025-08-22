import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load API key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Example video (Python tutorial by freeCodeCamp)
VIDEO_ID = "1tRTWwZ5DIc"

# Fetch comments
request = youtube.commentThreads().list(
    part="snippet",
    videoId=VIDEO_ID,
    maxResults=5,   # get 5 comments for testing
    textFormat="plainText"
)
response = request.execute()

# Print comments
for item in response["items"]:
    comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
    author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
    print(f"{author}: {comment}")
    print("-" * 50)
