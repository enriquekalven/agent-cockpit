import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 8888,
  },
  build: {
    outDir: "dist-web",
    emptyOutDir: true,
  },
  optimizeDeps: {
    entries: ['index.html'],
  }
})
