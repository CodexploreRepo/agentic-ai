import type * as Preset from '@docusaurus/preset-classic';
import type {Config} from '@docusaurus/types';
import {themes as prismThemes} from 'prism-react-renderer';

// The knowledge base lives in /docs at the repo root, not inside this app, so
// that every page stays readable on GitHub as plain Markdown. Docusaurus reads
// it from there via the `path` option below.
const config: Config = {
  title: 'Agentic AI',
  tagline: 'Build agents that survive production',
  favicon: 'img/favicon.ico',

  url: 'https://codexplorerepo.github.io',
  baseUrl: '/agentic-ai/',
  organizationName: 'CodexploreRepo',
  projectName: 'agentic-ai',
  trailingSlash: false,

  // A broken internal link is a broken promise to a reader who arrived from a
  // video description. Fail the build instead of shipping one.
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'warn',

  future: {
    v4: true,
    faster: true,
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  markdown: {
    // .md is parsed as CommonMark, .mdx as MDX. This is what lets generated
    // notebook pages (full of braces and angle brackets in code output) render
    // without escaping every one of them.
    format: 'detect',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          path: '../docs',
          routeBasePath: '/',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/CodexploreRepo/agentic-ai/tree/main/docs/',
          showLastUpdateTime: true,
          breadcrumbs: true,
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Agentic AI',
      logo: {alt: 'Agentic AI', src: 'img/logo.svg'},
      items: [
        {type: 'docSidebar', sidebarId: 'course', position: 'left', label: 'Curriculum'},
        {type: 'docSidebar', sidebarId: 'reference', position: 'left', label: 'Reference'},
        {
          href: 'https://www.youtube.com/@CodeXplore',
          label: 'YouTube',
          position: 'right',
        },
        {
          href: 'https://github.com/CodexploreRepo/agentic-ai',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Learn',
          items: [
            {label: 'Start here', to: '/start-here/how-to-use-this-repo'},
            {label: 'Module 01', to: '/modules/01-foundations/'},
            {label: 'Pattern catalogue', to: '/patterns/'},
          ],
        },
        {
          title: 'Reference',
          items: [
            {label: 'Evaluation', to: '/evaluation/eval-driven-development'},
            {label: 'Glossary', to: '/foundations/glossary'},
            {label: 'Reading list', to: '/references/reading-list'},
          ],
        },
        {
          title: 'More',
          items: [
            {label: 'CodeXplore on YouTube', href: 'https://www.youtube.com/@CodeXplore'},
            {label: 'GitHub', href: 'https://github.com/CodexploreRepo/agentic-ai'},
            {label: 'Attribution', to: '/references/attribution'},
          ],
        },
      ],
      copyright: `Code MIT, prose CC BY 4.0 · CodeXplore ${new Date().getFullYear()}`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['bash', 'json', 'yaml', 'python', 'diff'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
