/**
 * AJAX 点赞功能
 */

function initLikeButtons() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.disabled) {
                alert('请先登录以点赞');
                return;
            }
            
            const type = this.getAttribute('data-type');
            const id = this.getAttribute('data-id');
            
            likeItem(type, id, this);
        });
    });
}

function likeItem(type, id, buttonElement) {
    // 防止重复点击
    if (buttonElement.getAttribute('data-processing') === 'true') {
        return;
    }
    buttonElement.setAttribute('data-processing', 'true');
    
    const url = `/api/like/${type}/${id}`;
    
    // 获取 CSRF token (从全局变量或表单中)
    let token = window.csrfToken || '';
    if (!token) {
        const csrfInput = document.querySelector('input[name="csrf_token"]');
        if (csrfInput) {
            token = csrfInput.value;
        }
    }
    
    // 发送 AJAX 请求
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
            throw new Error('网络响应错误');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // 更新点赞数和图标
            const likeIcon = buttonElement.querySelector('.like-icon');
            const likeCount = buttonElement.querySelector('.like-count');
            
            if (likeIcon) {
                likeIcon.textContent = data.is_liked ? '❤️' : '🤍';
            }
            
            if (likeCount) {
                likeCount.textContent = data.likes_count;
            }
        } else {
            alert('操作失败，请重试');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('网络错误，请稍后重试');
    })
    .finally(() => {
        // 无论成功或失败，都移除处理标志
        buttonElement.removeAttribute('data-processing');
    });
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLikeButtons);
} else {
    initLikeButtons();
}

