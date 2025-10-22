<template>
  <div style="min-height: calc(100vh - 4rem); background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); padding: 2rem 1rem;">
    <div style="max-width: 64rem; margin: 0 auto;">
      <!-- 标题 -->
      <div style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
          选择 <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">心理测评</span>
        </h1>
        <p style="font-size: 1.125rem; color: #6b7280;">10种专业量表，全面了解您的心理状态</p>
      </div>

      <!-- 选择测评（未开始时） -->
      <div v-if="currentStep === 'choose'">
        <!-- 分类标签 -->
        <div style="display: flex; justify-content: center; margin-bottom: 2rem; gap: 0.5rem; flex-wrap: wrap;">
          <button
            v-for="cat in categories"
            :key="cat.id"
            @click="selectedCategory = cat.id"
            :style="getCategoryStyle(cat.id)"
          >
            {{ cat.name }}
          </button>
        </div>

        <!-- 测评卡片网格 -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
          <div 
            v-for="test in filteredTests" 
            :key="test.id"
            @click="startTest(test)"
            style="background: white; border-radius: 1rem; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); cursor: pointer; transition: all 0.3s; border: 2px solid transparent;"
            @mouseenter="e => { e.target.style.transform = 'translateY(-4px)'; e.target.style.boxShadow = '0 20px 25px -5px rgba(0, 0, 0, 0.1)'; }"
            @mouseleave="e => { e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)'; }"
          >
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
              <div :style="{ width: '3rem', height: '3rem', borderRadius: '0.75rem', background: test.gradient, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1.5rem', marginRight: '1rem' }">
                {{ test.icon }}
              </div>
              <div>
                <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 0.25rem;">{{ test.name }}</h3>
                <p style="font-size: 0.875rem; color: #6b7280;">{{ test.description }}</p>
              </div>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div style="display: flex; flex-direction: column; gap: 0.25rem;">
                <span style="font-size: 0.875rem; color: #9ca3af;">{{ test.questions }} 题</span>
                <span style="font-size: 0.75rem; color: #6b7280;">{{ test.time }}</span>
              </div>
              <span style="font-size: 0.875rem; color: #8b5cf6; font-weight: 600;">开始测评 →</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 进行测评（进行中） -->
      <div v-if="currentStep === 'testing'">
        <!-- 进度条 -->
        <div style="background: white; border-radius: 1rem; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h2 style="font-size: 1.5rem; font-weight: 600; color: #1f2937;">{{ currentTest.name }}</h2>
            <span style="font-size: 0.875rem; color: #6b7280;">{{ currentQuestionIndex + 1 }} / {{ currentTest.questions }}</span>
          </div>
          <div style="background: #e5e7eb; border-radius: 0.5rem; height: 0.5rem; overflow: hidden;">
            <div :style="{ width: progressPercentage + '%', background: 'linear-gradient(90deg, #8b5cf6, #3b82f6)', height: '100%', transition: 'width 0.3s' }"></div>
          </div>
        </div>

        <!-- 问题卡片 -->
        <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
          <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 2rem; line-height: 1.6;">
            {{ currentQuestion.text }}
          </h3>
          
          <!-- 选项 -->
          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            <label 
              v-for="(option, index) in currentQuestion.options" 
              :key="index"
              :style="getOptionStyle(index)"
              @click="selectOption(index)"
            >
              <input 
                type="radio" 
                :name="'question_' + currentQuestionIndex" 
                :value="index"
                v-model="selectedOption"
                style="margin-right: 0.75rem;"
              />
              {{ option }}
            </label>
          </div>

          <!-- 导航按钮 -->
          <div style="display: flex; justify-content: space-between; margin-top: 2rem;">
            <button 
              @click="goBack"
              style="padding: 0.75rem 1.5rem; background: #6b7280; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: background 0.2s;"
              @mouseenter="e => e.target.style.background = '#4b5563'"
              @mouseleave="e => e.target.style.background = '#6b7280'"
            >
              返回选择
            </button>
            <button 
              @click="nextQuestion"
              :disabled="selectedOption === null"
              style="padding: 0.75rem 1.5rem; background: #8b5cf6; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s;"
              :style="{ opacity: selectedOption === null ? 0.5 : 1, cursor: selectedOption === null ? 'not-allowed' : 'pointer' }"
              @mouseenter="e => { if (selectedOption !== null) e.target.style.background = '#7c3aed' }"
              @mouseleave="e => { if (selectedOption !== null) e.target.style.background = '#8b5cf6' }"
            >
              {{ isLastQuestion ? '完成测评' : '下一题' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 显示结果（完成后） -->
      <div v-if="currentStep === 'result'">
        <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
          <div style="text-align: center; margin-bottom: 2rem;">
            <div style="width: 4rem; height: 4rem; background: linear-gradient(135deg, #10b981, #059669); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;">
              <svg style="width: 2rem; height: 2rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <h2 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">测评完成</h2>
            <p style="color: #6b7280;">感谢您的参与，以下是您的测评结果</p>
          </div>

          <!-- 结果信息 -->
          <div style="background: #f8fafc; border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem;">
            <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">测评结果</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
              <div>
                <span style="font-size: 0.875rem; color: #6b7280;">总分</span>
                <div style="font-size: 1.5rem; font-weight: 700; color: #8b5cf6;">{{ testResult.total_score }}</div>
              </div>
              <div>
                <span style="font-size: 0.875rem; color: #6b7280;">等级</span>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">{{ testResult.level }}</div>
              </div>
            </div>
            <div style="margin-top: 1rem;">
              <span style="font-size: 0.875rem; color: #6b7280;">建议</span>
              <p style="color: #374151; margin-top: 0.5rem; line-height: 1.6;">{{ testResult.suggestion }}</p>
            </div>
          </div>

          <!-- AI报告 -->
          <div v-if="testResult.ai_report" style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
              <div style="width: 2rem; height: 2rem; background: rgba(255, 255, 255, 0.2); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                <svg style="width: 1rem; height: 1rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 style="font-size: 1.125rem; font-weight: 600; color: white;">AI 专业评估报告</h3>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); border-radius: 0.5rem; padding: 1rem; color: white; line-height: 1.6; font-size: 0.875rem;">
              <div v-html="renderMarkdown(testResult.ai_report)"></div>
            </div>
            <p style="font-size: 0.75rem; color: rgba(255, 255, 255, 0.8); margin-top: 0.75rem; text-align: center;">
              * 本报告由AI生成，仅供参考，不能替代专业医疗建议
            </p>
          </div>

          <!-- 操作按钮 -->
          <div style="display: flex; justify-content: center; gap: 1rem;">
            <button 
              @click="startNewTest"
              style="padding: 0.75rem 1.5rem; background: #8b5cf6; color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: background 0.2s;"
              @mouseenter="e => e.target.style.background = '#7c3aed'"
              @mouseleave="e => e.target.style.background = '#8b5cf6'"
            >
              继续其他测评
            </button>
            <router-link 
              to="/home"
              style="padding: 0.75rem 1.5rem; background: #6b7280; color: white; border-radius: 0.75rem; text-decoration: none; font-weight: 600; transition: background 0.2s; display: inline-block;"
              @mouseenter="e => e.target.style.background = '#4b5563'"
              @mouseleave="e => e.target.style.background = '#6b7280'"
            >
              返回首页
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

const userId = localStorage.getItem('user_id')
const currentStep = ref('choose')
const selectedCategory = ref('all')
const currentTest = ref(null)
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const answers = ref([])
const testResult = ref(null)

const categories = [
  { id: 'all', name: '全部' },
  { id: 'mood', name: '情绪' },
  { id: 'anxiety', name: '焦虑' },
  { id: 'stress', name: '压力' },
  { id: 'personality', name: '人格' },
  { id: 'trauma', name: '创伤' },
]

const tests = [
  {
    id: 'PHQ9',
    name: 'PHQ-9 抑郁自评量表',
    description: '评估过去两周的抑郁症状严重程度',
    category: 'mood',
    questions: 9,
    icon: '😔',
    gradient: 'linear-gradient(135deg, #fbbf24, #f59e0b)',
    time: '3-5分钟'
  },
  {
    id: 'GAD7',
    name: 'GAD-7 焦虑自评量表',
    description: '评估过去两周的焦虑症状严重程度',
    category: 'anxiety',
    questions: 7,
    icon: '😰',
    gradient: 'linear-gradient(135deg, #ef4444, #dc2626)',
    time: '2-4分钟'
  },
  {
    id: 'PSS14',
    name: 'PSS-14 压力知觉量表',
    description: '评估过去一个月的主观压力水平',
    category: 'stress',
    questions: 14,
    icon: '😤',
    gradient: 'linear-gradient(135deg, #f97316, #ea580c)',
    time: '5-7分钟'
  },
  {
    id: 'PANAS',
    name: 'PANAS 积极消极情绪量表',
    description: '评估过去一周的积极和消极情绪状态',
    category: 'mood',
    questions: 20,
    icon: '😊',
    gradient: 'linear-gradient(135deg, #10b981, #059669)',
    time: '5-7分钟'
  },
  {
    id: 'ECR36',
    name: 'ECR-36 亲密关系体验量表',
    description: '评估亲密关系中的依恋风格',
    category: 'personality',
    questions: 36,
    icon: '💕',
    gradient: 'linear-gradient(135deg, #ec4899, #be185d)',
    time: '8-12分钟'
  },
  {
    id: 'IRI28',
    name: 'IRI-28 人际反应指数量表',
    description: '评估共情能力和人际反应倾向',
    category: 'personality',
    questions: 28,
    icon: '🤝',
    gradient: 'linear-gradient(135deg, #8b5cf6, #7c3aed)',
    time: '6-10分钟'
  },
  {
    id: 'RSES',
    name: 'RSES 自尊量表',
    description: '评估整体自尊水平和自我价值感',
    category: 'personality',
    questions: 10,
    icon: '⭐',
    gradient: 'linear-gradient(135deg, #f59e0b, #d97706)',
    time: '3-5分钟'
  },
  {
    id: 'SCS26',
    name: 'SCS-26 自我同情量表',
    description: '评估自我同情和自我关怀能力',
    category: 'personality',
    questions: 26,
    icon: '🤗',
    gradient: 'linear-gradient(135deg, #06b6d4, #0891b2)',
    time: '6-8分钟'
  },
  {
    id: 'MBI22',
    name: 'MBI-22 职业倦怠量表',
    description: '评估工作倦怠的三个维度',
    category: 'stress',
    questions: 22,
    icon: '😴',
    gradient: 'linear-gradient(135deg, #6b7280, #4b5563)',
    time: '5-8分钟'
  },
  {
    id: 'PCL5_20',
    name: 'PCL-5 PTSD检查表',
    description: '评估创伤后应激障碍症状',
    category: 'trauma',
    questions: 20,
    icon: '🛡️',
    gradient: 'linear-gradient(135deg, #dc2626, #991b1b)',
    time: '5-7分钟'
  }
]

const filteredTests = computed(() => {
  if (selectedCategory.value === 'all') return tests
  return tests.filter(test => test.category === selectedCategory.value)
})

const currentQuestion = computed(() => {
  if (!currentTest.value) return null
  return currentTest.value.questions_data[currentQuestionIndex.value]
})

const progressPercentage = computed(() => {
  if (!currentTest.value) return 0
  return ((currentQuestionIndex.value + 1) / currentTest.value.questions) * 100
})

const isLastQuestion = computed(() => {
  return currentQuestionIndex.value === currentTest.value.questions - 1
})

const getCategoryStyle = (categoryId) => {
  const isSelected = selectedCategory.value === categoryId
  return {
    padding: '0.75rem 1.5rem',
    borderRadius: '0.75rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s',
    background: isSelected ? '#8b5cf6' : 'white',
    color: isSelected ? 'white' : '#6b7280',
    border: isSelected ? 'none' : '2px solid #e5e7eb',
  }
}

const getOptionStyle = (index) => {
  const isSelected = selectedOption.value === index
  return {
    padding: '1rem',
    borderRadius: '0.75rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    background: isSelected ? '#f3e8ff' : 'white',
    border: isSelected ? '2px solid #8b5cf6' : '2px solid #e5e7eb',
    color: '#374151',
    display: 'flex',
    alignItems: 'center',
  }
}

const startTest = async (test) => {
  currentTest.value = test
  currentQuestionIndex.value = 0
  selectedOption.value = null
  answers.value = []
  currentStep.value = 'testing'
  
  // 从后端获取测试题目
  try {
    const response = await fetch(`http://localhost:8000/api/psych/categories/${test.id}`)
    const data = await response.json()
    if (data.questions) {
      currentTest.value.questions_data = data.questions
    }
  } catch (error) {
    console.error('获取测试题目失败:', error)
  }
}

const selectOption = (index) => {
  selectedOption.value = index
}

const nextQuestion = async () => {
  if (selectedOption.value === null) return
  
  answers.value.push(selectedOption.value)
  
  if (isLastQuestion.value) {
    await submitTest()
  } else {
    currentQuestionIndex.value++
    selectedOption.value = null
  }
}

const submitTest = async () => {
  if (!userId) return
  
  try {
    const response = await fetch('http://localhost:8000/api/psych/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        test_type: currentTest.value.id,
        answers: answers.value
      })
    })
    
    const result = await response.json()
    if (response.ok) {
      testResult.value = result
      currentStep.value = 'result'
    } else {
      alert('提交失败：' + (result.detail || '请稍后重试'))
    }
  } catch (e) {
    alert('提交失败：' + (e.message || '请稍后重试'))
  }
}

const startNewTest = () => {
  currentStep.value = 'choose'
  currentTest.value = null
  currentQuestionIndex.value = 0
  selectedOption.value = null
  answers.value = []
  testResult.value = null
}

const goBack = () => {
  if (currentStep.value === 'testing') {
    currentStep.value = 'choose'
  } else {
    currentStep.value = 'choose'
  }
}

const renderMarkdown = (text) => {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

onMounted(() => {
  if (!userId) {
    // 重定向到登录页
    window.location.href = '/login'
  }
})
</script>

