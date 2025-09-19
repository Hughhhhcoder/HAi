<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
    <div class="max-w-4xl mx-auto">
      <!-- 页面标题 -->
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">心理健康测评</h1>
        <p class="text-lg text-gray-600 mb-2">选择适合的专业量表进行自我评估</p>
        <p class="text-sm text-gray-500">测评结果仅供参考，如有严重心理困扰请寻求专业帮助</p>
      </div>

      <!-- 测评选择卡片 -->
      <div class="grid md:grid-cols-2 gap-8 mb-12">
        <!-- PHQ-9 抑郁自评量表 -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
          <div class="bg-gradient-to-r from-blue-500 to-blue-600 p-6 text-white">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold">PHQ-9</h2>
                <p class="text-blue-100">抑郁自评量表</p>
              </div>
            </div>
            <p class="text-sm text-blue-100">
              评估过去两周的抑郁症状严重程度
            </p>
          </div>
          
          <div class="p-6">
            <div class="space-y-4 mb-6">
              <div class="flex items-start">
                <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">包含9个核心抑郁症状问题</p>
              </div>
              <div class="flex items-start">
                <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">评估情绪低落、兴趣缺失等症状</p>
              </div>
              <div class="flex items-start">
                <div class="w-2 h-2 bg-blue-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">预计完成时间：3-5分钟</p>
              </div>
            </div>
            
            <div class="border-t pt-4 mb-6">
              <h3 class="font-semibold text-gray-800 mb-2">评分说明：</h3>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-green-50 p-2 rounded">
                  <span class="font-medium text-green-700">0-4分：</span>
                  <span class="text-green-600">无/极轻微</span>
                </div>
                <div class="bg-yellow-50 p-2 rounded">
                  <span class="font-medium text-yellow-700">5-9分：</span>
                  <span class="text-yellow-600">轻度</span>
                </div>
                <div class="bg-orange-50 p-2 rounded">
                  <span class="font-medium text-orange-700">10-14分：</span>
                  <span class="text-orange-600">中度</span>
                </div>
                <div class="bg-red-50 p-2 rounded">
                  <span class="font-medium text-red-700">15-27分：</span>
                  <span class="text-red-600">重度</span>
                </div>
              </div>
            </div>
            
            <button 
              @click="startTest('PHQ9')"
              class="w-full bg-blue-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-blue-700 transition-colors"
            >
              开始 PHQ-9 测评
            </button>
          </div>
        </div>

        <!-- GAD-7 焦虑自评量表 -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow">
          <div class="bg-gradient-to-r from-purple-500 to-purple-600 p-6 text-white">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <div>
                <h2 class="text-xl font-bold">GAD-7</h2>
                <p class="text-purple-100">焦虑自评量表</p>
              </div>
            </div>
            <p class="text-sm text-purple-100">
              评估过去两周的焦虑症状严重程度
            </p>
          </div>
          
          <div class="p-6">
            <div class="space-y-4 mb-6">
              <div class="flex items-start">
                <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">包含7个核心焦虑症状问题</p>
              </div>
              <div class="flex items-start">
                <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">评估紧张、担忧、坐立不安等症状</p>
              </div>
              <div class="flex items-start">
                <div class="w-2 h-2 bg-purple-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                <p class="text-sm text-gray-600">预计完成时间：2-4分钟</p>
              </div>
            </div>
            
            <div class="border-t pt-4 mb-6">
              <h3 class="font-semibold text-gray-800 mb-2">评分说明：</h3>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div class="bg-green-50 p-2 rounded">
                  <span class="font-medium text-green-700">0-4分：</span>
                  <span class="text-green-600">无/极轻微</span>
                </div>
                <div class="bg-yellow-50 p-2 rounded">
                  <span class="font-medium text-yellow-700">5-9分：</span>
                  <span class="text-yellow-600">轻度</span>
                </div>
                <div class="bg-orange-50 p-2 rounded">
                  <span class="font-medium text-orange-700">10-14分：</span>
                  <span class="text-orange-600">中度</span>
                </div>
                <div class="bg-red-50 p-2 rounded">
                  <span class="font-medium text-red-700">15-21分：</span>
                  <span class="text-red-600">重度</span>
                </div>
              </div>
            </div>
            
            <button 
              @click="startTest('GAD7')"
              class="w-full bg-purple-600 text-white py-3 px-6 rounded-xl font-semibold hover:bg-purple-700 transition-colors"
            >
              开始 GAD-7 测评
            </button>
          </div>
        </div>
      </div>

      <!-- 测评进行中 -->
      <div v-if="currentTest" class="bg-white rounded-2xl shadow-lg p-8">
        <div class="mb-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-bold text-gray-900">{{ questionnaire.title }}</h2>
            <button 
              @click="cancelTest"
              class="text-gray-500 hover:text-gray-700 p-2"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          
          <!-- 进度条 -->
          <div class="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div 
              class="bg-blue-600 h-2 rounded-full transition-all duration-300"
              :style="{ width: `${(currentQuestionIndex / questionnaire.questions.length) * 100}%` }"
            ></div>
          </div>
          <p class="text-sm text-gray-600">
            问题 {{ currentQuestionIndex + 1 }} / {{ questionnaire.questions.length }}
          </p>
        </div>

        <!-- 当前问题 -->
        <div class="mb-8">
          <h3 class="text-lg font-semibold text-gray-800 mb-6">
            {{ questionnaire.questions[currentQuestionIndex] }}
          </h3>
          
          <!-- 选项 -->
          <div class="space-y-3">
            <div 
              v-for="(option, index) in questionnaire.options"
              :key="index"
              class="flex items-center p-4 border-2 rounded-xl cursor-pointer transition-all"
              :class="selectedAnswer === option.score ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-300'"
              @click="selectedAnswer = option.score"
            >
              <div 
                class="w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center"
                :class="selectedAnswer === option.score ? 'border-blue-500 bg-blue-500' : 'border-gray-300'"
              >
                <div v-if="selectedAnswer === option.score" class="w-2 h-2 bg-white rounded-full"></div>
              </div>
              <span class="font-medium text-gray-800">{{ option.text }}</span>
            </div>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="flex justify-between">
          <button 
            v-if="currentQuestionIndex > 0"
            @click="previousQuestion"
            class="px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors"
          >
            上一题
          </button>
          <div v-else></div>
          
          <button 
            @click="nextQuestion"
            :disabled="selectedAnswer === null"
            class="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ currentQuestionIndex === questionnaire.questions.length - 1 ? '完成测评' : '下一题' }}
          </button>
        </div>
      </div>

      <!-- 测评结果 -->
      <div v-if="testResult" class="bg-white rounded-2xl shadow-lg p-8">
        <div class="text-center mb-8">
          <div class="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center"
               :class="getResultColor(testResult.score).bg">
            <svg class="w-8 h-8" :class="getResultColor(testResult.score).text" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-gray-900 mb-2">测评完成</h2>
          <p class="text-gray-600">您的 {{ currentTest }} 测评结果</p>
        </div>

        <div class="bg-gray-50 rounded-xl p-6 mb-6">
          <div class="text-center mb-4">
            <div class="text-4xl font-bold mb-2" :class="getResultColor(testResult.score).text">
              {{ testResult.score }} 分
            </div>
            <div class="text-lg font-semibold text-gray-700">
              {{ getScoreLevel(currentTest, testResult.score) }}
            </div>
          </div>
          
          <div class="bg-white rounded-lg p-4">
            <h3 class="font-semibold text-gray-800 mb-2">专业建议：</h3>
            <p class="text-gray-700 leading-relaxed">{{ testResult.suggestion }}</p>
          </div>
        </div>

        <div class="flex space-x-4">
          <button 
            @click="restartTest"
            class="flex-1 px-6 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors"
          >
            重新测评
          </button>
          <router-link 
            to="/home"
            class="flex-1 px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition-colors text-center"
          >
            返回首页
          </router-link>
        </div>
      </div>

      <!-- 历史测评记录 -->
      <div v-if="testHistory.length > 0 && !currentTest && !testResult" class="bg-white rounded-2xl shadow-lg p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">历史测评记录</h2>
        <div class="space-y-3">
          <div 
            v-for="record in testHistory.slice(0, 5)" 
            :key="record.id"
            class="flex items-center justify-between p-4 bg-gray-50 rounded-lg"
          >
            <div class="flex items-center space-x-4">
              <div class="w-3 h-3 rounded-full" :class="getResultColor(record.score).bg"></div>
              <div>
                <div class="font-medium text-gray-800">{{ record.test_type }}</div>
                <div class="text-sm text-gray-600">{{ formatDate(record.date) }}</div>
              </div>
            </div>
            <div class="text-right">
              <div class="font-bold" :class="getResultColor(record.score).text">{{ record.score }}分</div>
              <div class="text-xs text-gray-500">{{ getScoreLevel(record.test_type, record.score) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { psychApi } from '../api/index.js'

const userId = localStorage.getItem('user_id')

// 测评状态
const currentTest = ref('')
const questionnaire = ref({})
const currentQuestionIndex = ref(0)
const selectedAnswer = ref(null)
const answers = ref([])
const testResult = ref(null)
const testHistory = ref([])

// 开始测评
const startTest = async (testType) => {
  try {
    const data = await psychApi.getQuestionnaire(testType)
    currentTest.value = testType
    questionnaire.value = data
    currentQuestionIndex.value = 0
    selectedAnswer.value = null
    answers.value = []
    testResult.value = null
  } catch (error) {
    console.error('获取问卷失败:', error)
  }
}

// 取消测评
const cancelTest = () => {
  currentTest.value = ''
  questionnaire.value = {}
  currentQuestionIndex.value = 0
  selectedAnswer.value = null
  answers.value = []
}

// 上一题
const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
    selectedAnswer.value = answers.value[currentQuestionIndex.value] || null
  }
}

