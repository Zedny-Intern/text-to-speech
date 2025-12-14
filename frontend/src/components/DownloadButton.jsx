import { getDownloadUrl } from '../api/api';

function DownloadButton({ filename }) {
    const handleDownload = () => {
        const link = document.createElement('a');
        link.href = getDownloadUrl(filename);
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <button className="download-btn" onClick={handleDownload}>
            <span>⬇️</span>
            Download Audio
        </button>
    );
}

export default DownloadButton;
