import MDXComponents from '@docusaurus/theme-classic/lib/theme/MDXComponents';
import Status from '@site/src/components/Status';
import WatchReadCode from '@site/src/components/WatchReadCode';
import YouTube from '@site/src/components/YouTube';

/**
 * Components usable in any .mdx page without an import.
 *
 * Worth the indirection because these three appear at the top of nearly every
 * module page, and an import line in each one is noise a content author should
 * not have to remember.
 */
export default {
  ...MDXComponents,
  YouTube,
  WatchReadCode,
  Status,
};
