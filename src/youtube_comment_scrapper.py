import os
import csv
import re
from googleapiclient.discovery import build
from dotenv import load_dotenv

class YouTubeCommentScraper:
    def __init__(self, api_key=None):
        """Initialize YouTube API client"""
        load_dotenv()
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("❌ API Key not found. Set YOUTUBE_API_KEY in .env file.")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)

    def clean_text(self, text):
        """Remove links, emojis, special chars from comments"""
        text = re.sub(r"http\S+", "", text)  # remove URLs
        text = re.sub(r"[^A-Za-z0-9\s]+", "", text)  # keep only letters/numbers
        return text.strip().lower()

    def get_video_id(self, url):
        """Extract video ID from YouTube URL"""
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            raise ValueError("Invalid YouTube URL")

    def fetch_comments(self, video_url, max_comments=100, save_to_csv=True):
        """Fetch comments and (optionally) save to CSV"""
        video_id = self.get_video_id(video_url)
        comments = []
        next_page_token = None

        while len(comments) < max_comments:
            request = self.youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=25,  # API max
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                text = self.clean_text(comment["textDisplay"])
                author = comment.get("authorDisplayName", "Unknown")
                likes = comment.get("likeCount", 0)
                published = comment.get("publishedAt", "")

                comments.append([text, author, likes, published])

                if len(comments) >= max_comments:
                    break

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        if save_to_csv:
            self.save_to_csv(comments)

        return comments

    def save_to_csv(self, comments, filename="data/comments.csv"):
        """Save comments to CSV file"""
        os.makedirs("../data", exist_ok=True)
        with open("../data/comments.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["comment", "author", "likes", "publishedAt"])
            writer.writerows(comments)
        print(f"✅ Saved {len(comments)} comments to {filename}")


# --------------------------
# Example Run
# --------------------------
if __name__ == "__main__":
    scraper = YouTubeCommentScraper()
    url = "https://www.youtube.com/watch?v=_dottViOJCs"  # Replace with any YouTube URL
    scraper.fetch_comments(url, max_comments=25)
