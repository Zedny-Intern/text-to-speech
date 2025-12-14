import { useState, useRef } from 'react';
import { uploadTextFile } from '../api/api';

function FileUpload({ language, gender, onResult, onError, setLoading }) {
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            await handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = async (e) => {
        if (e.target.files && e.target.files[0]) {
            await handleFile(e.target.files[0]);
        }
    };

    const handleFile = async (file) => {
        if (!file.name.endsWith('.txt')) {
            onError('Only .txt files are supported');
            return;
        }

        setLoading(true);
        try {
            const result = await uploadTextFile(file, language, gender);
            onResult(result);
        } catch (err) {
            onError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div
            className={`file-upload ${dragActive ? 'active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            style={dragActive ? { borderColor: 'var(--accent-primary)', background: 'rgba(99, 102, 241, 0.1)' } : {}}
        >
            <input
                ref={inputRef}
                type="file"
                accept=".txt"
                onChange={handleChange}
            />
            <div className="file-upload-icon">📁</div>
            <div className="file-upload-text">
                Drop a .txt file here or click to upload
            </div>
        </div>
    );
}

export default FileUpload;