// 下一题或完成测评
const nextQuestion = async () => {
  if (selectedAnswer.value === null) return

  // 保存当前答案
  answers.value[currentQuestionIndex.value] = selectedAnswer.value

  if (currentQuestionIndex.value === questionnaire.value.questions.length - 1) {
    // 完成测评，提交结果
    await submitTest()
  } else {
    // 下一题
    currentQuestionIndex.value++
    selectedAnswer.value = answers.value[currentQuestionIndex.value] || null
  }
}

// 提交测评
const submitTest = async () => {
  try {
    const data = await psychApi.submitTest(userId, currentTest.value, answers.value)
    testResult.value = data
    currentTest.value = ''
    loadTestHistory()
  } catch (error) {
    console.error('提交测评失败:', error)
  }
}

// 重新测评
const restartTest = () => {
  testResult.value = null
}

// 加载历史记录
const loadTestHistory = async () => {
  if (!userId) return

  try {
    const data = await psychApi.getHistory(userId)
    testHistory.value = data
  } catch (error) {
    console.error('加载历史记录失败:', error)
  }
}

// 获取分数等级
const getScoreLevel = (testType, score) => {
  if (testType === 'PHQ9') {
    if (score < 5) return '无/极轻微'
    if (score < 10) return '轻度'
    if (score < 15) return '中度'
    if (score < 20) return '中重度'
    return '重度'
  } else if (testType === 'GAD7') {
    if (score < 5) return '无/极轻微'
    if (score < 10) return '轻度'
    if (score < 15) return '中度'
    return '重度'
  }
  return ''
}

// 获取结果颜色
const getResultColor = (score) => {
  if (score < 5) return { bg: 'bg-green-100', text: 'text-green-600' }
  if (score < 10) return { bg: 'bg-yellow-100', text: 'text-yellow-600' }
  if (score < 15) return { bg: 'bg-orange-100', text: 'text-orange-600' }
  return { bg: 'bg-red-100', text: 'text-red-600' }
}

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  loadTestHistory()
})
</script> 