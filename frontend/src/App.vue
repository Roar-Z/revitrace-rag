<template>
  <div class="app-shell">
    <!-- 深色图标栏：模块切换 -->
    <IconRail
      :view="view"
      :doc-count="documents.length"
      :docs-url="docsUrl"
      @navigate="switchView"
    />

    <!-- 二级侧栏：会话历史 / 文档列表 -->
    <SecondarySidebar
      :view="view"
      :documents="documents"
      @navigate="switchView"
      @new-chat="newChat"
    />

    <!-- 主工作区 -->
    <main class="main-panel">
      <!-- 对话视图 -->
      <template v-if="view === 'chat'">
        <div class="chat-head">
          <div class="chat-head-left">
            <h1 class="chat-title">知识库问答</h1>
            <span class="scope-chip">
              <svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true">
                <path
                  d="M2 3.5C2 2.7 4.7 2 8 2s6 .7 6 1.5v9c0 .8-2.7 1.5-6 1.5s-6-.7-6-1.5v-9Z"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.2"
                />
                <path
                  d="M2 8c0 .8 2.7 1.5 6 1.5s6-.7 6-1.5"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.2"
                />
              </svg>
              {{ scopeText || '暂无文档' }}
            </span>
          </div>

          <div class="chat-tools">
            <button type="button" class="tool-btn" :disabled="!!toolLoading" @click="runSummary">
              {{ toolLoading === 'summary' ? '生成中…' : '考点总结' }}
            </button>
            <button type="button" class="tool-btn" :disabled="!!toolLoading" @click="openCompare">
              {{ toolLoading === 'compare' ? '生成中…' : '知识点对比' }}
            </button>
            <button type="button" class="tool-btn" :disabled="!!toolLoading" @click="runExercise">
              {{ toolLoading === 'exercise' ? '生成中…' : '随堂习题' }}
            </button>
          </div>
        </div>

        <section ref="scrollRef" class="chat-scroll">
          <div class="chat-stream">
            <!-- 空状态 -->
            <div v-if="!messages.length && !sending" class="empty-state">
              <svg class="empty-icon" viewBox="0 0 24 24" width="30" height="30" aria-hidden="true">
                <path
                  d="M7 3h6l4 4v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm6 0v4h4M9 12h6M9 15h4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.4"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
              <h2 class="empty-title">开始知识库问答</h2>
              <p class="empty-desc">
                知识库内的全部文档会统一参与检索，回答会自动标注来源文档与页码。
              </p>

              <div v-if="documents.length" class="prompt-wrap">
                <div class="prompt-label">试试这样问</div>
                <div class="prompt-grid">
                  <button
                    v-for="item in recommended"
                    :key="item.q"
                    type="button"
                    class="prompt-card"
                    @click="sendQuestion(item.q)"
                  >
                    <span class="prompt-main">
                      <span class="prompt-q">{{ item.q }}</span>
                      <span class="prompt-hint">{{ item.hint }}</span>
                    </span>
                    <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
                      <path
                        d="M3 8h9M8 3.5 12.5 8 8 12.5"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="1.3"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                  </button>
                </div>
              </div>

              <button
                v-else
                type="button"
                class="empty-action"
                @click="switchView('kb')"
              >
                前往知识库上传
              </button>
            </div>

            <!-- 对话消息 -->
            <template v-for="message in messages" :key="message.id">
              <ChatMessage
                v-if="message.role !== 'tool'"
                :message="message"
                :doc-names="docNameMap"
                @assist="assist"
              />
              <ToolResultCard v-else :message="message" />
            </template>

            <!-- 等待回答 -->
            <div v-if="sending" class="typing-row">
              <div class="assistant-avatar" aria-hidden="true">R</div>
              <div class="typing">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="typing-text">正在检索原文…</span>
              </div>
            </div>
          </div>
        </section>

        <ChatComposer
          :disabled="sending"
          :scope="scopeText"
          @send="sendQuestion"
        />
      </template>

      <!-- 知识库视图 -->
      <KnowledgeBase
        v-else
        :documents="documents"
        :uploading="uploading"
        @upload="handleUpload"
      />
    </main>

    <!-- 知识点对比：两个输入框 -->
    <el-dialog
      v-model="compareVisible"
      class="compare-dialog"
      title="知识点对比"
      width="440px"
      :close-on-click-modal="false"
    >
      <div class="dialog-field">
        <label>知识点 A</label>
        <el-input v-model="compareForm.conceptA" maxlength="50" placeholder="例如：向量检索" />
      </div>
      <div class="dialog-field">
        <label>知识点 B</label>
        <el-input v-model="compareForm.conceptB" maxlength="50" placeholder="例如：关键词检索" />
      </div>

      <template #footer>
        <el-button @click="compareVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCompare">生成对比</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import IconRail from './components/IconRail.vue'
