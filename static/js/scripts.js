document.addEventListener('DOMContentLoaded', function() {
    // Modals Logic
    var modals = document.querySelectorAll('.modal');
    modals.forEach(function(modal) {
        modal.addEventListener('hidden.bs.modal', function(e) {
            var iframe = modal.querySelector('iframe');
            if (iframe) {  // Check if iframe exists
                iframe.src = iframe.src;
            }
        });       
    });

    // Search Input Logic
    var searchInput = document.getElementById('search-input');
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            var query = this.value;
            if (query.length > 2) {
                fetch('/search/?q=' + query)
                    .then(response => response.json())
                    .then(data => displayResults(data))
                    .catch(error => console.error('Error fetching search results:', error));
            }
        });
    }

    // Dark Mode Logic
    var darkModeToggle = document.getElementById('darkModeToggle');
    var lightIcon = document.querySelector('.light-icon');
    var darkIcon = document.querySelector('.dark-icon');

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', function() {
            if (document.documentElement.getAttribute('data-bs-theme') === 'dark') {
                document.documentElement.removeAttribute('data-bs-theme');
                lightIcon.style.display = "";
                darkIcon.style.display = "none";
            } else {
                document.documentElement.setAttribute('data-bs-theme', 'dark');
                lightIcon.style.display = "none";
                darkIcon.style.display = "";
            }
        });
    }

    // Check for OS dark mode setting
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        // Set the attribute on the <html> element
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        
        lightIcon.style.display = "none";
        darkIcon.style.display = "";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Search dropdown hide logic
    const searchContainer = document.querySelector('.search-container');
    const dropdownResults = document.getElementById('live-search-results');

    document.addEventListener('click', function(event) {
        if (searchContainer && dropdownResults && !searchContainer.contains(event.target)) {
            dropdownResults.classList.remove('show'); // hide the dropdown
        }
    });

    // Watch button logic
    const watchButtons = document.querySelectorAll('.btn-watch');
    
    watchButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            e.preventDefault();

            const videoId = e.target.getAttribute('data-video-id');
            const privacyModal = document.getElementById('privacyModal-' + videoId);

            if (privacyModal) {
                const bsPrivacyModalInstance = bootstrap.Modal.getInstance(privacyModal);
                
                if (bsPrivacyModalInstance) {
                    bsPrivacyModalInstance.hide();
                }
                
                const bsPrivacyModal = new bootstrap.Modal(privacyModal);
                bsPrivacyModal.show();
            }
        });
    });
});

function embedVideo(videoId) {
    const privacyModal = document.getElementById('privacyModal-' + videoId);
    
    if (privacyModal) {
        const bsPrivacyModal = new bootstrap.Modal(privacyModal);
        bsPrivacyModal.hide();
    }

    const placeholder = document.querySelector('#videoModal-' + videoId + ' .video-placeholder');
    
    if (placeholder) {
        const videoUrl = placeholder.getAttribute('data-url');

        const iframe = document.createElement('iframe');
        iframe.width = "100%";
        iframe.height = "315";
        iframe.src = videoUrl;
        iframe.frameBorder = "0";
        iframe.allowFullscreen = true;

        // Replace the placeholder with the iframe
        placeholder.replaceWith(iframe);
    }

    const videoModal = document.getElementById('videoModal-' + videoId);
    
    if (videoModal) {
        const bsVideoModal = new bootstrap.Modal(videoModal);
        bsVideoModal.show();
    }
}

function displayResults(data) {
    var resultsDiv = document.getElementById('live-search-results');
    while (resultsDiv.firstChild) {
        resultsDiv.removeChild(resultsDiv.firstChild);
    }

    if (data.length === 0) {
        var p = document.createElement('p');
        p.textContent = 'No results found.';
        resultsDiv.appendChild(p);
    } else {
        data.forEach(function(item) {
            var a = document.createElement('a');
            a.href = item.url;
            a.classList.add('dropdown-item');
            a.classList.add('search-result');  // Add the search-result class to identify this as a search result
            a.setAttribute('data-content-text', item.title);  // Add the unique identifier or title
            a.textContent = item.title;
            resultsDiv.appendChild(a);
        });
    }

    if (data.length > 0) {
        var dropdown = new bootstrap.Dropdown(resultsDiv.parentElement);
        dropdown.show();
    }
};

// Event listener for search results
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('search-result')) {
            e.preventDefault(); // Prevent default action

            // Extract content text from the clicked search result
            let contentText = e.target.getAttribute('data-content-text');

            // Search for elements containing the contentText
            let contentElements = document.querySelectorAll('.d-flex .soft-text');
            for (let elem of contentElements) {
                if (elem.textContent.includes(contentText)) {
                    // Find the parent module/submodule of the matched content
                    let moduleElem = elem.closest('.card');

                    // Use Bootstrap's API to show (expand) the target
                    let bsCollapse = new bootstrap.Collapse(moduleElem.querySelector('.collapse'), {
                        toggle: true
                    });
                    bsCollapse.show();

                    // Exit the loop once we've found and expanded the module
                    break;
                }
            }
        }
    });
});
