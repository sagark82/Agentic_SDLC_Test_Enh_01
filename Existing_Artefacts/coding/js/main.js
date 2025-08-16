/* js/main.js */
document.getElementById('contact-form')?.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    const statusEl = document.getElementById('form-status');

    try {
        const response = await fetch('http://localhost:5000/api/contact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();
        statusEl.textContent = result.message;
        form.reset();
    } catch (error) {
        statusEl.textContent = 'An error occurred. Please try again.';
    }
});
