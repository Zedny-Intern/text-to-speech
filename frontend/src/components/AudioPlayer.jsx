import { useRef, useState } from 'react';
import { getAudioUrl } from '../api/api';

function AudioPlayer({ filename, duration, textLength, sentencesCount }) {
    const audioRef = useRef(null);
    const [playbackRate, setPlaybackRate] = useState(1);

    const handleSpeedChange = (speed) => {
        setPlaybackRate(speed);
        if (audioRef.current) {
            audioRef.current.playbackRate = speed;
        }
    };

    const speeds = [0.5, 0.75, 1, 1.25, 1.5, 2];

    return (
        <div className="audio-player-wrapper">
            <audio
                ref={audioRef}
                className="audio-player"
                controls
                src={getAudioUrl(filename)}
            />

            <div className="audio-info">
                <div className="audio-details">
                    <div className="audio-detail">
                        <span className="audio-detail-icon">⏱️</span>
                        <span>{duration}ms</span>
                    </div>
                    <div className="audio-detail">
                        <span className="audio-detail-icon">📝</span>
                        <span>{textLength} chars</span>
                    </div>
                    <div className="audio-detail">
                        <span className="audio-detail-icon">📄</span>
                        <span>{sentencesCount} sentences</span>
                    </div>
                </div>

                <div className="selector-options" style={{ gap: '4px' }}>
                    {speeds.map((speed) => (
                        <button
                            key={speed}
                            className={`option-btn ${playbackRate === speed ? 'active' : ''}`}
                            onClick={() => handleSpeedChange(speed)}
                            style={{ padding: '4px 8px', fontSize: '0.75rem' }}
                        >
                            {speed}x
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default AudioPlayer;
