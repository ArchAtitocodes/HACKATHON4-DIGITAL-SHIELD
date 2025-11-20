// static/js/literacy_js.js

document.addEventListener('DOMContentLoaded', function() {
    const platformsList = document.getElementById('platforms-list');
    const guideContent = document.getElementById('guide-content');
    let literacyData = {}; // To store the loaded literacy data

    // Function to fetch literacy data from the backend
    async function fetchLiteracyData() {
        try {
            // In a real scenario, you might fetch from /api/literacy/data
            // For now, we'll simulate loading from a local JSON structure
            const response = await fetch('/data/literacy.json'); // Direct fetch for development ease
            literacyData = await response.json();
            displayPlatforms();
        } catch (error) {
            console.error('Error fetching literacy data:', error);
            guideContent.innerHTML = '<p>Could not load literacy guide. Please try again later.</p>';
        }
    }

    // Function to display platform buttons
    function displayPlatforms() {
        platformsList.innerHTML = ''; // Clear existing buttons
        for (const platform in literacyData) {
            const button = document.createElement('button');
            button.classList.add('platform-button');
            button.textContent = platform;
            button.dataset.platform = platform;
            button.addEventListener('click', () => displayPlatformContent(platform));
            platformsList.appendChild(button);
        }
    }

    // Function to display content for a selected platform
    function displayPlatformContent(platform) {
        // Remove active class from all buttons
        document.querySelectorAll('.platform-button').forEach(btn => {
            btn.classList.remove('active');
        });
        // Add active class to the clicked button
        document.querySelector(`.platform-button[data-platform="${platform}"]`).classList.add('active');


        const data = literacyData[platform];
        if (data) {
            let htmlContent = `<h3>${data.title}</h3><p>${data.description}</p><ul>`;
            data.checklist.forEach(item => {
                htmlContent += `<li>${item}</li>`;
            });
            htmlContent += `</ul>`;
            guideContent.innerHTML = htmlContent;
        } else {
            guideContent.innerHTML = `<p>No content available for ${platform}.</p>`;
        }
    }

    // Initial load
    fetchLiteracyData();
});
