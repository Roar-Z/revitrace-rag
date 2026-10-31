<template>
  <section class="kb-page">
    <header class="kb-head">
      <div class="kb-head-text">
        <h1>知识库</h1>
        <p>知识库内的全部文档会统一参与问答，回答中会标注来源文档与页码。</p>
      </div>

      <div class="kb-actions">
        <el-input
          v-if="documents.length"
          v-model="keyword"
          class="kb-search"
          size="small"
          placeholder="搜索文档"
          clearable
        />

        <el-upload
          :auto-upload="false"
          :show-file-list="false"
          :disabled="uploading"
          accept=".pdf,application/pdf"
          :on-change="handleChange"
        >
          <el-button type="primary" class="upload-btn" :loading="uploading">
            <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
              <path
                d="M8 3v10M3 8h10"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
            </svg>
            {{ uploading ? '解析中…' : '上传 PDF' }}
          </el-button>
        </el-upload>
      </div>
    </header>

    <div v-if="!documents.length" class="kb-empty">
      <svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true">
        <path
          d="M7 3h6l4 4v13a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1Zm6 0v4h4"
          fill="none"
          stroke="currentColor"
          stroke-width="1.4"
          stroke-linejoin="round"
        />
      </svg>
      <p>还没有文档</p>
      <span>上传 PDF 后，全部文档会统一参与问答</span>
    </div>

    <div v-else class="kb-table">
      <div class="kb-row kb-row-head">
        <span>文档</span>
        <span class="cell-num">页数</span>
        <span class="cell-num">片段</span>
        <span class="cell-status">状态</span>
      </div>

      <div v-for="doc in filteredDocuments" :key="doc.doc_id" class="kb-row">
        <div class="cell-doc">
          <span class="doc-badge">PDF</span>
          <span class="doc-name" :title="doc.filename">{{ doc.filename }}</span>
        </div>
        <span class="cell-num">{{ doc.pages }}</span>
        <span class="cell-num">{{ doc.chunk_count }}</span>
        <div class="cell-status">
          <span class="status-chip">已入库</span>
        </div>
      </div>

      <div v-if="!filteredDocuments.length" class="kb-no-result">
        没有匹配的文档
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  documents: { type: Array, default: () => [] },
  uploading: { type: Boolean, default: false }
})

const emit = defineEmits(['upload'])

const keyword = ref('')

const filteredDocuments = computed(() => {
  const text = keyword.value.trim().toLowerCase()
  if (!text) return props.documents
  return props.documents.filter((doc) => doc.filename.toLowerCase().includes(text))
})

// 选择文件后的本地校验，减少无效请求
function handleChange(uploadFile) {
  const file = uploadFile?.raw
  if (!file) return

  if (!file.name.toLowerCase().endsWith('.pdf')) {
    ElMessage.warning('仅支持 PDF 文件')
    return
  }
  if (file.size > 50 * 1024 * 1024) {
    ElMessage.warning('文件不能超过 50MB')
    return
  }

  emit('upload', file)
}
</script>

<style scoped>
.kb-page {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow-y: auto;
  background: var(--surface);
}

.kb-head {
  display: flex;
  flex: none;
  flex-wrap: wrap;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
  padding: 28px 32px 20px;
}

.kb-head-text {
  min-width: 240px;
}

.kb-head-text h1 {
  margin: 0 0 6px;
  color: var(--ink);
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.kb-head-text p {
  margin: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 1.7;
}

.kb-actions {
  display: flex;
  flex: none;
  align-items: center;
  gap: 10px;
}

.kb-search {
  width: 200px;
}

.kb-search :deep(.el-input__wrapper) {
  min-height: 30px;
  font-size: 12px;
  background: var(--surface-soft);
  box-shadow: 0 0 0 1px var(--line) inset;
}

.upload-btn {
  height: 30px;
  padding: 0 14px;
  font-size: 13px;
  font-weight: 500;
  border-radius: 6px;
}

.upload-btn svg {
  margin-right: 5px;
}

.kb-empty {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 24px 120px;
  color: var(--faint);
  text-align: center;
}

.kb-empty svg {
  margin-bottom: 10px;
  color: #c4c9d1;
}

.kb-empty p {
  margin: 0 0 3px;
  color: var(--text);
  font-size: 13.5px;
}

.kb-empty span {
  font-size: 12.5px;
}

.kb-table {
  margin: 0 32px 32px;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.kb-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 64px 64px 76px;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  border-top: 1px solid #f1f3f6;
}

.kb-row:first-child {
  border-top: none;
}

.kb-row-head {
  padding: 9px 16px;
  background: var(--surface-soft);
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  font-size: 11.5px;
}

.cell-num {
  color: var(--muted);
  font-size: 12px;
  text-align: center;
  font-variant-numeric: tabular-nums;
}

.cell-status {
  text-align: right;
}

.cell-doc {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.doc-badge {
  flex: none;
  width: 28px;
  height: 32px;
  color: #dc2626;
  font-size: 9px;
  font-weight: 600;
  line-height: 32px;
  text-align: center;
  background: #fef5f5;
  border: 1px solid #fde2e2;
  border-radius: 5px;
}

.doc-name {
  overflow: hidden;
  color: var(--ink);
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-chip {
  display: inline-block;
  padding: 1px 8px;
  color: var(--muted);
  font-size: 11px;
  background: var(--surface-muted);
  border-radius: 4px;
}

.kb-no-result {
  padding: 28px 16px;
  color: var(--faint);
  font-size: 12.5px;
  text-align: center;
  border-top: 1px solid #f1f3f6;
}

@media (max-width: 720px) {
  .kb-head {
    padding: 20px 16px 16px;
  }

  .kb-actions {
    width: 100%;
  }

  .kb-search {
    flex: 1;
    width: auto;
  }

  .kb-table {
    margin: 0 16px 20px;
  }

  .kb-row {
    grid-template-columns: minmax(0, 1fr) 48px 48px;
    gap: 8px;
    padding: 10px 12px;
  }

  .cell-status {
    display: none;
  }
}
</style>
