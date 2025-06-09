# imports
from constants import *
from bin.fetch_yt_vid_infomation import fetch_yt_videos_information_for_channel
from bin.fetch_location_for_plotting import generate_folium_map
import pandas as pd
from crew import video_researcher, research_task
from crewai import Crew

rows, errors = list(), list()

# scrapes youtube and stores the information in a csv file [CSV_FILE_PATH]
fetch_yt_videos_information_for_channel(CHANNEL_ID, CSV_FILE_PATH, YOUTUBE_API_KEY)
# load the csv file [CSV_FILE_PATH]
data = pd.read_csv(CSV_FILE_PATH)


# iterate over the rows and get kickoff the crew to get necessary information for plotting
for index, row in data.iterrows():
    crew = Crew(agents=[video_researcher], tasks=[research_task])
    result = crew.kickoff(inputs={"youtube_video_url": row["Link"]})
    try:
        result_dict = eval(result.tasks_output[0].raw)
        rows.append(result_dict)
    except Exception as e:
        errors.append([e, row["Link"]])
        continue

pd.DataFrame(rows).to_csv(CSV_INFO_FILE_PATH, index=False)

from pprint import pprint
pprint(errors)  # fix these videos and append them to the csv file [CSV_INFO_FILE_PATH]
# Errors (as of Monday Jun 9, 2025);
# [[SyntaxError('unterminated string literal (detected at line 4)', ('<string>', 4, 408, "    'Description': 'In this video, I explore the famous Michelin Star street food restaurant, Jay Fai, located in Bangkok. Jay Fai is well-known for her expertise and recognition in the culinary world, attracting various celebrities and even featuring in Netflix shows, earning her the title as the queen of Thai street food. In today's video, we will see if the restaurant truly lives up to its reputation.',", 4, 408)),
#   'https://www.youtube.com/watch?v=z0e7_Nt7qUA'],
#  [SyntaxError('unterminated string literal (detected at line 4)', ('<string>', 4, 347, "    'Description': 'This video highlights a significant giveaway conducted by Alexander, co-owner of a Michelin star restaurant, as the channel reached 300,000 subscribers. The winner, Tuomas Tolsa from Finland, was treated to his first Michelin star dinner experience. Follow Alexander's gastronomical journey and insights through his Instagram.',", 4, 347)),
#   'https://www.youtube.com/watch?v=bC4HCoIkQ6w'],
#  [SyntaxError('unterminated string literal (detected at line 1)', ('<string>', 1, 653, "{'Title': 'I Had a DINNER IN THE SKY by a 2 Michelin Star Chef!', 'Link': 'https://www.youtube.com/watch?v=6Ko8ue4Yz-8', 'Description': 'In this video, I experienced the novel Dinner in the Sky event in Reims, France organized by a 2 Michelin Star chef. The adventure included an exclusive cellar tour at the Charles Heidsieck Champagne House, where I had the unique opportunity to taste one of their premium champagnes both 30 meters below the earth's surface and 50 meters above it, exploring whether the altitude affects the taste.', 'Publish Date': '2024-11-24', 'Location': 'Reims, France', 'Restaurant Visited': 'Charles Heidsieck Champagne House'}", 1, 653)),
#   'https://www.youtube.com/watch?v=6Ko8ue4Yz-8'],
#  [SyntaxError('unterminated string literal (detected at line 1)', ('<string>', 1, 577, "{'Title': 'I GOT INTO the WORLD-FAMOUS Champagne House', 'Link': 'https://www.youtube.com/watch?v=Ka1e5QO8tIU', 'Description': 'The video showcases a rare visit to the prestigious Krug Champagne house, highlighting the exclusive access to their vintage wine cellars and a private meal by a three-star Michelin chef. It also features a champagne tasting and a tour of their vineyards, uncovering the intricate processes behind one of the world's leading champagnes.', 'Publish Date': '2024-10-20', 'Location': 'Krug Champagne House', 'Restaurant Visited': 'Krug Champagne House'}", 1, 577)),
#   'https://www.youtube.com/watch?v=Ka1e5QO8tIU'],
#  [SyntaxError('leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers', ('<string>', 1, 500, "{'Title': 'Luxury Dinner for €530 in Paris - Le Cinq (Four Seasons Hotel George V)', 'Link': 'https://www.youtube.com/watch?v=CD_b8bZxk6g', 'Description': 'Join Alexander for a luxury dining experience at Le Cinq, renowned for its extravagant three-star Michelin menu priced at €530. Located within the opulent Four Seasons Hotel George V in Paris, this dinner emphasizes superior quality and service. Follow Alexander's culinary adventures for more gourmet experiences.', 'Publish Date': '2023-09-22', 'Location': 'Paris, France', 'Restaurant Visited': 'Le Cinq'}", 1, 501)),
#   'https://www.youtube.com/watch?v=CD_b8bZxk6g'],
#  [SyntaxError('leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers', ('<string>', 1, 519, "{'Title': 'I Went to CHINA for This Restaurant - Taian Table (Shanghai) 🇨🇳', 'Link': 'https://www.youtube.com/watch?v=9FbSPG4We0M', 'Description': 'Join Alexander in his journey to Shanghai, China, where he explores the culinary delights of the city which boasts over 100,000 restaurants. In this episode, he visits one of the two 3-Michelin starred restaurants in Shanghai, Taian Table, created by Stefan Stiller. Follow Alexander's gastronomic adventures and his quest for inspiration.', 'Publish Date': '2023-09-04', 'Location': 'Shanghai, China', 'Restaurant Visited': 'Taian Table'}", 1, 520)),
#   'https://www.youtube.com/watch?v=9FbSPG4We0M'],
#  [SyntaxError('unterminated string literal (detected at line 4)', ('<string>', 4, 602, "    'Description': 'Join Alexander, a Michelin-starred restaurant co-owner, as he explores Piazza Duomo, a remarkable establishment helmed by Enrico Crippa. Since its inception in 2005, the restaurant rapidly gained critical acclaim, earning its first Michelin star within a year and achieving three stars by 2011. Known for its prestigious ranking on the world’s 50 Best Restaurants list, Piazza Duomo stands as a testament to high culinary standards. Watch as Chef Crippa and his team showcase their exceptional skills, solidifying Piazza Duomo's reputation as arguably the best restaurant in Italy.',", 4, 602)),
#   'https://www.youtube.com/watch?v=4tdrMksmbZ0'],
#  [SyntaxError('unterminated string literal (detected at line 7)', ('<string>', 7, 80, "  'Restaurant Visited': 'Le Louis XV - Alain Ducasse at L'Hôtel de Paris Monaco'", 7, 80)),
#   'https://www.youtube.com/watch?v=-RAmiqe2neU'],
#  [SyntaxError('unterminated string literal (detected at line 1)', ('<string>', 1, 607, '{\'Title\': \'€2,222 Lunch with the BEST SERVICE EVER - Mirazur (#1 Restaurant in 2019)\', \'Link\': \'https://www.youtube.com/watch?v=lsZBiroyuCY\', \'Description\': "Join Alexander, a Michelin-starred restaurant co-owner, as he explores one of the most beautiful and acclaimed dining locales, Mirazur, on the Côte d\'Azur. Enjoy his journey through sensory excellence and sublime hospitality, headed by Chef Mauro Colagreco, whose culinary achievements have placed Mirazur among the pinnacle of global dining.", \'Publish Date\': \'2023-04-07\', \'Location\': \'Côte d\'Azur, French Riviera\', \'Restaurant Visited\': \'Mirazur\'}', 1, 607)),
#   'https://www.youtube.com/watch?v=lsZBiroyuCY'],
#  [SyntaxError('leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers', ('<string>', 1, 498, "{'Title': 'This Restaurant has a €100.000.000 Wine Cellar - Enoteca Pinchiorri', 'Link': 'https://www.youtube.com/watch?v=tV2ZaIaLRUM', 'Description': 'Alexander, a co-owner of a Michelin-star restaurant, explores the historic city of Florence and visits Enoteca Pinchiorri. There, he tours a renowned wine cellar housing over 100,000 bottles worth approximately €100 million. Follow Alexander's gastronomic journey as he seeks inspiration in the world of fine dining.', 'Publish Date': '2023-03-31', 'Location': 'Florence', 'Restaurant Visited': 'Enoteca Pinchiorri'}", 1, 499)),
#   'https://www.youtube.com/watch?v=tV2ZaIaLRUM'],
#  [SyntaxError('leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers', ('<string>', 1, 457, "{'Title': 'NOTHING is what it seems in this restaurant - The Fat Duck (Heston Blumenthal)', 'Link': 'https://www.youtube.com/watch?v=Sk9xOktLCqk', 'Description': 'Alexander, co-owner of a Michelin star restaurant, explores The Fat Duck, a culinary institution by Chef Heston Blumenthal, known for its unique guest experience focusing on gastronomic innovation. Visit the Fat Duck's official site for more: https://thefatduck.co.uk/', 'Publish Date': '2023-03-10', 'Location': 'Bray, United Kingdom', 'Restaurant Visited': 'The Fat Duck'}", 1, 458)),
#   'https://www.youtube.com/watch?v=Sk9xOktLCqk']]


# generate folium plot
generate_folium_map(CSV_FILE_PATH, CSV_INFO_FILE_PATH, HTML_MAP_FILE_PATH)