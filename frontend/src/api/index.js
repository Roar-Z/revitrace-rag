import http from './request'

/**
 * 六个后端接口的请求函数。
 * 大模型相关逻辑全部在后端完成，前端只负责传参和展示。
 */

// 1. 上传 PDF，完成解析、分块与向量入库
export function uploadPdf(file, onProgress) {
  const formData = new FormData()
  formData.append('file', file)

  return http.post('/api/upload', formData, {
    timeout: 120000,
    onUploadProgress: (event) => {
      if (onProgress && event.total) {
        onProgress(Math.round((event.loaded / event.total) * 100))
      }
    }
  })
}

// 2. 文档问答，返回标准答案与溯源片段
export function askQuestion(question, docId, topK = 4) {
  return http.post('/api/chat', {
    question,
    doc_id: docId || null,
    top_k: topK
  })
}

// 3. 通俗解读，style 支持 life / story / game
export function generateAnalogy(answer, style, docId) {
  return http.post('/api/assist-analogy', {
    answer,
    style,
    doc_id: docId || null
  })
}

// 4. 考点总结
export function getSummary(docId, topic = null) {
  return http.post('/api/summary', {
    doc_id: docId,
    topic
  })
}

// 5. 两个知识点对比，返回 Markdown 表格
export function compareConcepts(conceptA, conceptB, docId) {
  return http.post('/api/compare', {
    concept_a: conceptA,
    concept_b: conceptB,
    doc_id: docId || null
  })
}

// 6. 随堂习题
export function generateExercise(docId, topic = null, choiceCount = 3, includeShortAnswer = true) {
  return http.post('/api/generate-exercise', {
    doc_id: docId,
    topic,
    choice_count: choiceCount,
    include_short_answer: includeShortAnswer
  })
}
