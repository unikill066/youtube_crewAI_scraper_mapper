# imports
import os, pandas as pd, json, ast, yt_dlp
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool


# tool using yt-dlp
class YouTubeVideoInfoTool(BaseTool):
    name: str = "YouTube Video Info Tool"
    description: str = "Fetches title, description, and publish date for a given YouTube video URL. It is very reliable."

    def _run(self, youtube_video_url: str) -> dict:
        """Use yt-dlp to fetch video metadata."""
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(youtube_video_url, download=False)
                title = info_dict.get('title', 'N/A')
                description = info_dict.get('description', 'N/A')
                publish_date = info_dict.get('upload_date', 'N/A')  # YYYYMMDD
                return {
                    "Title": title,
                    "Link": youtube_video_url,
                    "Description": description,
                    "Publish Date": publish_date,
                    "Location": "Not identified in metadata.",
                    "Restaurant Visited": "Not identified in metadata."
                }
            except Exception as e:
                return {"error": str(e)}


youtube_info_tool = YouTubeVideoInfoTool()

# agent 
video_researcher = Agent(
    role="Video Researcher",
    goal="Extract relevant information like Title, Link, Description, Publish Date, Location and the restaurant the host visited.",
    backstory="An expert researcher who specializes in analyzing YouTube video content and its metadata.",
    tools=[youtube_info_tool], # Use the new tool
    verbose=True,
)

# task
research_task = Task(
    description="Use your tool to extract information about the Title, Link, Description, Publish Date, Location and Restaurant visited in the YouTube video at the URL: {youtube_video_url}",
    expected_output="A dictionary summary of the Title, Link, rephrase the Description, Publish Date, Location and the name of the Restaurant Visited.",
    agent=video_researcher,
)