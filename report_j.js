document.getElementById('uploadForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent the default form submission

    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please choose a file!');
        return;
    }

    // Check if the file is a valid type (image or pdf)
    const validTypes = ['image/jpeg', 'image/png', 'application/pdf'];
    if (!validTypes.includes(file.type)) {
        alert('Unsupported file type. Please upload a JPEG, PNG, or PDF.');
        return;
    }

    // Convert image to JPEG if it's not already in JPEG format
    let convertedFile = file;
    if (file.type === 'image/png') {
        const image = await loadImage(file);
        convertedFile = await convertToJpeg(image);
    }

    const formData = new FormData();
    formData.append('file', convertedFile, convertedFile.name);

    try {
        const response = await fetch('https://hreport.openai.azure.com/openai/deployments/gpt-4/chat/completions?api-version=2024-08-01-preview', {
            method: 'POST',
            headers: {
                'api-key': '7eff5afad45744488b4c01d1c0291ae5'
            },
            body: formData
        });

        if (response.ok) {
            const result = await response.json();
            document.getElementById('uploadStatus').textContent = 'File uploaded successfully!';
            console.log(result);
        } else {
            document.getElementById('uploadStatus').textContent = `Upload failed: ${response.statusText}`;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('uploadStatus').textContent = 'An error occurred while uploading the file.';
    }
});

function loadImage(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = event.target.result;
        };
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

function convertToJpeg(image) {
    return new Promise((resolve) => {
        const canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(image, 0, 0);
        canvas.toBlob((blob) => {
            resolve(new File([blob], 'converted.jpg', { type: 'image/jpeg' }));
        }, 'image/jpeg');
    });
}
