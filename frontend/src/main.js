import { createApp } from 'vue'
import App from './App.vue'

// 按需组件由 unplugin 自动引入，这里只补充 message 的样式
import 'element-plus/es/components/message/style/css'
import './styles/global.css'

createApp(App).mount('#app')
