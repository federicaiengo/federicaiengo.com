import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
export default defineConfig({ site: 'https://federicaiengo.com', integrations: [sitemap({ customPages: ['https://federicaiengo.com/tools/sql/'] })] });