import SecondarySidebar from './components/SecondarySidebar.vue'
import ChatComposer from './components/ChatComposer.vue'
import ChatMessage from './components/ChatMessage.vue'
import KnowledgeBase from './components/KnowledgeBase.vue'
import ToolResultCard from './components/ToolResultCard.vue'
import { uploadPdf } from './api'
import { baseURL } from './api/request'
import { useConversation } from './composables/useConversation'

const STORAGE_KEY = 'revitrace:documents'

// 文档列表来自上传结果，持久化到 localStorage，刷新后仍可继续使用
function loadDocuments() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]')
    return Array.isArray(saved) ? saved : []
  } catch (error) {
    return []
  }
}

// 当前页面：对话 / 知识库
const view = ref('chat')
const documents = ref(loadDocuments())
const uploading = ref(false)
const scrollRef = ref(null)

const hasDocuments = computed(() => documents.value.length > 0)
const totalChunks = computed(() =>
  documents.value.reduce((sum, doc) => sum + (doc.chunk_count || 0), 0)
)
// 知识库全局问答范围，展示在对话页顶部
const scopeText = computed(() =>
  hasDocuments.value
    ? `${documents.value.length} 个文档 · ${totalChunks.value} 个片段`
    : ''
)
// 统一问答时引用片段来自不同文档，用本地文档列表回填文件名
const docNameMap = computed(() =>
  Object.fromEntries(documents.value.map((doc) => [doc.doc_id, doc.filename]))
)

const {
  messages,
  sending,
  toolLoading,
  sendQuestion,
  assist,
  runSummary,
  runCompare,
  runExercise,
  newChat
} = useConversation(hasDocuments)

const docsUrl = computed(() => `${baseURL}/docs`)

// 空态推荐问题：点击即发问，用于引导首次使用。
// 统一面向整个知识库，不做单份文档指向。
const recommended = [
  { q: '知识库主要讲了什么？', hint: '快速了解内容概览' },
  { q: '有哪些核心知识点需要掌握？', hint: '把握复习重点' },
  { q: '容易混淆的概念有哪些？', hint: '辨析易错概念' },
  { q: '给我举一个实际应用的例子', hint: '结合实例理解' }
]

function saveDocuments() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(documents.value))
  } catch (error) {
    // localStorage 不可用时忽略，不影响本次会话
  }
}

function switchView(name) {
  view.value = name
}

async function handleUpload(file) {
  if (uploading.value) return
  uploading.value = true

  try {
    const data = await uploadPdf(file)
    const doc = {
      doc_id: data.doc_id,
      filename: data.filename,
      pages: data.pages,
      chunk_count: data.chunk_count
    }

    documents.value = [
      doc,
      ...documents.value.filter((item) => item.doc_id !== doc.doc_id)
    ]
    saveDocuments()

    ElMessage.success(`《${doc.filename}》已入库，共 ${doc.chunk_count} 个片段`)
  } catch (error) {
    // 错误提示已由 axios 拦截器统一处理
  } finally {
    uploading.value = false
  }
}

// ---------- 知识点对比弹窗 ----------
const compareVisible = ref(false)
const compareForm = reactive({ conceptA: '', conceptB: '' })

function openCompare() {
  compareForm.conceptA = ''
  compareForm.conceptB = ''
  compareVisible.value = true
}

async function submitCompare() {
  const conceptA = compareForm.conceptA.trim()
  const conceptB = compareForm.conceptB.trim()

  if (!conceptA || !conceptB) {
    ElMessage.warning('请填写两个知识点')
    return
  }

  compareVisible.value = false
  await runCompare(conceptA, conceptB)
}

