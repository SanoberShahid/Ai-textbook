import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
import { resolve } from 'path'; // Import resolve for path handling


// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'AI Textbook', // Updated title
  tagline: 'A Comprehensive Guide to Physical AI & Humanoid Robotics',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  customFields: {
    // Make the backend URL configurable
    backendUrl: process.env.BACKEND_URL || 'http://localhost:8000',
  },

  // Set the production url of your site here
url: 'https://SanoberShahid.github.io',
baseUrl: '/my-ai-textbook/',
  favicon: 'img/favicon.ico', // Set the favicon path



  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  // baseUrl: '/',

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ur'],
    localeConfigs: {
      ur: {
        htmlLang: 'ur-UR',
        direction: 'rtl',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'AI Textbook', // Updated title
      logo: {
        alt: 'Docusaurus Logo',
        src: 'img/favicon.ico',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Text Book', // Renamed from 'Book'
        },
        {
          to: '/blog', // Link to the blog page
          label: 'Blog',
          position: 'left'
        },
        {
          to: '/rag-chatbot',
          label: 'RAG Chatbot',
          position: 'left'
        },

        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/SanoberShahid/my-ai-textbook', // User needs to update this to their actual repo
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Docusaurus Logo',
        src: 'img/favicon.ico',
        href: 'https://github.com/SanoberShahid/my-ai-textbook', // User needs to update this
        width: 50,
        height: 50,
      },
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Text Book',
              to: '/docs/intro', // Link to the intro page
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Stack Overflow',
              href: 'https://stackoverflow.com/questions/tagged/docusaurus', // Placeholder
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com/invite/docusaurus', // Placeholder
            },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Blog',
              to: '/blog',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/SanoberShahid/my-ai-textbook', // Placeholder, user needs to update
            },
          ],
        },
      ],
      copyright: `Copyright © 2025 Sanober-Site. Built with Docusaurus.`, // Updated copyright
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
