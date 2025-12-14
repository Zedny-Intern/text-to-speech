const API_BASE = 'http://localhost:8000';

export async function synthesizeSpeech(text, language = 'auto', gender = 'female') {
    const response = await fetch(`${API_BASE}/synthesize`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text, language, gender }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Synthesis failed');
    }

    return response.json();
}

export async function uploadTextFile(file, language = 'auto', gender = 'female') {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(
        `${API_BASE}/upload-text?language=${language}&gender=${gender}`,
        {
            method: 'POST',
            body: formData,
        }
    );

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Upload failed');
    }

    return response.json();
}

export async function getVoices() {
    const response = await fetch(`${API_BASE}/voices`);
    if (!response.ok) {
        throw new Error('Failed to fetch voices');
    }
    return response.json();
}

export async function getStatus() {
    const response = await fetch(`${API_BASE}/status`);
    if (!response.ok) {
        throw new Error('Backend not available');
    }
    return response.json();
}

export function getDownloadUrl(filename) {
    return `${API_BASE}/download/${filename}`;
}

export function getAudioUrl(filename) {
    return `${API_BASE}/download/${filename}`;
}
