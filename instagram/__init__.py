from pydantic import BaseModel
from typing import List, Dict, Optional, TypedDict
from datetime import datetime
import requests

class InstagramMedia(BaseModel):
    id: str
    caption: Optional[str]
    media_url: str
    permalink: str
    media_type: str  # 'IMAGE', 'VIDEO', 'CAROUSEL_ALBUM'
    timestamp: datetime
    like_count: int
    comments_count: int
    view_count: Optional[int]
    children: Optional[List['InstagramMedia']] = None  # Для каруселей

# class InstagramBusinessAccount(BaseModel):
#     id: str
#     username: str
#     stats: AccountStats
#     media: List[InstagramMedia]

class InstagramBusinessAccountBase(BaseModel):
    id: str
    name: str
    username: str

class InstagramAPI:
    BASE_URL = "https://graph.facebook.com/v23.0"
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.session = requests.Session()

        page = self._get_page_id()
        user = self._get_business_account()
        self.id = user.id
        self.username = user.username
        self.name = user.name
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Базовый метод для выполнения запросов"""
        params = params or {}
        params['access_token'] = self.access_token
        
        try:
            response = self.session.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def _get_page_id(self) -> int:
        pages = self._make_request("me/accounts")['data']
        if not pages:
            raise Exception("No Facebook pages found")
        return pages[0]['id']

    def _get_business_account(self) -> InstagramBusinessAccountBase:
        """Полный процесс получения данных бизнес-аккаунта"""
        page_id = self._get_page_id()
        result = self._make_request(
            f"{page_id}",
            params={'fields': 'instagram_business_account{id,name,username}'}
        )
        
        if not result.get('instagram_business_account'):
            raise Exception("No connected Instagram Business account")
            
        return InstagramBusinessAccountBase.model_validate(result['instagram_business_account'])
    def get_media(self) -> [InstagramMedia]:
        # 3. Получаем статистику и медиа
        media_list = self._make_request(
            f"{self.id}",
            params={
                'fields': 'business_discovery.username(' + self.username + '){'
                # 'username,followers_count,media_count,'
                'media.limit(12){id,caption,media_url,permalink,'
                'media_type,timestamp,like_count,comments_count,'
                'view_count,children{media_url,media_type}}}'
            }
        )['business_discovery']['media']['data']
        return [InstagramMedia(**item) for item in media_list]
        
  
if __name__ == "__main__":
    ig = InstagramAPI("")
    print(ig.username)
    media = ig.get_media()
    print(media)
    for m in media:
      print(f"ID: {m.id}\nCaption: {m.caption}")