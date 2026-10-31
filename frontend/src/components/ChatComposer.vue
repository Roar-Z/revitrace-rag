<template>
  <div class="composer">
    <div class="composer-inner">
      <div class="input-shell" :class="{ 'is-disabled': disabled }">
        <el-input
          v-model="draft"
          type="textarea"
          resize="none"
          :autosize="{ minRows: 1, maxRows: 5 }"
          :disabled="disabled"
          placeholder="输入你的问题，例如：这份资料的核心结论是什么？"
          @keydown.enter.exact.prevent="submit"
        />

        <el-button
          type="primary"
          class="send-btn"
          :loading="disabled"
          :disabled="!draft.trim() || disabled"
          @click="submit"
        >
          发送
        </el-button>
      </div>

      <div class="composer-meta">
        <span>Enter 发送 · Shift + Enter 换行</span>
        <span class="doc-hint">知识库：{{ scope || '暂无文档' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  disabled: { type: Boolean, default: false },
  scope: { type: String, default: '' }
})

const emit = defineEmits(['send'])
const draft = ref('')

function submit() {
  const text = draft.value.trim()
  if (!text || props.disabled) return

  emit('send', text)
  draft.value = ''
}
</script>

<style scoped>
.composer {
  flex: none;
  padding: 12px 20px 14px;
  background: var(--surface);
  border-top: 1px solid var(--line);
}

.composer-inner {
  max-width: 820px;
  margin: 0 auto;
}

.input-shell {
  display: flex;
  align-items: flex-end;
  gap: 8px;
  padding: 5px 5px 5px 12px;
  background: var(--surface);
  border: 1px solid var(--line-strong);
  border-radius: 8px;
  transition: border-color 0.16s ease, box-shadow 0.16s ease;
}

.input-shell:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.input-shell.is-disabled {
  background: var(--surface-soft);
}

.input-shell :deep(.el-textarea__inner) {
  padding: 7px 0;
  color: var(--ink);
  font-size: 14px;
  line-height: 1.65;
  background: transparent;
  border: none;
  box-shadow: none;
  resize: none;
}

.input-shell :deep(.el-textarea__inner:focus) {
  box-shadow: none;
}

.input-shell :deep(.el-textarea__inner::placeholder) {
  color: var(--faint);
}

.send-btn {
  flex: none;
  height: 32px;
  padding: 0 14px;
  font-size: 12.5px;
  border-radius: 6px;
}

.composer-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 6px;
  padding: 0 2px;
  color: var(--faint);
  font-size: 11px;
}

.doc-hint {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 720px) {
  .composer {
    padding: 10px 14px 12px;
  }

  .composer-meta span:first-child {
    display: none;
  }

  .composer-meta {
    justify-content: flex-end;
  }
}
</style>
