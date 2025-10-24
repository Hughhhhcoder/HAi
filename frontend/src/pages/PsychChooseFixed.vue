<template>
  <div style="min-height: calc(100vh - 4rem); background: linear-gradient(135deg, #f3e8ff 0%, #e9d5ff 100%); padding: 2rem 1rem;">
    <div style="max-width: 64rem; margin: 0 auto;">
      <!-- 标题 -->
      <div v-if="currentStep === 'choose'" style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
          选择 <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">心理测评</span>
        </h1>
        <p style="font-size: 1.125rem; color: #6b7280; margin-bottom: 2rem;">10种专业量表，全面了解您的心理状态</p>
        
        <!-- 历史记录按钮 -->
        <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
          <button 
            @click="showTestHistory"
            style="padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 0.75rem; border: none; font-weight: 600; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); display: flex; align-items: center; gap: 0.5rem;"
            @mouseenter="e => { e.target.style.background = 'linear-gradient(135deg, #059669, #047857)'; e.target.style.transform = 'translateY(-2px)'; e.target.style.boxShadow = '0 8px 20px rgba(16, 185, 129, 0.4)'; }"
            @mouseleave="e => { e.target.style.background = 'linear-gradient(135deg, #10b981, #059669)'; e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.3)'; }"
          >
            <svg style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
            📊 查看测评记录
          </button>
        </div>
      </div>
      
      <div v-else-if="currentStep === 'testing'" style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
          <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">心理测评</span>
        </h1>
        <p style="font-size: 1.125rem; color: #6b7280;">请根据您的真实感受选择最符合的答案</p>
      </div>
      
      <div v-else-if="currentStep === 'submitting'" style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
          <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">生成报告</span>
        </h1>
        <p style="font-size: 1.125rem; color: #6b7280;">AI正在为您生成专业的心理评估报告</p>
      </div>
      
      <div v-else-if="currentStep === 'result'" style="text-align: center; margin-bottom: 3rem;">
        <h1 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">
          <span style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">测评结果</span>
        </h1>
        <p style="font-size: 1.125rem; color: #6b7280;">您的心理测评已完成，以下是详细结果</p>
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
            <span style="font-size: 0.875rem; color: #6b7280;">{{ currentQuestionIndex + 1 }} / {{ currentTest.questions_data ? currentTest.questions_data.length : 0 }}</span>
          </div>
          <div style="background: #e5e7eb; border-radius: 0.5rem; height: 0.5rem; overflow: hidden;">
            <div :style="{ width: progressPercentage + '%', background: 'linear-gradient(90deg, #8b5cf6, #3b82f6)', height: '100%', transition: 'width 0.3s' }"></div>
          </div>
        </div>

        <!-- 问题卡片 -->
        <div style="background: white; border-radius: 1rem; padding: 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
          <h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 2rem; line-height: 1.6;">
            {{ currentQuestion }}
          </h3>
          
          <!-- 选项 -->
          <div style="display: flex; flex-direction: column; gap: 0.75rem;">
            <label 
              v-for="(option, index) in currentTest.options" 
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
              {{ option.text }}
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

      <!-- 提交中（正在生成结果） -->
      <div v-if="currentStep === 'submitting'">
        <div style="background: white; border-radius: 1.5rem; padding: 3rem; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); text-align: center;">
          <!-- 加载动画 -->
          <div style="margin-bottom: 2rem;">
            <div style="width: 80px; height: 80px; margin: 0 auto; position: relative;">
              <div style="width: 100%; height: 100%; border: 4px solid #e5e7eb; border-top: 4px solid #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite;"></div>
              <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 2rem;">🧠</div>
            </div>
          </div>
          
          <!-- 标题 -->
          <h2 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">
            正在为您生成结果
          </h2>
          
          <!-- 描述 -->
          <p style="color: #6b7280; margin-bottom: 2rem; line-height: 1.6;">
            AI正在分析您的测评数据，生成专业的心理评估报告<br>
            请稍候，这通常需要几秒钟时间...
          </p>
          
          <!-- 进度指示 -->
          <div style="background: #f3f4f6; border-radius: 0.5rem; padding: 1rem; margin-bottom: 2rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 0.875rem; color: #6b7280;">分析测评数据</span>
              <span style="font-size: 0.875rem; color: #8b5cf6; font-weight: 600;">✓</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 0.875rem; color: #6b7280;">生成AI报告</span>
              <span style="font-size: 0.875rem; color: #8b5cf6; font-weight: 600;">进行中...</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 0.875rem; color: #6b7280;">更新用户画像</span>
              <span style="font-size: 0.875rem; color: #9ca3af;">等待中</span>
            </div>
          </div>
          
          <!-- 提示 -->
          <div style="background: linear-gradient(135deg, #f0f9ff, #e0f2fe); border: 1px solid #bae6fd; border-radius: 0.75rem; padding: 1rem;">
            <p style="font-size: 0.875rem; color: #0369a1; margin: 0;">
              💡 我们的AI正在为您生成个性化的心理评估报告，这将帮助您更好地了解自己的心理状态
            </p>
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
                <div style="font-size: 1.5rem; font-weight: 700; color: #8b5cf6;">{{ testResult.score || testResult.result_details?.main_score || 'N/A' }}</div>
              </div>
              <div>
                <span style="font-size: 0.875rem; color: #6b7280;">等级</span>
                <div style="font-size: 1.5rem; font-weight: 700; color: #10b981;">{{ testResult.result_details?.level || 'N/A' }}</div>
              </div>
            </div>
            <div style="margin-top: 1rem;">
              <span style="font-size: 0.875rem; color: #6b7280;">建议</span>
              <p style="color: #374151; margin-top: 0.5rem; line-height: 1.6;">{{ testResult.result_details?.suggestion || '暂无建议' }}</p>
            </div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;">
              <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                <span style="font-size: 0.75rem; color: #9ca3af;">
                  📅 测评时间：{{ formatTimestamp(testResult.created_at) }}
                </span>
                <span v-if="testResult.updated_at" style="font-size: 0.75rem; color: #9ca3af;">
                  🔄 更新时间：{{ formatTimestamp(testResult.updated_at) }}
                </span>
              </div>
            </div>
          </div>

          <!-- AI报告 -->
          <div v-if="testResult.ai_report" style="background: white; border-radius: 0.75rem; padding: 0; margin-bottom: 2rem; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1); overflow: hidden;">
            <!-- 报告头部 -->
            <div style="background: linear-gradient(135deg, #8b5cf6, #3b82f6); padding: 1.5rem; color: white;">
              <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="width: 2rem; height: 2rem; background: rgba(255, 255, 255, 0.2); border-radius: 0.5rem; display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                  <svg style="width: 1rem; height: 1rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                  </svg>
                </div>
                <h3 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0;">AI 专业评估报告</h3>
              </div>
            </div>
            
            <!-- 报告内容 -->
            <div style="padding: 2rem; color: #1f2937; line-height: 1.7; font-size: 0.95rem; max-height: 500px; overflow-y: auto;">
              <div v-html="renderMarkdown(testResult.ai_report)" style="markdown-content-light"></div>
            </div>
            
            <!-- 报告底部 -->
            <div style="background: #f8fafc; padding: 1rem; border-top: 1px solid #e5e7eb;">
              <p style="font-size: 0.75rem; color: #6b7280; margin: 0; text-align: center;">
                * 本报告由AI生成，仅供参考，不能替代专业医疗建议
              </p>
            </div>
          </div>

          <!-- 操作按钮 -->
          <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 2rem;">
            <button 
              @click="showTestHistory"
              style="padding: 1rem 2rem; background: linear-gradient(135deg, #10b981, #059669); color: white; border-radius: 1rem; border: none; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3); font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;"
              @mouseenter="e => { e.target.style.background = 'linear-gradient(135deg, #059669, #047857)'; e.target.style.transform = 'translateY(-2px)'; e.target.style.boxShadow = '0 8px 20px rgba(16, 185, 129, 0.4)'; }"
              @mouseleave="e => { e.target.style.background = 'linear-gradient(135deg, #10b981, #059669)'; e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 12px rgba(16, 185, 129, 0.3)'; }"
            >
              <svg style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
              📊 测评记录
            </button>
            <button 
              @click="startNewTest"
              style="padding: 1rem 2rem; background: linear-gradient(135deg, #8b5cf6, #3b82f6); color: white; border-radius: 1rem; border: none; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3); font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;"
              @mouseenter="e => { e.target.style.background = 'linear-gradient(135deg, #7c3aed, #2563eb)'; e.target.style.transform = 'translateY(-2px)'; e.target.style.boxShadow = '0 8px 20px rgba(139, 92, 246, 0.4)'; }"
              @mouseleave="e => { e.target.style.background = 'linear-gradient(135deg, #8b5cf6, #3b82f6)'; e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 12px rgba(139, 92, 246, 0.3)'; }"
            >
              <svg style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              继续其他测评
            </button>
            <router-link 
              to="/home"
              style="padding: 1rem 2rem; background: linear-gradient(135deg, #6b7280, #4b5563); color: white; border-radius: 1rem; text-decoration: none; font-weight: 700; transition: all 0.3s; display: inline-flex; align-items: center; gap: 0.5rem; box-shadow: 0 4px 12px rgba(107, 114, 128, 0.3); font-size: 1rem;"
              @mouseenter="e => { e.target.style.background = 'linear-gradient(135deg, #4b5563, #374151)'; e.target.style.transform = 'translateY(-2px)'; e.target.style.boxShadow = '0 8px 20px rgba(107, 114, 128, 0.4)'; }"
              @mouseleave="e => { e.target.style.background = 'linear-gradient(135deg, #6b7280, #4b5563)'; e.target.style.transform = 'translateY(0)'; e.target.style.boxShadow = '0 4px 12px rgba(107, 114, 128, 0.3)'; }"
            >
              <svg style="width: 1.25rem; height: 1.25rem;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
              </svg>
              返回首页
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- 测评记录弹窗 -->
    <div v-if="showHistoryModal" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;" @click="closeHistoryModal">
      <div style="background: white; border-radius: 1rem; width: 90%; max-width: 800px; max-height: 80vh; overflow: hidden; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);" @click.stop>
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid #e5e7eb; background: linear-gradient(135deg, #10b981, #059669); color: white;">
          <h3 style="font-size: 1.25rem; font-weight: 600; margin: 0;">📊 心理测评记录</h3>
          <button @click="closeHistoryModal" style="background: rgba(255, 255, 255, 0.2); border: none; border-radius: 0.5rem; padding: 0.5rem; cursor: pointer; transition: background 0.2s;" @mouseenter="e => e.target.style.background = 'rgba(255, 255, 255, 0.3)'">
            <svg style="width: 1.25rem; height: 1.25rem; color: white;" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div style="display: flex; gap: 2rem; padding: 1.5rem; background: #f8fafc; border-bottom: 1px solid #e5e7eb;">
          <div style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.875rem; color: #6b7280;">总测评数</span>
            <span style="font-size: 1.125rem; font-weight: 600; color: #1f2937;">{{ testHistoryStats.totalTests }}</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 0.25rem;">
            <span style="font-size: 0.875rem; color: #6b7280;">最近测评</span>
            <span style="font-size: 1.125rem; font-weight: 600; color: #1f2937;">{{ testHistoryStats.lastTestTime }}</span>
          </div>
        </div>

        <div style="max-height: 400px; overflow-y: auto; padding: 1rem;">
          <div v-for="(record, index) in testHistoryRecords" :key="index" style="padding: 1rem; border-bottom: 1px solid #f3f4f6; transition: background 0.2s;" @mouseenter="e => e.target.style.background = '#f8fafc'" @mouseleave="e => e.target.style.background = 'white'">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-size: 0.75rem; color: #9ca3af;">{{ formatTimestamp(record.created_at) }}</span>
              <span style="font-size: 0.75rem; padding: 0.25rem 0.5rem; border-radius: 0.375rem; background: #e5e7eb; color: #374151;">{{ record.test_type }}</span>
            </div>
            <div style="margin-top: 0.5rem;">
              <p style="font-size: 0.875rem; color: #374151; line-height: 1.5; margin: 0;">分数：{{ record.score }} | 等级：{{ record.result_details?.level || 'N/A' }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { marked } from 'marked'

const userId = localStorage.getItem('user_id')
const currentStep = ref('choose')
const selectedCategory = ref('all')
const currentTest = ref(null)
const currentQuestionIndex = ref(0)
const selectedOption = ref(null)
const answers = ref([])
const testResult = ref(null)
const isSubmitting = ref(false)
const showHistoryModal = ref(false)
const testHistoryRecords = ref([])
const testHistoryStats = ref({
  totalTests: 0,
  lastTestTime: '暂无'
})

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
  if (!currentTest.value || !currentTest.value.questions_data) return null
  return currentTest.value.questions_data[currentQuestionIndex.value]
})

