import os
from datetime import timedelta

import isodate
from googleapiclient.discovery import build


class PlayList:

    api_key = os.getenv('YT_API_KEY')
    youtube = build("youtube", "v3", developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist = self.youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails, snippet',
                                                          maxResults=50,).execute()
        self.title = self.playlist["items"][0]["snippet"]["title"].split(".")[0]
        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlist['items']]
        self.url = f"https://www.youtube.com/playlist?list={playlist_id}"
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                         id=','.join(self.video_ids)).execute()

    @property
    def total_duration(self):
        duration = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def show_best_video(self):
        max_like = 0
        link = ""
        for video in self.video_ids:
            video_resp = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                    id=video).execute()
            like_count: int = video_resp['items'][0]['statistics']['likeCount']
            if int(like_count) > int(max_like):
                max_like = like_count
                link = f"https://youtu.be/{video}"
        return link
