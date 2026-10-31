import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

export default defineConfig({
  plugins: [
    vue(),
    // ElMessage 等 API 自动按需引入
    AutoImport({
      resolvers: [ElementPlusResolver()],
      dts: false
    }),
    // 模板中的 Element Plus 组件按需引入，样式同步按需加载
    Components({
      resolvers: [ElementPlusResolver({ importStyle: 'css' })],
      dts: false
    })
  ],
  server: {
    host: '127.0.0.1',
    port: 5173
  }
})
