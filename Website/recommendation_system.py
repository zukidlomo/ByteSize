from dotenv import load_dotenv
import google.generativeai as genai
import os
from typing import List, Dict, Any
import json
from .Video import Video
class LLMEnhancedRecommendationSystem:
    def __init__(self):
        load_dotenv()
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        genai.configure(api_key=google_api_key)
        self.videos: List[Video] = []
        self.add_sample_videos()
    def add_video(self, video: Video):
        self.videos.append(video)
    def add_sample_videos(self):
        sample_videos = [
            Video("Introduction to Python", "Programming"),
            Video("Machine Learning Basics", "AI"),
            Video("Web Development with Django", "Web"),
            Video("Data Structures and Algorithms", "Programming"),
            Video("Deep Learning Fundamentals", "AI"),
            Video("invideo-ai-480 How to Calculate Your Business Funding N 2024-09-14", "Business"),
            Video("invideo-ai-480 Understanding Recursion in Programming_  2024-09-14", "Recursive"),
            Video("invideo-ai-480 Unlock the Power of Pandas in Python! 2024-09-14", "Pandas"),
            Video("invideo-ai-720 How Netflix Knows What You Want to Watch 2024-09-14", "Neflix"),
        ]
        self.videos.extend(sample_videos)
    def like_video(self, video_name: str):
        video = self.get_video_by_name(video_name)
        if video:
            video.add_like()
        else:
            print(f"Video '{video_name}' not found")
    def view_video(self, video_name: str):
        video = self.get_video_by_name(video_name)
        if video:
            video.view()
        else:
            print(f"Video '{video_name}' not found")
    def get_video_by_name(self, video_name: str) -> Video | None:
        return next((video for video in self.videos if video.name == video_name), None)
    def generate_learning_path(self, user_preference: str) -> List[Dict[str, Any]]:
        prompt = f"""
        Based on the user's preference '{user_preference}' ,
        generate a personalized learning path using the following available content:
        {self.videos}
        Consider the following factors when recommending videos:
        1. Relevance to the user's preference
        2. Number of likes and views
        3. How recently the video was last viewed
        Format the response as a JSON array, containing a ranked list of video names, their tags.
        The total duration should not exceed the available time.
        """
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        raw_text = response.text
        learning_path_str = raw_text.replace("```json", "").replace("```", "").strip()
        try:
            learning_path = json.loads(learning_path_str)
            return learning_path
        except json.JSONDecodeError:
            print("Error decoding JSON. Raw response:", raw_text)
            return []
    def get_video_stats(self) -> Dict[str, Dict[str, int]]:
        return {video.name: {"likes": video.likes, "views": video.views} for video in self.videos}
    def get_popular_tags(self, n: int = 3) -> List[str]:
        tag_counts = {}
        for video in self.videos:
            tag_counts[video.tag] = tag_counts.get(video.tag, 0) + video.views
        return sorted(tag_counts, key=tag_counts.get, reverse=True)[:n]
if __name__ == "__main__":
    recommender = LLMEnhancedRecommendationSystem()
    # Simulate some user activity
    recommender.view_video("Introduction to Python")
    # recommender.like_video("Introduction to Python")
    recommender.view_video("Machine Learning Basics")
    # Generate a learning path
    learning_path = recommender.generate_learning_path("AI and Programming")
    print(learning_path)
    