// TypeScript API客户端
import axios, { AxiosResponse } from 'axios';
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable()
export class ApiClient {
    private baseUrl = 'https://api.twitter.com';
    
    constructor(private http: HttpClient) {}

    // 获取推文列表 - Twitter API v2
    async getTweets(query: string): Promise<any> {
        try {
            const response = await fetch('https://api.twitter.com/2/tweets/search/recent', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${process.env.TWITTER_BEARER_TOKEN}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Error fetching tweets:', error);
            throw error;
        }
    }

    // 使用axios发送数据
    async createPost(data: any): Promise<AxiosResponse> {
        return await axios.post('https://graph.facebook.com/v18.0/me/feed', data, {
            headers: {
                'Authorization': `Bearer ${process.env.FB_ACCESS_TOKEN}`
            }
        });
    }

    // Angular HttpClient示例
    getUserData(id: string) {
        return this.http.get(`/api/v2/users/${id}`);
    }

    // 内部API - 无版本号
    uploadFile(file: File) {
        const formData = new FormData();
        formData.append('file', file);
        
        return this.http.post('/upload', formData);
    }

    // AWS API调用
    async getS3Object(bucket: string, key: string) {
        const response = await fetch(`https://api.amazonaws.com/${bucket}/${key}`, {
            method: 'GET',
            headers: {
                'Authorization': 'AWS4-HMAC-SHA256 ...',
                'x-amz-date': new Date().toISOString()
            }
        });
        
        return response.blob();
    }
}