// 新消息或进入等待状态时，把滚动位置保持在底部
function scrollToBottom() {
  nextTick(() => {
    const el = scrollRef.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

watch(() => messages.value.length, scrollToBottom)
watch(sending, (value) => {
  if (value) scrollToBottom()
})
</script>

<style scoped>
.app-shell {
  display: flex;
  height: 100%;
  background: var(--bg);
  overflow: hidden;
}

/* ---------- 主工作区 ---------- */
.main-panel {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  background: var(--surface);
}

.chat-head {
  display: flex;
  flex: none;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  height: 52px;
  padding: 0 20px;
  background: var(--surface);
  border-bottom: 1px solid var(--line);
}

.chat-head-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.chat-title {
  margin: 0;
  color: var(--ink);
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
}

.scope-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  max-width: 300px;
  padding: 2px 8px;
  overflow: hidden;
  color: var(--muted);
  font-size: 11px;
  white-space: nowrap;
  text-overflow: ellipsis;
  background: var(--surface-soft);
  border: 1px solid var(--line);
  border-radius: 4px;
}

.scope-chip svg {
  flex: none;
  color: var(--faint);
}

.chat-tools {
  display: flex;
  flex: none;
  align-items: center;
  gap: 8px;
}

.tool-btn {
  height: 28px;
  padding: 0 10px;
  color: var(--text);
  font-size: 12px;
  white-space: nowrap;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}

.tool-btn:hover:not(:disabled) {
  color: var(--accent);
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

.tool-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

/* ---------- 对话区 ---------- */
.chat-scroll {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  background: var(--surface);
}

.chat-stream {
  display: flex;
  flex-direction: column;
  gap: 22px;
  min-height: 100%;
  max-width: 820px;
  margin: 0 auto;
  padding: 20px 20px 8px;
}

/* ---------- 空状态 ---------- */
.empty-state {
  max-width: 380px;
  margin: auto;
  padding: 24px 0;
  text-align: center;
}

.empty-icon {
  display: block;
  margin: 0 auto 12px;
  color: #9ca3af;
}

.empty-title {
  margin: 0 0 6px;
  color: var(--ink);
  font-size: 15px;
  font-weight: 600;
  line-height: 1.5;
}

.empty-desc {
  max-width: 380px;
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
}

.empty-action {
  height: 30px;
  margin-top: 14px;
  padding: 0 12px;
  color: var(--accent);
  font-size: 12.5px;
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.empty-action:hover {
  background: #dbeafe;
}

/* ---------- 空态推荐问题 ---------- */
.prompt-wrap {
  max-width: 560px;
  margin: 20px auto 0;
}

.prompt-label {
  margin-bottom: 8px;
  color: var(--faint);
  font-size: 11px;
}

.prompt-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  text-align: left;
}

.prompt-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 11px 13px;
  text-align: left;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
}

.prompt-card:hover {
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

.prompt-main {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.prompt-q {
  color: var(--ink);
  font-size: 13px;
}

.prompt-hint {
  color: var(--faint);
  font-size: 11px;
}

.prompt-card:hover .prompt-q {
  color: var(--accent);
}

.prompt-card svg {
  flex: none;
  color: var(--faint);
  transition: color 0.15s ease;
}

.prompt-card:hover svg {
  color: var(--accent);
}

@media (max-width: 720px) {
  .prompt-grid {
    grid-template-columns: 1fr;
  }
}

/* ---------- 等待回答 ---------- */
.typing-row {
  display: flex;
  gap: 12px;
  align-items: flex-start;
}

.assistant-avatar {
  display: grid;
  flex: none;
  place-items: center;
  width: 26px;
  height: 26px;
  color: var(--accent);
  font-size: 13px;
  font-weight: 600;
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  border-radius: 6px;
}

.typing {
  display: flex;
  align-items: center;
  gap: 5px;
  padding-top: 7px;
}

.dot {
  width: 5px;
  height: 5px;
  background: #c4c9d1;
  border-radius: 50%;
  animation: dot-pulse 1.2s ease-in-out infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.15s;
}

.dot:nth-child(3) {
  animation-delay: 0.3s;
}

.typing-text {
  margin-left: 6px;
  color: var(--faint);
  font-size: 11px;
}

@keyframes dot-pulse {
  0%,
  60%,
  100% {
    opacity: 0.35;
  }
  30% {
    opacity: 1;
  }
}

@media (max-width: 960px) {
  .chat-head {
    padding: 0 16px;
  }

  .scope-chip {
    max-width: 200px;
  }

  .chat-stream {
    padding: 18px 16px 8px;
  }
}

@media (max-width: 720px) {
  .chat-head {
    padding: 0 12px;
    gap: 10px;
  }

  .scope-chip {
    display: none;
  }

  .chat-tools {
    gap: 6px;
  }

  .tool-btn {
    padding: 0 8px;
    font-size: 11.5px;
  }

  .chat-stream {
    padding: 16px 12px 8px;
  }
}
</style>