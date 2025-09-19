// API配置
// - 在容器/生产中，nginx 将 /api 代理到后端
// - 可通过 VITE_API_BASE 覆盖，默认使用 /api
const API_BASE_URL = (import.meta.env && import.meta.env.VITE_API_BASE) || '/api'

// 通用请求函数
async function apiRequest(url, options = {}) {
  const fullUrl = url.startsWith('http') ? url : `${API_BASE_URL}${url}`
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
  }

  const requestOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  }

  try {
    const response = await fetch(fullUrl, requestOptions)
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Network error' }))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }
    
    return await response.json()
  } catch (error) {
    console.error('API Request Error:', error)
    throw error
  }
}

// 用户相关API
export const userApi = {
  login: (username, password) =>
    apiRequest('/user/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
    
  register: (username, password) =>
    apiRequest('/user/register', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    }),
}

// 打卡相关API
export const checkinApi = {
  dailyCheckin: (userId, mood, sleepHours, completedTasks) =>
    apiRequest('/checkin/daily', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        user_id: userId,
        mood: mood || '',
        sleep_hours: sleepHours?.toString() || '',
        completed_tasks: completedTasks || '',
      }),
    }),
    
  getHistory: (userId) =>
    apiRequest(`/checkin/history?user_id=${userId}`),
}

// AI相关API
export const aiApi = {
  getRoles: () => apiRequest('/ai/roles'),
  
  chat: (userId, roleId, message, imageUrl = null, audioUrl = null) =>
    apiRequest('/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        user_id: userId,
        role_id: roleId.toString(),
        message: message || '',
        image_url: imageUrl || '',
        audio_url: audioUrl || '',
      }),
    }),
    
  getHistory: (userId, roleId, limit = 10) =>
    apiRequest(`/ai/history?user_id=${userId}&role_id=${roleId}&limit=${limit}`),
}

// 心理测试相关API
export const psychApi = {
  getQuestionnaire: (testType) =>
    apiRequest(`/psych/questionnaire?test_type=${testType}`),
    
  submitTest: (userId, testType, answers) =>
    apiRequest('/psych/submit', {
      method: 'POST',
      body: JSON.stringify({
        user_id: parseInt(userId),
        test_type: testType,
        answers: answers,
      }),
    }),
    
  getHistory: (userId, testType = null) => {
    const url = testType 
      ? `/psych/history?user_id=${userId}&test_type=${testType}`
      : `/psych/history?user_id=${userId}`
    return apiRequest(url)
  },
}

// 康复计划相关API
export const planApi = {
  updateProfile: (userId, sleepTime, wakeTime, preferences) =>
    apiRequest('/plan/profile', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        user_id: userId,
        sleep_time: sleepTime || '',
        wake_time: wakeTime || '',
        preferences: preferences || '',
      }),
    }),
    
  getProfile: (userId) =>
    apiRequest(`/plan/profile?user_id=${userId}`),
    
  generatePlan: (userId) =>
    apiRequest('/plan/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        user_id: userId,
      }),
    }),
    
  getHistory: (userId) =>
    apiRequest(`/plan/history?user_id=${userId}`),
}

// 文献相关API
export const literatureApi = {
  upload: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiRequest('/literature/upload', {
      method: 'POST',
      headers: {}, // 让浏览器自动设置Content-Type
      body: formData,
    })
  },
  
  getList: () => apiRequest('/literature/list'),
  
  getChunks: (fileId) =>
    apiRequest(`/literature/chunks?file_id=${fileId}`),
    
  search: (query, topK = 3) =>
    apiRequest(`/literature/search?query=${encodeURIComponent(query)}&top_k=${topK}`),
}

// 奖励相关API
export const rewardsApi = {
  getPoints: (userId) =>
    apiRequest(`/rewards/points?user_id=${userId}`),
    
  getHistory: (userId) =>
    apiRequest(`/rewards/history?user_id=${userId}`),
}

// 上传相关API
export const uploadApi = {
  uploadImage: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiRequest('/upload/image', {
      method: 'POST',
      headers: {}, // 让浏览器自动设置Content-Type
      body: formData,
    })
  },
  
  uploadAudio: (file) => {
    const formData = new FormData()
    formData.append('file', file)
    return apiRequest('/upload/audio', {
      method: 'POST',
      headers: {}, // 让浏览器自动设置Content-Type
      body: formData,
    })
  },
}

export default {
  userApi,
  checkinApi,
  aiApi,
  psychApi,
  planApi,
  literatureApi,
  rewardsApi,
  uploadApi,
} 