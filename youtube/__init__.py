from googleapiclient.discovery import build
from pydantic import BaseModel

class YTVideo(BaseModel):
    viewCount: str
    likeCount: str
    commentCount: str

class YoutubeAPI:
    def __init__(self, apiKey: str):
        self.apiKey = apiKey
        self.client = build('youtube', 'v3', developerKey=self.apiKey)
    def getVideoInfo(self, videoID: str) -> YTVideo:
        request = self.client.videos().list(
            part="statistics",
            id=videoID
        )
        response = request.execute()
        if response['items']:
            stats = response['items'][0]['statistics']
            return YTVideo.model_validate(stats)
        else:
            raise Exception("Video not found")

if __name__ == "__main__":
    API_KEY = ""
    api = YoutubeAPI(API_KEY)
    v = api.getVideoInfo("s9bGXXNKCVg")
    print(v)