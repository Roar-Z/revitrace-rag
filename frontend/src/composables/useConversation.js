import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  askQuestion,
  compareConcepts,
  generateAnalogy,
  generateExercise,
  getSummary
} from '../api'

// 类比风格循环顺序：生活 -> 故事 -> 游戏
const STYLE_LABELS = {
  life: '生活类比',
  story: '故事类比',
  game: '游戏类比'
}
const STYLE_ORDER = ['life', 'story', 'game']

/**
 * 对话状态与业务动作。
 * 问答统一作用于整个知识库（doc_id 传 null），不再按单篇文档切换。
 */
export function useConversation(hasDocuments) {
  const messages = ref([])
  const sending = ref(false)
  const toolLoading = ref('')

  let seed = 0
  const nextId = () => `${Date.now()}-${seed++}`

  // 新建对话：清空当前会话消息
  function newChat() {
    messages.value = []
  }

  // 发送问题，追加用户消息与助手回答
  async function sendQuestion(question) {
    const text = String(question || '').trim()
    if (!text || sending.value) return

    messages.value.push({ id: nextId(), role: 'user', content: text })
    sending.value = true

    try {
      const data = await askQuestion(text, null)
      messages.value.push({
        id: nextId(),
        role: 'assistant',
        kind: 'chat',
        content: data.answer || '暂无回答',
        citations: data.citations || [],
        analogy: null
      })
    } catch (error) {
      // 错误提示已由 axios 拦截器统一处理，这里只结束 loading 状态
    } finally {
      sending.value = false
    }
  }

  /**
   * 辅助理解：
   * initial 首次生成生活类比；simpler 基于当前通俗版继续简化；switch 换一种类比风格。
   */
  async function assist(message, mode) {
    if (message.analogy?.loading) return

    let baseAnswer = message.content
    let style = 'life'

    if (mode === 'simpler') {
      if (!message.analogy?.text) return
      baseAnswer = message.analogy.text
      style = message.analogy.style || 'life'
    } else if (mode === 'switch') {
      const currentIndex = STYLE_ORDER.indexOf(message.analogy?.style || 'life')
      style = STYLE_ORDER[(currentIndex + 1) % STYLE_ORDER.length]
    }

    // depth 用于区分层级：assist 只做进一步解释，simple 才进入通俗类比
    const depth = mode === 'simpler' || mode === 'switch' ? 'simple' : 'assist'

    // 记录旧内容，请求失败时可以回滚
    const previous = message.analogy?.text ? { ...message.analogy } : null
    message.analogy = {
      text: previous?.text || '',
      style,
      styleLabel: STYLE_LABELS[style],
      depth,
      loading: true
    }

    try {
      const data = await generateAnalogy(baseAnswer, style, null)
      message.analogy = {
        text: data.analogy || '',
        style: data.style || style,
        styleLabel: STYLE_LABELS[data.style || style] || STYLE_LABELS[style],
        depth,
        loading: false
      }
    } catch (error) {
      message.analogy = previous ? { ...previous, loading: false } : null
    }
  }

  // 学习工具的统一执行入口，避免三个接口各写一套 loading 逻辑
  async function runTool(kind, request) {
    if (toolLoading.value) return

    toolLoading.value = kind
    try {
      const data = await request()
      messages.value.push({ id: nextId(), role: 'tool', kind, data })
    } catch (error) {
      // 错误提示由拦截器处理
    } finally {
      toolLoading.value = ''
    }
  }

  async function runSummary() {
    if (!hasDocuments.value) {
      ElMessage.warning('请先在知识库上传文档')
      return
    }
    await runTool('summary', () => getSummary(null))
  }

  async function runCompare(conceptA, conceptB) {
    if (!conceptA || !conceptB) return
    await runTool('compare', () => compareConcepts(conceptA, conceptB, null))
  }

  async function runExercise() {
    if (!hasDocuments.value) {
      ElMessage.warning('请先在知识库上传文档')
      return
    }
    await runTool('exercise', () => generateExercise(null))
  }

  return {
    messages,
    sending,
    toolLoading,
    sendQuestion,
    assist,
    runSummary,
    runCompare,
    runExercise,
    newChat
  }
}
