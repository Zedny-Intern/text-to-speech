import { useState, useEffect } from 'react';
import TextInput from '../components/TextInput';
import VoiceSelector from '../components/VoiceSelector';
import AudioPlayer from '../components/AudioPlayer';
import DownloadButton from '../components/DownloadButton';
import FileUpload from '../components/FileUpload';
import { synthesizeSpeech, getStatus } from '../api/api';

function Home() {
    const [text, setText] = useState('');
    const [language, setLanguage] = useState('auto');
    const [gender, setGender] = useState('female');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [result, setResult] = useState(null);
    const [backendStatus, setBackendStatus] = useState(null);

    // Check backend status on mount
    useEffect(() => {
        checkBackendStatus();
    }, []);

    const checkBackendStatus = async () => {
        try {
            const status = await getStatus();
            setBackendStatus(status);
        } catch (err) {
            setBackendStatus({ status: 'offline' });
        }
    };

    const handleGenerate = async () => {
        if (!text.trim()) {
            setError('Please enter some text');
            return;
        }

        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await synthesizeSpeech(text, language, gender);
            setResult(response);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleResult = (response) => {
        setResult(response);
        setError('');
    };

    const handleError = (message) => {
        setError(message);
        setResult(null);
    };

    return (
        <div className="app-container">
            {/* Header */}
            <header className="header">
                <div className="header-icon">🔊</div>
                <h1>Multilingual TTS</h1>
                <p>Arabic & English Text-to-Speech with Neural Voices</p>
                {backendStatus && (
                    <div className="status-badge" style={{
                        marginTop: '12px',
                        background: backendStatus.status === 'healthy' ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                        borderColor: backendStatus.status === 'healthy' ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)',
                        color: backendStatus.status === 'healthy' ? '#22c55e' : '#ef4444'
                    }}>
                        <div className="status-dot" style={{
                            background: backendStatus.status === 'healthy' ? '#22c55e' : '#ef4444'
                        }}></div>
                        {backendStatus.status === 'healthy' ? 'Backend Connected' : 'Backend Offline'}
                    </div>
                )}
            </header>

            {/* Text Input */}
            <TextInput value={text} onChange={setText} />

            {/* File Upload */}
            <div className="card">
                <div className="card-title">
                    <span className="card-title-icon">📁</span>
                    Or Upload Text File
                </div>
                <FileUpload
                    language={language}
                    gender={gender}
                    onResult={handleResult}
                    onError={handleError}
                    setLoading={setLoading}
                />
            </div>

            {/* Voice Settings */}
            <VoiceSelector
                language={language}
                onLanguageChange={setLanguage}
                gender={gender}
                onGenderChange={setGender}
            />

            {/* Generate Button */}
            <button
                className={`generate-btn ${loading ? 'loading' : ''}`}
                onClick={handleGenerate}
                disabled={loading || !text.trim()}
            >
                {loading ? (
                    <>
                        <div className="spinner"></div>
                        Generating...
                    </>
                ) : (
                    <>
                        <span>🎵</span>
                        Generate Speech
                    </>
                )}
            </button>

            {/* Error Message */}
            {error && (
                <div className="error-message" style={{ marginTop: '16px' }}>
                    ⚠️ {error}
                </div>
            )}

            {/* Audio Result */}
            {result && (
                <div className="card" style={{ marginTop: '24px' }}>
                    <div className="card-title">
                        <span className="card-title-icon">🎧</span>
                        Generated Audio
                    </div>
                    <AudioPlayer
                        filename={result.filename}
                        duration={result.duration_ms}
                        textLength={result.text_length}
                        sentencesCount={result.sentences_count}
                    />
                    <div style={{ marginTop: '16px', display: 'flex', justifyContent: 'flex-end' }}>
                        <DownloadButton filename={result.filename} />
                    </div>
                </div>
            )}

            {/* Language Support Info */}
            <div className="card" style={{ marginTop: '24px' }}>
                <div className="card-title">
                    <span className="card-title-icon">ℹ️</span>
                    Supported Languages
                </div>
                <div className="language-tags">
                    <span className="lang-tag">🇪🇬 Egyptian Arabic</span>
                    <span className="lang-tag">🇺🇸 American English</span>
                    <span className="lang-tag">🔀 Code-Switching</span>
                    <span className="lang-tag">🎙️ Neural Voices</span>
                </div>
            </div>

            {/* Footer */}
            <footer className="footer">
                <p>Powered by Edge-TTS Neural Voices</p>
            </footer>
        </div>
    );
}

export default Home;
