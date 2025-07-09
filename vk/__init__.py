import requests
from pydantic import BaseModel
from requests import request


class VKVideo(BaseModel):
    viewCount: int
    likeCount: int
    commentCount: int


class VkVAPI:
    GET_TOKEN_URL = 'https://login.vk.com/?act=get_anonym_token'
    GET_VIDEO_URL = 'https://api.vk.com/method/video.get'
    VERSION_VK_API = '5.254'
    CLIENT_ID = '6287487'
    CLIENT_SECRET = 'QbYic1K3lEV5kTGiqlq2'

    def __init__(self):
        self.session = requests.Session()

        self.apikey = self.get_anonymous_apikey()

    def get_anonymous_apikey(self):
        body_params = {
            "client_secret": self.CLIENT_SECRET,
            "client_id": self.CLIENT_ID
        }
        post_request = self.session.post(url=self.GET_TOKEN_URL,
                                         data=body_params)
        apikey = post_request.json()['data']['access_token']
        return apikey

    @staticmethod
    def format_link(link: str):
        true_link = link.split('clip')[1]
        return true_link

    def getVideoInfo(self, link):
        link = self.format_link(link)
        body_params = {'access_token': self.apikey,
                       'videos': link
                       }
        query_params = {'v': self.VERSION_VK_API, 'client_id': self.CLIENT_ID}
        post_request = self.session.post(self.GET_VIDEO_URL, data=body_params, params=query_params)
        video_json = post_request.json()
        video_static = video_json['response']['items'][0]
        views = video_static['views']
        likes = video_static['likes']['count']
        comments = video_static['comments']
        video_static = VKVideo(viewCount = views,likeCount = likes,commentCount = comments)
        return video_static

vk_api = VkVAPI()
video_static = vk_api.getVideoInfo('https://vk.com/clip-9039989_456240996')
print(video_static.viewCount,video_static.likeCount,video_static.commentCount)

