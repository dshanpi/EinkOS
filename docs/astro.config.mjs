import { defineConfig } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import starlight from '@astrojs/starlight';
import { remarkDocs } from './src/plugins/remark-docs.mjs';
import { syncContent, sourcePaths } from './scripts/prepare-docs.mjs';
import { site, base, repository, sidebar } from './routes.mjs';

export default defineConfig({
  site, base, trailingSlash: 'always',
  markdown: { processor: unified({ remarkPlugins: [remarkDocs] }) },
  integrations: [
    {
      name: 'einkos-canonical-docs',
      hooks: {
        'astro:server:setup': ({ server }) => {
          server.watcher.add(sourcePaths);
          const update = (file) => {
            if (sourcePaths.includes(file)) syncContent();
          };
          server.watcher.on('change', update);
          server.watcher.on('add', update);
        },
      },
    },
    starlight({
      title: 'EinkOS',
      description: '面向墨水屏设备的 Linux 桌面：安装、操作、系统架构与开发文档。',
      locales: { root: { label: '简体中文', lang: 'zh-CN' } },
      social: [{ icon: 'github', label: 'GitHub', href: repository }],
      sidebar,
      customCss: ['./src/styles/custom.css'],
      head: [{ tag: 'script', attrs: { type: 'module', src: base + '/enhance.js' } }],
    }),
  ],
});
