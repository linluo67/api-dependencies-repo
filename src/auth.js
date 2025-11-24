// 用户认证服务
class AuthService {
    constructor() {
        this.apiBase = 'https://api.example.com';
        this.token = localStorage.getItem('token');
    }

    // 用户登录 - 外部API调用
    async login(username, password) {
        try {
            const response = await fetch('https://api.github.com/user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                throw new Error('Login failed');
            }

            return await response.json();
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    }

    // 获取用户信息 - 使用axios
    async getUserInfo(userId) {
        const axios = require('axios');
        
        try {
            const response = await axios.get(`https://api.stripe.com/v1/customers/${userId}`, {
                headers: {
                    'Authorization': `Bearer ${process.env.STRIPE_API_KEY}`
                }
            });
            
            return response.data;
        } catch (error) {
            console.error('Failed to get user info:', error);
            return null;
        }
    }

    // 内部API调用 - 无错误处理
    updateProfile(data) {
        fetch('/api/v1/profile', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    // jQuery Ajax调用
    loadUserPreferences() {
        $.ajax({
            url: 'https://api.openai.com/v1/completions',
            method: 'GET',
            headers: {
                'Authorization': 'Bearer sk-xxx',
                'Content-Type': 'application/json'
            },
            success: function(data) {
                console.log('Preferences loaded:', data);
            },
            error: function(xhr, status, error) {
                console.error('Failed to load preferences:', error);
            }
        });
    }
}

// XMLHttpRequest 示例
function sendAnalytics(event) {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'https://analytics.google.com/collect');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(event));
}

module.exports = AuthService;
