import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'lucide-react'],
          gre333: ['./src/data/gre333.json'],
          wordsmart1: ['./src/data/wordsmart1.json'],
          wordsmart2: ['./src/data/wordsmart2.json']
        }
      }
    }
  }
});
