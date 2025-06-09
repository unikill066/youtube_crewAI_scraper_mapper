# imports
import googlemaps, requests, pandas as pd, os, folium
from folium import Map, FeatureGroup, Marker, Icon
from folium.plugins import Search
from dotenv import load_dotenv
load_dotenv()  # load environment vars

gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAP_API_KEY"))


def fetch_lat_lng_for_restaurant(restaurant, location):
    location_result = gmaps.geocode(f"{restaurant}, {location}")
    if location_result:
        return location_result[0]['geometry']['location']['lat'], location_result[0]['geometry']['location']['lng']
    return None, None

def generate_folium_map(yt_csv_file, info_csv_file, html_map_file):
    yt_data = pd.read_csv(yt_csv_file)
    data = pd.read_csv(info_csv_file, encoding='cp1252')
    merged = pd.merge(data, yt_data[['Link', 'PublishedAt']], on='Link', how='left')
    merged[['Lat', 'Lng']] = merged.apply(lambda row: pd.Series(fetch_lat_lng_for_restaurant(row['Restaurant Visited'], row['Location'])), axis=1)
    merged = merged.dropna(subset=['Lat', 'Lng']).reset_index(drop=True)
    merged['PublishedAt'] = [date[:10] for date in merged['PublishedAt']]

    # folium plot
    center_lat = merged['Lat'].mean()
    center_lng = merged['Lng'].mean()
    m = folium.Map(location=[center_lat+10, center_lng-10], zoom_start=5)
    fg = FeatureGroup().add_to(m)

    for _, row in merged.iterrows():
        lat = row['Lat']
        lng = row['Lng']
        restaurant = row['Restaurant Visited']
        date = row['PublishedAt']
        youtube_url = row['Link']
        address = row['Location']
        description = row['Description']
    
        html = f"""
        <b>Restaurant:</b> {restaurant}<br>
        <b>Publish Date:</b> {date}<br>
        <b>Address:</b> {address}<br>
        <a href="{youtube_url}" target="_blank">
          <i class="fa fa-youtube-play"></i>
        </a>
        <a href="https://www.google.com/maps/search/?api=1&query={lat},{lng}"
           target="_blank">
          Google Maps: {restaurant}
        </a>
        """

        iframe = folium.IFrame(html, width=300, height=200)
        popup = folium.Popup(iframe, max_width=300)
        icon = folium.Icon(prefix='fa', icon='youtube-play', color='red')
        title = folium.Popup(title=restaurant, max_width=300)
        folium.Marker(location=[lat, lng], popup=popup, icon=icon).add_to(fg)

    Search(fg, search_label="Restaurant").add_to(m)
    m.save(html_map_file)