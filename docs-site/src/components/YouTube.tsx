import React, {useState} from 'react';

type Props = {
  /** The YouTube video id. Pass nothing (or null) before the episode exists. */
  id?: string | null;
  title?: string;
};

/**
 * A lazy YouTube embed.
 *
 * It renders a thumbnail first and only loads the iframe on click. That keeps
 * a page with an embed from pulling in several hundred kilobytes of player on
 * every visit, which matters because most readers arriving from search never
 * press play.
 *
 * With no `id`, it renders a quiet placeholder instead of an empty box, so a
 * module page can be published before its video is recorded.
 */
export default function YouTube({id, title = 'Watch on YouTube'}: Props): React.ReactElement {
  const [playing, setPlaying] = useState(false);

  if (!id) {
    return (
      <div className="video-placeholder">
        <strong>Video coming soon.</strong> The written material below is complete and
        stands on its own.
      </div>
    );
  }

  return (
    <div className="video-frame">
      {playing ? (
        <iframe
          src={`https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`}
          title={title}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; picture-in-picture"
          allowFullScreen
        />
      ) : (
        <button
          type="button"
          className="video-poster"
          onClick={() => setPlaying(true)}
          aria-label={`Play video: ${title}`}
        >
          <img src={`https://i.ytimg.com/vi/${id}/hqdefault.jpg`} alt="" loading="lazy" />
          <span className="video-play" aria-hidden="true" />
        </button>
      )}
    </div>
  );
}
