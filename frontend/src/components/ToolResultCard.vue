<template>
  <article class="tool-card">
    <header class="tool-head">
      <div class="tool-title">
        <h3>{{ title }}</h3>
      </div>
      <span v-if="countLabel" class="tool-count">{{ countLabel }}</span>
    </header>

    <!-- 考点总结 -->
    <div v-if="kind === 'summary'">
      <p class="summary-text">{{ data.summary }}</p>

      <div v-if="points.length" class="point-list">
        <div v-for="(point, index) in points" :key="index" class="point">
          <span class="point-index">{{ String(index + 1).padStart(2, '0') }}</span>
          <div class="point-main">
            <h4>{{ point.title }}</h4>
            <p>{{ point.detail }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 知识点对比：把 Markdown 表格转成原生表格 -->
    <div v-else-if="kind === 'compare'">
      <table v-if="table" class="compare-table">
        <thead>
          <tr>
            <th v-for="(header, index) in table.headers" :key="index">{{ header }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, rowIndex) in table.rows" :key="rowIndex">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
          </tr>
        </tbody>
      </table>
      <pre v-else class="raw-markdown">{{ data.table_markdown }}</pre>
    </div>

    <!-- 随堂习题 -->
    <div v-else class="exercise">
      <div v-if="choiceQuestions.length" class="exercise-group">
        <span class="group-label">选择题</span>

        <div
          v-for="(question, index) in choiceQuestions"
          :key="index"
          class="question"
        >
          <p class="question-stem">
            <span class="question-index">{{ index + 1 }}.</span>
            {{ question.question }}
          </p>

          <div class="option-list">
            <span v-for="(option, optionIndex) in question.options" :key="optionIndex" class="option">
              {{ option }}
            </span>
          </div>

          <div class="answer-block">
            <span class="answer-tag">答案 {{ question.answer }}</span>
            <p class="answer-text">{{ question.explanation }}</p>
          </div>
        </div>
      </div>

      <div v-if="shortQuestions.length" class="exercise-group short-group">
        <span class="group-label">简答题</span>

        <div
          v-for="(question, index) in shortQuestions"
          :key="index"
          class="question"
        >
          <p class="question-stem">
            <span class="question-index">{{ index + 1 }}.</span>
            {{ question.question }}
          </p>
          <div class="answer-block">
            <span class="answer-tag is-plain">参考答案</span>
            <p class="answer-text">{{ question.reference_answer }}</p>
          </div>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { parseMarkdownTable } from '../utils/markdownTable'

const props = defineProps({
  message: { type: Object, required: true }
})

const TITLES = {
  summary: '考点总结',
  compare: '知识点对比',
  exercise: '随堂习题'
}

const kind = computed(() => props.message.kind)
const data = computed(() => props.message.data || {})
const title = computed(() => TITLES[kind.value] || '学习结果')

const points = computed(() => data.value.points || [])
const table = computed(() =>
  kind.value === 'compare' ? parseMarkdownTable(data.value.table_markdown) : null
)
const choiceQuestions = computed(() => data.value.choice_questions || [])
const shortQuestions = computed(() => data.value.short_answer_questions || [])

const countLabel = computed(() => {
  if (kind.value === 'summary') return points.value.length ? `${points.value.length} 个考点` : ''
  if (kind.value === 'compare') return table.value ? `${table.value.rows.length} 组对比` : ''
  if (kind.value === 'exercise') {
    const parts = []
    if (choiceQuestions.value.length) parts.push(`${choiceQuestions.value.length} 道选择`)
    if (shortQuestions.value.length) parts.push(`${shortQuestions.value.length} 道简答`)
    return parts.join(' · ')
  }
  return ''
})
</script>

<style scoped>
.tool-card {
  max-width: 780px;
  margin-left: 36px;
  padding: 16px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(17, 24, 39, 0.03);
}

.tool-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}

.tool-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tool-title h3 {
  margin: 0;
  color: var(--ink);
  font-size: 14px;
  font-weight: 600;
}

.tool-count {
  color: var(--muted);
  font-size: 11px;
}

/* ---------- 考点总结 ---------- */
.summary-text {
  margin: 0;
  color: var(--text);
  font-size: 13px;
  line-height: 1.8;
  white-space: pre-wrap;
}

.point-list {
  margin-top: 14px;
}

.point {
  display: flex;
  gap: 10px;
  padding: 10px 0;
}

.point + .point {
  border-top: 1px solid #f1f3f6;
}

.point-index {
  flex: none;
  padding-top: 1px;
  color: var(--faint);
  font-size: 11px;
  font-variant-numeric: tabular-nums;
}

.point-main h4 {
  margin: 0 0 3px;
  color: var(--ink);
  font-size: 13px;
  font-weight: 600;
}

.point-main p {
  margin: 0;
  color: var(--muted);
  font-size: 12.5px;
  line-height: 1.7;
}

/* ---------- 知识点对比 ---------- */
.compare-table {
  width: 100%;
  border-spacing: 0;
  border-collapse: separate;
  overflow: hidden;
  font-size: 12.5px;
  border: 1px solid var(--line);
  border-radius: 6px;
}

.compare-table th {
  padding: 9px 12px;
  color: var(--ink);
  font-weight: 600;
  text-align: left;
  background: var(--surface-soft);
  border-bottom: 1px solid var(--line);
}

.compare-table td {
  padding: 9px 12px;
  color: var(--text);
  line-height: 1.65;
  vertical-align: top;
  border-bottom: 1px solid #f1f3f6;
}

.compare-table tr:last-child td {
  border-bottom: none;
}

.compare-table th + th,
.compare-table td + td {
  border-left: 1px solid #f1f3f6;
}

.raw-markdown {
  margin: 0;
  padding: 12px;
  overflow-x: auto;
  color: var(--text);
  font-size: 12px;
  line-height: 1.7;
  background: var(--surface-soft);
  border: 1px solid var(--line);
  border-radius: 8px;
}

/* ---------- 随堂习题 ---------- */
.exercise-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.short-group {
  margin-top: 20px;
  padding-top: 18px;
  border-top: 1px solid var(--line);
}

.group-label {
  color: var(--muted);
  font-size: 11px;
}

.question-stem {
  margin: 0 0 9px;
  color: var(--ink);
  font-size: 13px;
  line-height: 1.7;
}

.question-index {
  margin-right: 4px;
  color: var(--muted);
}

.option-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 6px;
}

.option {
  padding: 6px 9px;
  color: var(--text);
  font-size: 12px;
  line-height: 1.55;
  background: var(--surface-soft);
  border: 1px solid #f1f3f6;
  border-radius: 4px;
}

.answer-block {
  display: flex;
  gap: 9px;
  align-items: flex-start;
  margin-top: 8px;
  padding: 8px 10px;
  background: var(--surface-soft);
  border-radius: 4px;
}

.answer-tag {
  flex: none;
  padding-top: 1px;
  color: var(--accent);
  font-size: 10.5px;
  font-weight: 600;
}

.answer-tag.is-plain {
  color: var(--muted);
  font-weight: 500;
}

.answer-text {
  margin: 0;
  color: #4b5563;
  font-size: 12px;
  line-height: 1.65;
}

@media (max-width: 780px) {
  .tool-card {
    margin-left: 0;
  }

  .option-list {
    grid-template-columns: 1fr;
  }
}
</style>