const progressPercentage = computed(() => {
  if (!currentTest.value || !currentTest.value.questions_data) return 0
  return ((currentQuestionIndex.value + 1) / currentTest.value.questions_data.length) * 100
})

const isLastQuestion = computed(() => {
  if (!currentTest.value || !currentTest.value.questions_data) return false
  return currentQuestionIndex.value === currentTest.value.questions_data.length - 1
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
    const response = await fetch(`/api/psych/questionnaire?test_type=${test.id}`)
    const data = await response.json()
    if (data.questions) {
      // 直接使用后端返回的数据格式
      currentTest.value.questions_data = data.questions
      currentTest.value.options = data.options || []
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
  
  // 推送选项的分数而不是索引
  const selectedScore = currentTest.value.options[selectedOption.value].score
  answers.value.push(selectedScore)
  
  console.log('答题进度:', {
    currentQuestionIndex: currentQuestionIndex.value,
    totalQuestions: currentTest.value.questions_data ? currentTest.value.questions_data.length : 0,
    isLastQuestion: isLastQuestion.value,
    answersCount: answers.value.length,
    answers: answers.value
  })
  
  if (isLastQuestion.value) {
    console.log('最后一题，准备提交')
    await submitTest()
  } else {
    currentQuestionIndex.value++
    selectedOption.value = null
  }
}

const submitTest = async () => {
  if (!userId) return
  
  // 设置加载状态
  isSubmitting.value = true
  currentStep.value = 'submitting'
  
  // 添加调试信息
  console.log('提交测评数据:', {
    user_id: userId,
    test_type: currentTest.value.id,
    answers: answers.value,
    answers_length: answers.value.length,
    questions_length: currentTest.value.questions_data ? currentTest.value.questions_data.length : 0
  })
  
  try {
    const response = await fetch('/api/psych/submit', {
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
      currentStep.value = 'testing' // 返回答题页面
    }
  } catch (e) {
    alert('提交失败：' + (e.message || '请稍后重试'))
    currentStep.value = 'testing' // 返回答题页面
  } finally {
    isSubmitting.value = false
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
  try {
    // 配置marked选项
    marked.setOptions({
      breaks: true,
      gfm: true
    })
    return marked(text)
  } catch (error) {
    console.error('Markdown渲染错误:', error)
    return text.replace(/\n/g, '<br>')
  }
}

const formatTimestamp = (timestamp) => {
  if (!timestamp) return '未知时间'
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diff = now - date
    
    // 如果是今天
    if (diff < 24 * 60 * 60 * 1000 && date.getDate() === now.getDate()) {
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit'
      })
    }
    
    // 如果是昨天
    const yesterday = new Date(now)
    yesterday.setDate(yesterday.getDate() - 1)
    if (date.getDate() === yesterday.getDate() && date.getMonth() === yesterday.getMonth()) {
      return `昨天 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
    }
    
    // 其他情况显示完整日期时间
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    })
  } catch (error) {
    console.error('时间格式化错误:', error)
    return '时间格式错误'
  }
}

const showTestHistory = async () => {
  if (!userId) return
  
  try {
    const response = await fetch(`/api/psych/history?user_id=${userId}`)
    if (!response.ok) throw new Error('Failed to load test history')
    
    const data = await response.json()
    testHistoryRecords.value = data || []
    testHistoryStats.value = {
      totalTests: data.length,
      lastTestTime: data.length > 0 ? formatTimestamp(data[0].created_at) : '暂无'
    }
    showHistoryModal.value = true
  } catch (error) {
    console.error('Error loading test history:', error)
    alert('加载测评记录失败')
  }
}

const closeHistoryModal = () => {
  showHistoryModal.value = false
}

onMounted(() => {
  // 暂时移除登录检查，允许所有用户访问
  console.log('心理测评页面已加载，用户ID:', userId)
})
</script>

<style scoped>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Markdown内容样式 - 浅色主题 */
:deep(.markdown-content-light) {
  color: #1f2937;
}

:deep(.markdown-content-light h1),
:deep(.markdown-content-light h2),
:deep(.markdown-content-light h3),
:deep(.markdown-content-light h4),
:deep(.markdown-content-light h5),
:deep(.markdown-content-light h6) {
  color: #1f2937;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
}

:deep(.markdown-content-light h1) {
  font-size: 1.5rem;
  border-bottom: 2px solid #8b5cf6;
  padding-bottom: 0.75rem;
  color: #8b5cf6;
}

:deep(.markdown-content-light h2) {
  font-size: 1.25rem;
  color: #374151;
  border-left: 4px solid #8b5cf6;
  padding-left: 1rem;
  background: #f8fafc;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
}

:deep(.markdown-content-light h3) {
  font-size: 1.125rem;
  color: #4b5563;
}

:deep(.markdown-content-light p) {
  margin-bottom: 1rem;
  line-height: 1.7;
  color: #374151;
}

:deep(.markdown-content-light ul),
:deep(.markdown-content-light ol) {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}

:deep(.markdown-content-light li) {
  margin-bottom: 0.5rem;
  color: #374151;
}

:deep(.markdown-content-light strong) {
  font-weight: 700;
  color: #8b5cf6;
}

:deep(.markdown-content-light em) {
  font-style: italic;
  color: #6b7280;
}

:deep(.markdown-content-light code) {
  background: #f1f5f9;
  color: #8b5cf6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.375rem;
  font-family: 'Courier New', monospace;
  font-size: 0.875rem;
  font-weight: 600;
}

:deep(.markdown-content-light blockquote) {
  border-left: 4px solid #8b5cf6;
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  font-style: italic;
  color: #6b7280;
  background: #f8fafc;
  padding: 1rem 1.5rem;
  border-radius: 0.5rem;
}

:deep(.markdown-content-light a) {
  color: #8b5cf6;
  text-decoration: none;
  font-weight: 600;
}

:deep(.markdown-content-light a:hover) {
  text-decoration: underline;
}

/* 保持原有的深色主题样式作为备用 */
:deep(.markdown-content) {
  color: white;
}

:deep(.markdown-content h1),
:deep(.markdown-content h2),
:deep(.markdown-content h3),
:deep(.markdown-content h4),
:deep(.markdown-content h5),
:deep(.markdown-content h6) {
  color: white;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
}

:deep(.markdown-content h1) {
  font-size: 1.25rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  padding-bottom: 0.5rem;
}

:deep(.markdown-content h2) {
  font-size: 1.125rem;
}

:deep(.markdown-content h3) {
  font-size: 1rem;
}

:deep(.markdown-content p) {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

:deep(.markdown-content ul),
:deep(.markdown-content ol) {
  margin-bottom: 0.75rem;
  padding-left: 1.5rem;
}

:deep(.markdown-content li) {
  margin-bottom: 0.25rem;
}

:deep(.markdown-content strong) {
  font-weight: 600;
  color: #fbbf24;
}

:deep(.markdown-content em) {
  font-style: italic;
  color: #a78bfa;
}

:deep(.markdown-content code) {
  background: rgba(255, 255, 255, 0.2);
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-family: 'Courier New', monospace;
  font-size: 0.8rem;
}

:deep(.markdown-content blockquote) {
  border-left: 3px solid rgba(255, 255, 255, 0.5);
  padding-left: 1rem;
  margin: 1rem 0;
  font-style: italic;
  color: rgba(255, 255, 255, 0.9);
}
</style>

