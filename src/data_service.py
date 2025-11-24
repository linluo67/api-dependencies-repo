# -*- coding: utf-8 -*-
"""
数据服务模块 - Python API调用示例
"""

import requests
import urllib.request
import httpx
import aiohttp
import asyncio
import json
from typing import Optional, Dict, Any

class DataService:
    def __init__(self):
        self.base_url = "https://api.example.com"
        self.api_key = "sk-1234567890abcdef"
        
    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """使用requests获取用户数据"""
        try:
            response = requests.get(f"https://api.github.com/users/{user_id}", 
                                 headers={'Authorization': f'token {self.api_key}'})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user data: {e}")
            return None
    
    def create_payment(self, amount: int, currency: str = "usd") -> Dict:
        """Stripe支付API调用 - 有错误处理"""
        try:
            payload = {
                'amount': amount,
                'currency': currency,
                'payment_method_types': ['card']
            }
            
            response = requests.post('https://api.stripe.com/v1/payment_intents',
                                   data=payload,
                                   headers={
                                       'Authorization': f'Bearer {self.api_key}',
                                       'Content-Type': 'application/x-www-form-urlencoded'
                                   })
            
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Payment failed: {response.status_code}")
                
        except Exception as e:
            print(f"Payment creation error: {e}")
            raise
    
    def upload_file_to_s3(self, file_path: str):
        """AWS S3 API调用 - 无错误处理"""
        requests.put('https://api.amazonaws.com/bucket/file.txt',
                    files={'file': open(file_path, 'rb')})
    
    def get_weather_data(self, city: str):
        """使用urllib获取天气数据"""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read())
                return data
        except Exception as e:
            print(f"Weather API error: {e}")
            return {}

class AsyncApiClient:
    """异步API客户端"""
    
    async def fetch_multiple_users(self, user_ids: list):
        """使用httpx并发获取多个用户信息"""
        async with httpx.AsyncClient() as client:
            tasks = []
            for user_id in user_ids:
                task = client.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            return [r.json() if hasattr(r, 'json') else None for r in responses]
    
    async def post_analytics_event(self, event_data: Dict):
        """使用aiohttp发送分析事件"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post('https://analytics.google.com/v4/events',
                                      json=event_data,
                                      headers={'Authorization': 'Bearer ga_token'}) as response:
                    return await response.json()
            except aiohttp.ClientError as e:
                print(f"Analytics error: {e}")
                return None

# 内部API调用函数
def update_user_profile(user_id: str, profile_data: Dict):
    """更新用户资料 - 内部API v1"""
    requests.patch(f"/api/v1/users/{user_id}/profile", json=profile_data)

def get_internal_stats():
    """获取内部统计 - 无版本号"""
    return requests.get("/internal/stats").json()

# 第三方集成
def send_slack_notification(message: str):
    """发送Slack通知"""
    webhook_url = "https://hooks.slack.com/services/YOUR_WORKSPACE/YOUR_CHANNEL/YOUR_SECRET_TOKEN"
    
    payload = {
        'text': message,
        'username': 'bot',
        'icon_emoji': ':robot_face:'
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except:
        return False

# OpenAI API调用
def generate_text(prompt: str) -> str:
    """OpenAI GPT API调用"""
    headers = {
        'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 100
    }
    
    response = requests.post('https://api.openai.com/v1/chat/completions',
                           headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception("OpenAI API call failed")
