// Toggle between PDF upload and text paste
document.addEventListener('DOMContentLoaded', function() {
    const uploadOption = document.getElementById('upload_option');
    const pasteOption = document.getElementById('paste_option');
    const uploadSection = document.getElementById('upload_section');
    const pasteSection = document.getElementById('paste_section');
    const form = document.getElementById('analysisForm');
    const submitBtn = document.getElementById('submitBtn');
    const loading = document.getElementById('loading');

    if (uploadOption && pasteOption) {
        uploadOption.addEventListener('change', function() {
            uploadSection.style.display = 'block';
            pasteSection.style.display = 'none';
        });

        pasteOption.addEventListener('change', function() {
            uploadSection.style.display = 'none';
            pasteSection.style.display = 'block';
        });
    }

    // Form submission handling
    if (form) {
        form.addEventListener('submit', function(e) {
            submitBtn.disabled = true;
            submitBtn.textContent = '⏳ Analyzing...';
            loading.style.display = 'block';
        });
    }
});
