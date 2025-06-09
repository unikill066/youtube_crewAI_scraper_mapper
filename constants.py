# imports
import os, io, sys
from pathlib import Path

# CHANNEL_ID = "UCPs2_fXu_zZIQYI5lslUISg"
CONFIG_DIR = Path(os.getcwd())  # Path(__file__).parent
BIN_DIR = CONFIG_DIR / "bin"
DATA_DIR = CONFIG_DIR / "data"
UTILS_DIR = CONFIG_DIR / "utils"

CSV_FILE_PATH = DATA_DIR / "youtube_videos.csv"  # extracted informtion is stored in this file
CSV_INFO_FILE_PATH = DATA_DIR / "youtube_videos_info.csv"
HTML_MAP_FILE_PATH = DATA_DIR / "restaurant_map_all.html"

# define the channel-id here
CHANNEL_ID = "UCPs2_fXu_zZIQYI5lslUISg"# "UCK6gkTCPYQDf3c8tszhwwGg"     # "UCPs2_fXu_zZIQYI5lslUISg"


from dotenv import load_dotenv
load_dotenv()  # load environment vars
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")