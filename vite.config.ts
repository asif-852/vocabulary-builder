import { defineConfig, Plugin } from 'vite';
import react from '@vitejs/plugin-react';

/**
 * Inlines emitted stylesheet assets into dist/index.html to eliminate
 * render-blocking CSS requests on initial load.
 */
function inlineCssPlugin(): Plugin {
  return {
    name: 'inline-css',
    apply: 'build',
    enforce: 'post',
    generateBundle(_options, bundle) {
      const htmlAsset = bundle['index.html'];
      if (!htmlAsset || htmlAsset.type !== 'asset' || typeof htmlAsset.source !== 'string') {
        return;
      }

      let html = htmlAsset.source;
      for (const [fileName, chunk] of Object.entries(bundle)) {
        if (!fileName.endsWith('.css') || chunk.type !== 'asset' || typeof chunk.source !== 'string') {
          continue;
        }
        const linkRe = new RegExp(
          `<link\\b[^>]*href=["']/?${fileName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}["'][^>]*>`,
          'i'
        );
        if (linkRe.test(html)) {
          html = html.replace(linkRe, `<style>${chunk.source}</style>`);
          delete bundle[fileName];
        }
      }
      htmlAsset.source = html;
    }
  };
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), inlineCssPlugin()],
  build: {
    sourcemap: true,
    chunkSizeWarningLimit: 2000,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom']
        }
      }
    }
  }
});
