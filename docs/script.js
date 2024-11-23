async function searchLocation() {
    const city = document.getElementById('city').value;
    const country = document.getElementById('country').value;
    const resultsDiv = document.getElementById('results');
    
    if (!city || !country) {
        resultsDiv.innerHTML = '<p class="error">Please enter both city and country</p>';
        return;
    }

    resultsDiv.innerHTML = '<p class="loading">Searching for recycling businesses...</p>';

    try {
        const response = await fetch(
            `https://irecycle-digital-research.vercel.app/api/search?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`
        );
        const data = await response.json();

        if (data.status === 'error') {
            resultsDiv.innerHTML = `<p class="error">${data.message}</p>`;
            return;
        }

        displayResults(data.data);
    } catch (error) {
        resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
}

function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.innerHTML = '';

    data.forEach(business => {
        const card = document.createElement('div');
        card.className = 'business-card';
        card.innerHTML = `
            <div class="business-name">${business.name}</div>
            <div>${business.address}</div>
            ${business.phone ? `<div>📞 ${business.phone}</div>` : ''}
            ${business.website ? `<div>🌐 <a href="${business.website}" target="_blank">Website</a></div>` : ''}
            ${business.rating ? `<div>⭐ ${business.rating}</div>` : ''}
            ${business.materials.length ? `<div>♻️ Materials: ${business.materials.join(', ')}</div>` : ''}
        `;
        resultsDiv.appendChild(card);
    });
} 