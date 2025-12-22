import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'My-Site', // Updated title
  tagline: 'A Comprehensive Guide to Physical AI & Humanoid Robotics',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
url: 'https://my-ai-textbook-xasc.vercel.app',
baseUrl: '/',




  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  // baseUrl: '/',

  onBrokenLinks: 'throw',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
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
      title: 'My-Site', // Updated title
      logo: {
        alt: 'Docusaurus Logo',
        src: 'img/logo.svg', // Assuming a logo.svg exists in static/img
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
          to: '/ask-the-book', // Assuming a page or external link for 'Ask the Book'
          label: 'Ask the Book',
          position: 'left'
        },
        {
          href: 'https://github.com/user/repo', // User needs to update this to their actual repo
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      logo: {
        alt: 'Docusaurus Logo',
        src: '/img/logo.svg',
        href: 'https://github.com/user/repo', // User needs to update this
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
              href: 'https://github.com/user/repo', // Placeholder, user needs to update
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
