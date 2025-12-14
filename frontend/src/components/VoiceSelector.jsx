function VoiceSelector({ language, onLanguageChange, gender, onGenderChange }) {
    const languages = [
        { id: 'auto', label: '🌐 Auto' },
        { id: 'ar', label: '🇪🇬 Arabic' },
        { id: 'en', label: '🇺🇸 English' },
    ];

    const genders = [
        { id: 'female', label: '👩 Female' },
        { id: 'male', label: '👨 Male' },
    ];

    return (
        <div className="card">
            <div className="card-title">
                <span className="card-title-icon">🎙️</span>
                Voice Settings
            </div>
            <div className="voice-selector">
                <div className="selector-group">
                    <label className="selector-label">Language</label>
                    <div className="selector-options">
                        {languages.map((lang) => (
                            <button
                                key={lang.id}
                                className={`option-btn ${language === lang.id ? 'active' : ''}`}
                                onClick={() => onLanguageChange(lang.id)}
                            >
                                {lang.label}
                            </button>
                        ))}
                    </div>
                </div>
                <div className="selector-group">
                    <label className="selector-label">Voice</label>
                    <div className="selector-options">
                        {genders.map((g) => (
                            <button
                                key={g.id}
                                className={`option-btn ${gender === g.id ? 'active' : ''}`}
                                onClick={() => onGenderChange(g.id)}
                            >
                                {g.label}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default VoiceSelector;
