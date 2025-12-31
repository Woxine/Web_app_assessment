/**
 * AJAX Like Functionality
 */

function initLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) {
                alert('Please log in to like');
                return;
            }
            
            const type = this.getAttribute('data-type');
            const id = this.getAttribute('data-id');
            
            likeItem(type, id, this);
        });
    });
}

function likeItem(type, id, buttonElement) {
    // Prevent duplicate clicks
    if (buttonElement.getAttribute('data-processing') === 'true') {
        return;
    }
    buttonElement.setAttribute('data-processing', 'true');
    
    const url = `/api/like/${type}/${id}`;
    
    // Get CSRF token (from global variable or form)
    let token = window.csrfToken || '';
    if (!token) {
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        if (csrfInput) {
            token = csrfInput.value;
        }
    }
    
    // Send AJAX request
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': token
        },
        credentials: 'same-origin'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response error');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update like count and icon
            const likeIcon = buttonElement.querySelector('.like-icon');
            const likeCount = buttonElement.querySelector('.like-count');
            
            if (likeIcon) {
                likeIcon.textContent = data.is_liked ? '❤️' : '🤍';
            }
            
            if (likeCount) {
                likeCount.textContent = data.likes_count;
            }
        } else {
            alert('Operation failed, please try again');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Network error, please try again later');
    })
    .finally(() => {
        // Remove processing flag regardless of success or failure
        buttonElement.removeAttribute('data-processing');
    });
}

// Initialize after page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLikeButtons);
} else {
    initLikeButtons();
}

