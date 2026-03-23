import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiBaseUrl = env.VITE_API_BASE_URL || 'http://localhost:5001'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    server: {
      port: 3100,
      host: '0.0.0.0',
      proxy: {
        '/api': {
          target: apiBaseUrl,
          changeOrigin: true
        },
        '/login': {
          target: apiBaseUrl,
          changeOrigin: true
        },
        '/register': {
          target: apiBaseUrl,
          changeOrigin: true
        },
        '/logout': {
          target: apiBaseUrl,
          changeOrigin: true
        },
        '/me': {
          target: apiBaseUrl,
          changeOrigin: true
        },
        '/static': {
          target: apiBaseUrl,
          changeOrigin: true
        }
      }
    }
  }
})
