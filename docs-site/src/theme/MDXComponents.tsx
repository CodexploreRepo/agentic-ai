import MDXComponents from '@docusaurus/theme-classic/lib/theme/MDXComponents';
import WatchReadCode from '@site/src/components/WatchReadCode';
import YouTube from '@site/src/components/YouTube';

/**
 * Components usable in any .mdx page without an import.
 *
 * Worth the indirection because both appear at the top of every module page,
 * and an import line in each one is noise a content author should not have to
 * remember.
 *
 * Note that only .mdx pages can use these. Reference pages are .md (parsed as
 * CommonMark) and use `:::note` admonitions instead -- see CLAUDE.md.
 */
export default {
  ...MDXComponents,
  YouTube,
  WatchReadCode,
};
