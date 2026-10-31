<template>
  <!-- 用户消息：右对齐气泡 -->
  <div v-if="message.role === 'user'" class="message-row user-row">
    <div class="user-bubble">{{ message.content }}</div>
  </div>

  <!-- 助手消息：头像 + 标准答案 + 溯源 + 辅助理解 -->
  <div v-else class="message-row assistant-row">
    <div class="assistant-avatar" aria-hidden="true">R</div>

    <div class="assistant-main">
      <span class="message-label">标准答案</span>
      <p class="answer-text">{{ message.content }}</p>

      <div v-if="message.citations?.length" class="citations">
        <el-collapse>
          <el-collapse-item name="sources">
            <template #title>
              <span class="collapse-title">
                溯源原文
                <span class="collapse-count">· {{ message.citations.length }} 条</span>
              </span>
            </template>

            <div class="citation-list">
              <article
                v-for="(citation, index) in message.citations"
                :key="`${citation.doc_id}-${citation.chunk_id}-${index}`"
                class="citation"
              >
                <div class="citation-head">
                  <span class="source-doc" :title="citationName(citation.doc_id)">
                    {{ citationName(citation.doc_id) }}
                  </span>
                  <span class="page-tag">第 {{ citation.page }} 页</span>
                  <span class="score">相关度 {{ citation.score }}</span>
                </div>
                <p class="citation-text">{{ citation.text }}</p>
              </article>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="assist-area">
        <!-- 首次辅助理解 -->
        <button
          v-if="!message.analogy"
          type="button"
          class="ghost-btn"
          @click="requestAssist('initial')"
        >
          辅助理解
        </button>

        <!-- 第一层：辅助理解；第二层：再通俗一点后才进入生活类比 -->
        <div v-else class="assist-card" :class="{ 'is-simple': message.analogy.depth === 'simple' }">
          <div class="assist-head">
            <span class="assist-label">
              {{ message.analogy.depth === 'simple' ? '通俗解读' : '辅助理解' }}
            </span>
            <span v-if="message.analogy.depth === 'simple'" class="assist-style">
              {{ message.analogy.styleLabel }}
            </span>
            <button
              v-if="message.analogy.depth === 'simple'"
              type="button"
              class="text-btn switch-btn"
              :disabled="message.analogy.loading"
              @click="requestAssist('switch')"
            >
              换一个类比
            </button>
          </div>

          <p v-if="message.analogy.loading" class="assist-loading">
            {{ message.analogy.depth === 'simple' ? '正在换一种说法…' : '正在整理辅助解读…' }}
          </p>
          <p v-else class="assist-text">{{ message.analogy.text }}</p>

          <button
            v-if="!message.analogy.loading"
            type="button"
            class="text-btn more-btn"
            @click="requestAssist('simpler')"
          >
            再通俗一点
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  message: { type: Object, required: true },
  docNames: { type: Object, default: () => ({}) }
})

const emit = defineEmits(['assist'])

function requestAssist(mode) {
  emit('assist', props.message, mode)
}

// 统一问答下引用可能来自不同文档，用本地文档列表回填文件名
function citationName(docId) {
  return props.docNames?.[docId] || '文档'
}
</script>

<style scoped>
.message-row {
  display: flex;
  width: 100%;
}

.user-row {
  justify-content: flex-end;
}

.user-bubble {
  max-width: 76%;
  padding: 9px 12px;
  color: var(--ink);
  font-size: 13.5px;
  line-height: 1.7;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  background: var(--user-bubble);
  border-radius: 8px;
}

.assistant-row {
  gap: 10px;
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

.assistant-main {
  min-width: 0;
  max-width: 780px;
}

.message-label {
  display: block;
  margin: 0 0 4px;
  color: var(--faint);
  font-size: 11px;
  font-weight: 500;
}

.answer-text {
  margin: 0;
  color: var(--text);
  font-size: 14px;
  line-height: 1.78;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

/* ---------- 溯源原文 ---------- */
.citations {
  margin-top: 12px;
  overflow: hidden;
  background: var(--surface-soft);
  border: 1px solid var(--line);
  border-radius: 8px;
}

.citations :deep(.el-collapse) {
  border: none;
}

.citations :deep(.el-collapse-item__header) {
  height: 36px;
  padding: 0 12px;
  color: var(--muted);
  font-size: 12px;
  line-height: 36px;
  background: transparent;
  border-bottom: none;
}

.citations :deep(.el-collapse-item__wrap) {
  background: transparent;
  border-bottom: none;
}

.citations :deep(.el-collapse-item__content) {
  padding: 0 12px 12px;
}

.citations :deep(.el-collapse-item__arrow) {
  color: var(--faint);
}

.collapse-title {
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.collapse-count {
  color: var(--faint);
}

.citation-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.citation {
  padding-top: 10px;
  border-top: 1px solid #eceff3;
}

.citation:first-child {
  padding-top: 4px;
  border-top: none;
}

.citation-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 5px;
}

.source-doc {
  max-width: 150px;
  overflow: hidden;
  color: var(--muted);
  font-size: 10.5px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.page-tag {
  flex: none;
  padding: 1px 6px;
  color: var(--accent);
  font-size: 10.5px;
  background: var(--accent-soft);
  border-radius: 4px;
}

.score {
  color: var(--faint);
  font-size: 10.5px;
}

.citation-text {
  margin: 0;
  padding-left: 9px;
  color: #4b5563;
  font-size: 12.5px;
  line-height: 1.7;
  overflow-wrap: anywhere;
  border-left: 2px solid var(--line);
}

/* ---------- 辅助理解 ---------- */
.assist-area {
  margin-top: 12px;
}

.ghost-btn {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  color: var(--text);
  font-size: 12px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}

.ghost-btn:hover {
  color: var(--accent);
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

.assist-card {
  padding: 10px 12px;
  background: var(--surface-soft);
  border: 1px solid var(--line);
  border-radius: 8px;
  transition: background 0.2s ease, border-color 0.2s ease;
}

/* 只有第二层“再通俗一点”才使用通俗解读的强调样式 */
.assist-card.is-simple {
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

.assist-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.assist-label {
  color: var(--muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.assist-card.is-simple .assist-label {
  color: var(--accent);
}

.assist-style {
  color: var(--faint);
  font-size: 10.5px;
}

.text-btn {
  padding: 0;
  color: var(--muted);
  font-size: 11.5px;
  background: none;
  border: none;
  cursor: pointer;
}

.text-btn:hover:not(:disabled) {
  color: var(--accent);
}

.text-btn:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

.switch-btn {
  margin-left: auto;
}

.assist-text {
  margin: 0;
  color: var(--text);
  font-size: 13px;
  line-height: 1.75;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.assist-loading {
  margin: 0;
  color: var(--faint);
  font-size: 12.5px;
}

.more-btn {
  display: inline-block;
  margin-top: 7px;
  color: var(--accent);
}

@media (max-width: 720px) {
  .user-bubble {
    max-width: 88%;
  }

  .assistant-main {
    max-width: 100%;
  }
}
</style>
