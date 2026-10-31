<template>
  <aside class="side-panel">
    <!-- 对话模块：会话历史 -->
    <template v-if="view === 'chat'">
      <div class="side-head">
        <h2 class="side-title">对话</h2>
        <button type="button" class="new-btn" title="新建对话" @click="$emit('new-chat')">
          <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
            <path d="M8 3v10M3 8h10" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </button>
      </div>

      <div class="side-body">
        <div class="side-guide">
          <span class="guide-ico" aria-hidden="true">
            <svg viewBox="0 0 16 16" width="18" height="18">
              <path
                d="M3 3.5h10v6H6.2L3 12.5v-9Z"
                fill="none"
                stroke="currentColor"
                stroke-width="1.2"
                stroke-linejoin="round"
              />
            </svg>
          </span>
          <p class="guide-title">开始新的对话</p>
          <span class="guide-desc">提问后会显示在这里</span>
        </div>

        <div v-if="documents.length" class="side-stat">
          <span class="stat-dot" aria-hidden="true"></span>
          已就绪 {{ documents.length }} 个文档
        </div>
      </div>
    </template>

    <!-- 知识库模块：文档列表 -->
    <template v-else>
      <div class="side-head">
        <h2 class="side-title">知识库</h2>
        <span class="side-count">{{ documents.length }}</span>
      </div>

      <div class="side-body">
        <div v-if="!documents.length" class="side-empty">
          还没有文档
        </div>

        <ul v-else class="doc-list">
          <li v-for="doc in documents" :key="doc.doc_id" class="doc-item">
            <span class="doc-ico" aria-hidden="true">
              <svg viewBox="0 0 16 16" width="14" height="14">
                <path
                  d="M4 2h5l3 3v9H4V2Zm5 0v3h3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.2"
                  stroke-linejoin="round"
                />
              </svg>
            </span>
            <div class="doc-meta">
              <span class="doc-name" :title="doc.filename">{{ doc.filename }}</span>
              <span class="doc-sub">{{ doc.chunk_count }} 片段 · {{ doc.pages }} 页</span>
            </div>
          </li>
        </ul>
      </div>
    </template>
  </aside>
</template>

<script setup>
defineProps({
  view: { type: String, default: 'chat' },
  documents: { type: Array, default: () => [] }
})

defineEmits(['navigate', 'new-chat'])
</script>

<style scoped>
.side-panel {
  display: flex;
  flex: none;
  flex-direction: column;
  width: 232px;
  min-height: 0;
  background: var(--surface-soft);
  border-right: 1px solid var(--line);
}

.side-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;
  padding: 0 14px 0 16px;
  border-bottom: 1px solid var(--line);
}

.side-title {
  margin: 0;
  color: var(--ink);
  font-size: 14px;
  font-weight: 600;
}

.side-count {
  color: var(--faint);
  font-size: 12px;
}

.new-btn {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  color: var(--muted);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 6px;
  cursor: pointer;
  transition: color 0.15s ease, border-color 0.15s ease, background 0.15s ease;
}

.new-btn:hover {
  color: var(--accent);
  background: var(--accent-soft);
  border-color: var(--accent-line);
}

.side-body {
  flex: 1;
  min-height: 0;
  padding: 12px 10px;
  overflow-y: auto;
}

.side-empty {
  padding: 24px 12px;
  color: var(--faint);
  font-size: 12.5px;
  text-align: center;
}

.side-guide {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 30px 12px 18px;
  text-align: center;
}

.guide-ico {
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
  color: var(--accent);
  background: var(--accent-soft);
  border: 1px solid var(--accent-line);
  border-radius: 10px;
}

.guide-title {
  margin: 0 0 3px;
  color: var(--text);
  font-size: 13px;
  font-weight: 600;
}

.guide-desc {
  color: var(--faint);
  font-size: 11.5px;
}

.side-stat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin: 4px 8px 0;
  padding: 8px 10px;
  color: var(--muted);
  font-size: 11.5px;
  background: var(--surface-muted);
  border-radius: 6px;
}

.stat-dot {
  width: 6px;
  height: 6px;
  background: #16a34a;
  border-radius: 50%;
}

.doc-list {
  display: flex;
  flex-direction: column;
  gap: 2px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 9px;
  border-radius: 6px;
  cursor: default;
  transition: background 0.14s ease;
}

.doc-item:hover {
  background: var(--surface-muted);
}

.doc-ico {
  display: grid;
  flex: none;
  place-items: center;
  width: 28px;
  height: 28px;
  color: #dc2626;
  background: #fef5f5;
  border: 1px solid #fde2e2;
  border-radius: 6px;
}

.doc-meta {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.doc-name {
  overflow: hidden;
  color: var(--text);
  font-size: 12.5px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.doc-sub {
  color: var(--faint);
  font-size: 11px;
}

@media (max-width: 960px) {
  .side-panel {
    width: 200px;
  }
}
</style>