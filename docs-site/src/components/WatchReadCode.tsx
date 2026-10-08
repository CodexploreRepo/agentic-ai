import Link from '@docusaurus/Link';
import React from 'react';

type Props = {
  /** YouTube video id, or omit until the episode is published. */
  video?: string | null;
  /** Where the written material starts. */
  read?: string;
  /** Path to the lab notebook on GitHub. */
  code?: string;
  /** Repo-relative path to the eval set, if the module has one. */
  evals?: string;
};

const REPO = 'https://github.com/CodexploreRepo/agentic-ai/blob/main';

/**
 * The three-button header at the top of every module page.
 *
 * Each module exists in three forms -- a video, a set of pages, and runnable
 * code -- and readers arrive wanting a different one. Making all three visible
 * at the top saves them guessing which navigation item means what.
 */
export default function WatchReadCode({video, read, code, evals}: Props): React.ReactElement {
  return (
    <div className="wrc">
      {video ? (
        <a className="wrc-item" href={`https://www.youtube.com/watch?v=${video}`}>
          <span className="wrc-icon">▶</span>
          <span>
            <strong>Watch</strong>
            <small>on YouTube</small>
          </span>
        </a>
      ) : (
        <span className="wrc-item wrc-disabled">
          <span className="wrc-icon">▶</span>
          <span>
            <strong>Watch</strong>
            <small>coming soon</small>
          </span>
        </span>
      )}

      {read && (
        <Link className="wrc-item" to={read}>
          <span className="wrc-icon">📖</span>
          <span>
            <strong>Read</strong>
            <small>start the theory</small>
          </span>
        </Link>
      )}

      {code && (
        <a className="wrc-item" href={`${REPO}/${code}`}>
          <span className="wrc-icon">💻</span>
          <span>
            <strong>Code</strong>
            <small>run the lab</small>
          </span>
        </a>
      )}

      {evals && (
        <a className="wrc-item" href={`${REPO}/${evals}`}>
          <span className="wrc-icon">📊</span>
          <span>
            <strong>Evals</strong>
            <small>the test cases</small>
          </span>
        </a>
      )}
    </div>
  );
}
