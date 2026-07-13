import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { BootstrapVueNextResolver } from 'bootstrap-vue-next'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    Components({
      dirs: ['src/components'],
      extensions: ['vue'],
      deep: true,
      resolvers: [
        BootstrapVueNextResolver(),
        IconsResolver({
          prefix: 'i', // all icons Components will start with <i-...>
          enabledCollections: ['bi'], // 'bi' stands for bootstrap-icons
        }),
      ],
    }),
    Icons({
      autoInstall: true,
    }),
  ],
})
