# imports
from pytube import YouTube, extract
from googleapiclient.discovery import build
import pandas as pd, re, ast, time, os, googlemaps, json
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound
from dotenv import load_dotenv
load_dotenv()  # load environment vars

def fetch_yt_videos_information_for_channel(CHANNEL_ID, CSV_FILE_PATH, YOUTUBE_API_KEY):

    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    channel_id = CHANNEL_ID

    def get_channel_videos(channel_id):
        request = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        )
        response = request.execute()
        uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

        videos = []
        next_page_token = None
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            videos += response["items"]
            next_page_token = response.get("nextPageToken")
            if next_page_token is None:
                break
        return videos

    def get_video_descriptions(videos):
        descriptions = []
        for video in videos:
            video_id = video["snippet"]["resourceId"]["videoId"]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            descriptions.append({"title": title, "description": description, "video_id": video_id})
        return descriptions

    # Get all videos from the channel
    videos = get_channel_videos(channel_id)

    # Get descriptions of all videos
    descriptions = get_video_descriptions(videos)


    def get_video_details(videos):
        video_details = []
        for video in videos:
            video_id = video["snippet"]["resourceId"]["videoId"]
            title = video["snippet"]["title"]
            description = video["snippet"]["description"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            published_at = video["snippet"]["publishedAt"]
            video_details.append({"Title": title, "Link": link, "Description": description, "PublishedAt": published_at})
        return video_details

    vid_details = get_video_details(videos)
    df = pd.DataFrame(vid_details)

    def extract_links(text):
        # Regular expression to find URLs
        url_pattern = re.compile(r'(https?://\S+)')
        return url_pattern.findall(text)

    df["Links"] = df["Description"].apply(extract_links)


    # Function to extract video ID
    def get_video_id(link):
        return extract.video_id(link)

    # Apply the function to the Link column
    df['video_id'] = df['Link'].apply(get_video_id)


    def extract_and_translate_transcript(youtube_video_url):
        try:
            video_id = youtube_video_url.split("=")[1]
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                return "No transcript available"
            return " ".join(snippet.text for snippet in transcript.fetch()).strip()

        except Exception as e:
            return f"Error: {e}"

    def process_row(row):
        print(f"Extraction - Video: {row.name} | Link: {row.Link}")
        return extract_and_translate_transcript(row['Link'])

    df['transcript'] = df.apply(process_row, axis=1)

    df.to_csv(CSV_FILE_PATH, index=False)

# testing
# if __name__ == "__main__":
#     fetch_yt_videos_information_for_channel(CHANNEL_ID, CSV_FILE_PATH, YOUTUBE_API_KEY)