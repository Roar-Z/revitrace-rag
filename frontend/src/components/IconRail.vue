<template>
  <aside class="icon-rail">
    <div class="rail-brand" title="ReviTrace">R</div>

    <nav class="rail-nav">
      <button
        type="button"
        class="rail-item"
        :class="{ active: view === 'chat' }"
        title="对话"
        @click="$emit('navigate', 'chat')"
      >
        <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">
          <path
            d="M3.5 4.5h13v8.5H9l-3.2 3v-3H3.5v-8.5Z"
            fill="none"
            stroke="currentColor"
            stroke-width="1.4"
            stroke-linejoin="round"
          />
        </svg>
        <span>对话</span>
      </button>

      <button
        type="button"
        class="rail-item"
        :class="{ active: view === 'kb' }"
        title="知识库"
        @click="$emit('navigate', 'kb')"
      >
        <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">
          <path
            d="M3 5.5C3 4.6 6.1 4 10 4s7 .6 7 1.5v9c0 .9-3.1 1.5-7 1.5s-7-.6-7-1.5v-9Z"
            fill="none"
            stroke="currentColor"
            stroke-width="1.4"
          />
          <path d="M3 10c0 .9 3.1 1.5 7 1.5s7-.6 7-1.5" fill="none" stroke="currentColor" stroke-width="1.4" />
        </svg>
        <span>知识库</span>
        <span v-if="docCount" class="rail-badge">{{ docCount }}</span>
      </button>
    </nav>

    <div class="rail-foot">
      <a
        class="rail-item"
        :href="docsUrl"
        target="_blank"
        rel="noopener noreferrer"
        title="API 文档"
      >
        <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true">
          <path
            d="M6 4.5 3.5 7 6 9.5M12 4.5l2.5 2.5-2.5 2.5M9.5 3.5l-2 9"
            fill="none"
            stroke="currentColor"
            stroke-width="1.4"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
        <span>文档</span>
      </a>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  view: { type: String, default: 'chat' },
  docCount: { type: Number, default: 0 },
  docsUrl: { type: String, default: '#' }
})

defineEmits(['navigate'])
</script>

<style scoped>
.icon-rail {
  display: flex;
  flex: none;
  flex-direction: column;
  align-items: center;
  width: 64px;
  min-height: 0;
  padding: 12px 0;
  background: #17191f;
}

.rail-brand {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  margin-bottom: 18px;
  color: #ffffff;
  font-size: 16px;
  font-weight: 700;
  background: var(--accent);
  border-radius: 8px;
}

.rail-nav {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  width: 100%;
}

.rail-foot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  width: 100%;
}

.rail-item {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  width: 46px;
  height: 48px;
  color: #8f95a3;
  font-size: 10px;
  line-height: 1;
  background: transparent;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  text-decoration: none;
  transition: color 0.15s ease, background 0.15s ease;
}

.rail-item:hover {
  color: #e4e6eb;
  background: rgba(255, 255, 255, 0.07);
}

.rail-item.active {
  color: #ffffff;
  background: var(--accent);
}

.rail-item.active:hover {
  background: var(--accent-hover);
}

.rail-badge {
  position: absolute;
  top: 6px;
  right: 5px;
  min-width: 14px;
  height: 14px;
  padding: 0 3px;
  color: #ffffff;
  font-size: 9px;
  line-height: 14px;
  text-align: center;
  background: #ef4444;
  border-radius: 7px;
}
</style>