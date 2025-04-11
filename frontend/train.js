const pretrainButton = document.getElementById('pretrain-button');
const dataType = document.getElementById('data-type');
const dataContent = document.getElementById('data-content');
const fileUpload = document.getElementById('file-upload');
const uploadButton = document.getElementById('upload-button');

// Show the file input for screenshot or text file
dataType.addEventListener('change', () => {
    if (dataType.value === 'screenshot' || dataType.value === 'text') {
        dataContent.style.display = 'none';
        fileUpload.style.display = 'block';
    } else if (dataType.value === 'video') {
        dataContent.style.display = 'block';
        fileUpload.style.display = 'none';
    }
});

// Pretrain the chatbot
pretrainButton.addEventListener('click', async () => {
    const response = await fetch('http://127.0.0.1:5000/pretrain-formal-chat', {
        method: 'POST',
    });
    const data = await response.json();
    alert(data.message);
});

// Upload data for training
uploadButton.addEventListener('click', async () => {
    const type = dataType.value;
    const formData = new FormData();
    formData.append('type', type);

    if (type === 'video') {
        const content = dataContent.value.trim();
        if (!content) {
            alert('Please provide a video URL.');
            return;
        }
        formData.append('content', content);
    } else {
        const file = fileUpload.files[0];
        if (!file) {
            alert('Please select a file.');
            return;
        }
        formData.append('file', file);
    }

    const response = await fetch('http://127.0.0.1:5000/upload-data', {
        method: 'POST',
        body: formData,
    });
    const data = await response.json();
    alert(data.message || data.error);
});