<template>
  <div class="min-h-screen flex items-center justify-center bg-[#EDF3FF] px-4">
    <Card class="w-full max-w-[400px] p-8 relative">
      <h1 class="text-4xl font-semibold text-gray-900 text-center leading-tight mb-2">注册</h1>
      <p class="text-center text-gray-600 text-sm mb-6">欢迎加入生活恢复计划</p>
      <form @submit.prevent="onRegister">
        <div class="mb-4">
          <label for="username" class="block text-gray-700 text-sm mb-1">用户名</label>
          <Input id="username" v-model="username" placeholder="请输入用户名" aria-required="true" />
        </div>
        <div class="mb-4">
          <label for="password" class="block text-gray-700 text-sm mb-1">密码</label>
          <Input id="password" v-model="password" type="password" placeholder="请输入密码" aria-required="true" />
        </div>
        <!-- 错误提示示例 -->
        <!-- <p class="mt-1 text-red-500 text-xs">用户名或密码错误</p> -->
        <Button type="primary" block class="mt-6" :disabled="loading">
          <span v-if="!loading">注册</span>
          <span v-else class="animate-pulse">注册中...</span>
        </Button>
      </form>
      <div class="mt-6 flex items-center justify-center text-sm text-gray-600">
        <span>已有账号？</span>
        <router-link to="/login" class="ml-2 px-3 py-1 border border-indigo-500 text-indigo-500 rounded-full hover:bg-indigo-50 transition">登录</router-link>
      </div>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { userApi } from '../api/index.js'
import Card from '../components/Card.vue'
import Button from '../components/Button.vue'
import Input from '../components/Input.vue'
const username = ref('')
const password = ref('')
const loading = ref(false)
const router = useRouter()

async function onRegister() {
  if (!username.value.trim() || !password.value.trim()) return
  loading.value = true
  try {
    await userApi.register(username.value.trim(), password.value)
    router.push('/login')
  } catch (error) {
    console.error('Register error:', error)
    alert(error.message || '注册失败，请稍后再试')
  } finally {
    loading.value = false
  }
}
</script> 