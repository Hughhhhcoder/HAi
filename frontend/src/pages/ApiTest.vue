<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">API 连接测试</h1>
      
      <div class="grid gap-6">
        <!-- 后端连接测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">后端连接测试</h2>
          <button @click="testPing" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试 Ping
          </button>
          <div v-if="pingResult" class="mt-4 p-4 rounded" :class="pingResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ pingResult.message }}
          </div>
        </div>

        <!-- 用户API测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">用户API测试</h2>
          <button @click="testLogin" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试登录
          </button>
          <div v-if="loginResult" class="mt-4 p-4 rounded" :class="loginResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ loginResult.message }}
          </div>
        </div>

        <!-- AI API测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">AI API测试</h2>
          <button @click="testAiRoles" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试AI角色
          </button>
          <div v-if="aiResult" class="mt-4 p-4 rounded" :class="aiResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ aiResult.message }}
          </div>
        </div>

        <!-- 打卡API测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">打卡API测试</h2>
          <button @click="testCheckin" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试打卡历史
          </button>
          <div v-if="checkinResult" class="mt-4 p-4 rounded" :class="checkinResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ checkinResult.message }}
          </div>
        </div>

        <!-- 心理测试API测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">心理测试API测试</h2>
          <button @click="testPsych" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试问卷获取
          </button>
          <div v-if="psychResult" class="mt-4 p-4 rounded" :class="psychResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ psychResult.message }}
          </div>
        </div>

        <!-- 积分API测试 -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-xl font-semibold mb-4">积分API测试</h2>
          <button @click="testRewards" class="bg-blue-500 text-white px-4 py-2 rounded mr-4">
            测试积分查询
          </button>
          <div v-if="rewardsResult" class="mt-4 p-4 rounded" :class="rewardsResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'">
            {{ rewardsResult.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { userApi, aiApi, checkinApi, psychApi, rewardsApi } from '../api/index.js'

const pingResult = ref(null)
const loginResult = ref(null)
const aiResult = ref(null)
const checkinResult = ref(null)
const psychResult = ref(null)
const rewardsResult = ref(null)

const testPing = async () => {
  try {
    const response = await fetch('/api/ping')
    const data = await response.json()
    pingResult.value = {
      success: true,
      message: `连接成功: ${JSON.stringify(data)}`
    }
  } catch (error) {
    pingResult.value = {
      success: false,
      message: `连接失败: ${error.message}`
    }
  }
}

const testLogin = async () => {
  try {
    const data = await userApi.login('admin', 'admin123')
    loginResult.value = {
      success: true,
      message: `登录成功: ${JSON.stringify(data)}`
    }
  } catch (error) {
    loginResult.value = {
      success: false,
      message: `登录失败: ${error.message}`
    }
  }
}

const testAiRoles = async () => {
  try {
    const data = await aiApi.getRoles()
    aiResult.value = {
      success: true,
      message: `获取AI角色成功: 共${data.length}个角色`
    }
  } catch (error) {
    aiResult.value = {
      success: false,
      message: `获取AI角色失败: ${error.message}`
    }
  }
}

const testCheckin = async () => {
  try {
    const data = await checkinApi.getHistory('1')
    checkinResult.value = {
      success: true,
      message: `获取打卡历史成功: 共${data.length}条记录`
    }
  } catch (error) {
    checkinResult.value = {
      success: false,
      message: `获取打卡历史失败: ${error.message}`
    }
  }
}

const testPsych = async () => {
  try {
    const data = await psychApi.getQuestionnaire('PHQ9')
    psychResult.value = {
      success: true,
      message: `获取问卷成功: ${data.title}, 共${data.questions.length}道题`
    }
  } catch (error) {
    psychResult.value = {
      success: false,
      message: `获取问卷失败: ${error.message}`
    }
  }
}

const testRewards = async () => {
  try {
    const data = await rewardsApi.getPoints('1')
    rewardsResult.value = {
      success: true,
      message: `获取积分成功: ${data.points}分`
    }
  } catch (error) {
    rewardsResult.value = {
      success: false,
      message: `获取积分失败: ${error.message}`
    }
  }
}
</script> 