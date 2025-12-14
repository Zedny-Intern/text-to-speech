import { useState } from 'react';

function TextInput({ value, onChange, maxLength = 10000 }) {
    const charCount = value.length;
    const isNearLimit = charCount > maxLength * 0.9;

    return (
        <div className="card">
            <div className="card-title">
                <span className="card-title-icon">✍️</span>
                Enter Your Text
            </div>
            <div className="text-input-wrapper">
                <textarea
                    className="text-input"
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    placeholder="Type or paste your text here... اكتب النص هنا...&#10;&#10;Supports Arabic, English, and mixed language text."
                    maxLength={maxLength}
                />
                <div
                    className="char-counter"
                    style={{ color: isNearLimit ? '#ef4444' : undefined }}
                >
                    {charCount.toLocaleString()} / {maxLength.toLocaleString()}
                </div>
            </div>
        </div>
    );
}

export default TextInput;
