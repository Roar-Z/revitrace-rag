/**
 * 把后端返回的 Markdown 表格转换成前端可直接渲染的行列数据。
 * 只处理标准 `| a | b |` 表格，解析失败时返回 null，由调用方降级展示原文。
 */
export function parseMarkdownTable(markdown) {
  if (typeof markdown !== 'string') return null

  const lines = markdown
    .trim()
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith('|'))

  if (lines.length < 3) return null

  const readCells = (line) =>
    line
      .replace(/^\|/, '')
      .replace(/\|$/, '')
      .split('|')
      .map((cell) => cell.trim())

  const headers = readCells(lines[0])
  const separator = readCells(lines[1])

  // 第二行必须是 | --- | 形式的分隔行
  const isSeparator = separator.every((cell) => /^:?-{3,}:?$/.test(cell))
  if (!headers.length || !isSeparator) return null

  const rows = lines
    .slice(2)
    .map(readCells)
    .filter((row) => row.length === headers.length)

  if (!rows.length) return null

  return { headers, rows }
}
