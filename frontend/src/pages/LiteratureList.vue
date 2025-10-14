<template>
  <div class="min-h-screen bg-gradient-to-br from-teal-50 to-emerald-100 p-6">
    <div class="max-w-5xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">文献库</h1>
        <p class="text-gray-600">上传 PDF/TXT，查看分段与检索（mock）</p>
      </div>

      <!-- 上传 -->
      <div class="bg-white rounded-2xl shadow-lg p-6 mb-8">
        <div class="flex flex-col md:flex-row md:items-center gap-3">
          <input type="file" accept=".pdf,.txt" @change="onPickFile" class="hidden" ref="picker" />
          <button @click="picker.click()" class="px-5 py-3 bg-teal-600 text-white rounded-xl hover:bg-teal-700 transition-colors">选择文件</button>
          <div class="text-sm text-gray-600" v-if="pickedName">已选择：{{ pickedName }}</div>
          <button @click="onUpload" :disabled="!file || isUploading" class="px-5 py-3 bg-emerald-600 text-white rounded-xl hover:bg-emerald-700 transition-colors disabled:opacity-60">
            {{ isUploading ? '上传中...' : '上传' }}
          </button>
          <div class="ml-auto flex-1" />
          <input v-model="searchQuery" type="text" placeholder="输入关键词检索..." class="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500" />
          <button @click="onSearch" class="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-900">检索</button>
        </div>
        <div class="mt-3 text-sm text-gray-500" v-if="uploadMessage">{{ uploadMessage }}</div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 文献列表 -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-xl font-semibold text-gray-800">文献列表</h2>
            <button @click="loadList" class="text-sm text-teal-600 hover:text-teal-700">刷新</button>
          </div>
          <div v-if="files.length === 0" class="text-gray-500 text-sm">暂无文献</div>
          <ul class="divide-y divide-gray-100">
            <li v-for="f in files" :key="f.id" class="py-3 cursor-pointer hover:bg-gray-50 rounded" @click="openFile(f)">
              <div class="flex items-center justify-between">
                <div>
                  <div class="font-medium text-gray-800">{{ f.filename }}</div>
                  <div class="text-xs text-gray-500">类型：{{ f.file_type }} · {{ formatDate(f.upload_time) }}</div>
                </div>
                <div class="text-teal-600 text-sm">查看分段</div>
              </div>
            </li>
          </ul>
        </div>

        <!-- 分段/检索结果 -->
        <div class="bg-white rounded-2xl shadow-lg p-6">
          <div class="flex items-center justify-between mb-3">
            <h2 class="text-xl font-semibold text-gray-800">{{ rightPanelTitle }}</h2>
            <div class="text-sm text-gray-500" v-if="activeFile">文件ID：{{ activeFile.id }}</div>
          </div>
          <div v-if="chunks.length === 0 && searchResults.length === 0" class="text-gray-500 text-sm">选择左侧文件查看分段，或输入关键词检索</div>
          <div v-if="chunks.length > 0" class="space-y-3 max-h-[60vh] overflow-auto">
            <div v-for="c in chunks" :key="c.chunk_index" class="p-3 rounded bg-gray-50 text-gray-800">
              <div class="text-xs text-gray-500 mb-1">第 {{ c.chunk_index + 1 }} 段</div>
              <div class="whitespace-pre-wrap">{{ c.text }}</div>
            </div>
          </div>
          <div v-if="searchResults.length > 0" class="space-y-3 max-h-[60vh] overflow-auto">
            <div v-for="r in searchResults" :key="r.file_id + '-' + r.chunk_index" class="p-3 rounded bg-gray-50 text-gray-800">
              <div class="text-xs text-gray-500 mb-1">文件 {{ r.file_id }} · 段 {{ r.chunk_index + 1 }} · 匹配 {{ r.score }}</div>
              <div class="whitespace-pre-wrap">{{ r.text }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { literatureApi } from '../api/index.js'

const picker = ref(null)
const file = ref(null)
const pickedName = ref('')
const isUploading = ref(false)
const uploadMessage = ref('')

const files = ref([])
const activeFile = ref(null)
const chunks = ref([])

const searchQuery = ref('')
const searchResults = ref([])

const rightPanelTitle = computed(() => {
  if (searchResults.value.length > 0) return '检索结果'
  if (activeFile.value) return `分段 · ${activeFile.value.filename}`
  return '分段 / 检索'
})

async function loadList() {
  files.value = await literatureApi.getList()
}

function onPickFile(e) {
  const f = e.target.files && e.target.files[0]
  if (!f) return
  file.value = f
  pickedName.value = f.name
}

async function onUpload() {
  if (!file.value) return
  isUploading.value = true
  uploadMessage.value = ''
  try {
    const resp = await literatureApi.upload(file.value)
    uploadMessage.value = `上传成功：ID ${resp.file_id}，分段 ${resp.chunks}`
    await loadList()
    chunks.value = []
    searchResults.value = []
    activeFile.value = null
    pickedName.value = ''
    if (picker.value) picker.value.value = ''
    file.value = null
  } catch (e) {
    uploadMessage.value = e.message || '上传失败'
  } finally {
    isUploading.value = false
  }
}

async function openFile(f) {
  activeFile.value = f
  searchResults.value = []
  chunks.value = await literatureApi.getChunks(f.id)
}

async function onSearch() {
  if (!searchQuery.value.trim()) return
  activeFile.value = null
  chunks.value = []
  searchResults.value = await literatureApi.search(searchQuery.value.trim(), 5)
}

function formatDate(ts) {
  try { return new Date(ts).toLocaleString('zh-CN') } catch { return String(ts) }
}

onMounted(loadList)
</script>