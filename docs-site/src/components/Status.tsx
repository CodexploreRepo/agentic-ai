import React from 'react';

type Props = {
  /**
   * `complete` -- written, reviewed, code runs.
   * `draft` -- outline plus sources, safe to read but thin.
   * `planned` -- a stub so links resolve; nothing to read yet.
   */
  value: 'complete' | 'draft' | 'planned';
  /** Which module covers this, for reference pages. */
  module?: string;
};

const LABEL = {
  complete: 'Complete',
  draft: 'Draft',
  planned: 'Planned',
} as const;

/**
 * An honest status badge.
 *
 * This site publishes its outline before its prose, and a reader who lands on
 * a thin page deserves to know that it is thin rather than concluding the
 * subject is thin. Cheaper than hiding unfinished pages, and more useful.
 */
export default function Status({value, module}: Props): React.ReactElement {
  return (
    <p className="status-row">
      <span className={`status status-${value}`}>{LABEL[value]}</span>
      {module && <span className="status-module">Covered in {module}</span>}
    </p>
  );
}
