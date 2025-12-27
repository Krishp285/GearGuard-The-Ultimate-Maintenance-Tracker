// Kanban Drag and Drop Functionality

let draggedCard = null;

// Initialize drag and drop
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.kanban-card');
    const columns = document.querySelectorAll('.kanban-cards');
    
    // Add drag event listeners to cards
    cards.forEach(card => {
        card.addEventListener('dragstart', handleDragStart);
        card.addEventListener('dragend', handleDragEnd);
    });
    
    // Add drop event listeners to columns
    columns.forEach(column => {
        column.addEventListener('dragover', handleDragOver);
        column.addEventListener('drop', handleDrop);
        column.addEventListener('dragenter', handleDragEnter);
        column.addEventListener('dragleave', handleDragLeave);
    });
});

function handleDragStart(e) {
    draggedCard = this;
    this.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', this.innerHTML);
}

function handleDragEnd(e) {
    this.classList.remove('dragging');
}

function handleDragOver(e) {
    if (e.preventDefault) {
        e.preventDefault();
    }
    e.dataTransfer.dropEffect = 'move';
    return false;
}

function handleDragEnter(e) {
    this.classList.add('drag-over');
}

function handleDragLeave(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    if (e.stopPropagation) {
        e.stopPropagation();
    }
    
    this.classList.remove('drag-over');
    
    if (draggedCard !== this) {
        // Get the new status from the column
        const newStatus = this.closest('.kanban-column').dataset.status;
        const requestId = draggedCard.dataset.requestId;
        
        // Update status via API
        updateRequestStatus(requestId, newStatus);
        
        // Move the card visually
        this.appendChild(draggedCard);
        
        // Update badge count
        updateColumnBadges();
    }
    
    return false;
}

function updateRequestStatus(requestId, newStatus) {
    fetch('/requests/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            request_id: requestId,
            status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Status updated successfully');
            
            // Show a success message
            showNotification('Request moved to ' + newStatus, 'success');
            
            // If moved to Scrap, show additional notification
            if (newStatus === 'Scrap') {
                showNotification('Equipment has been marked as scrapped', 'warning');
            }
        } else {
            console.error('Error updating status:', data.message);
            showNotification('Error updating status: ' + data.message, 'error');
            // Reload page to restore correct state
            setTimeout(() => location.reload(), 2000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Network error occurred', 'error');
        setTimeout(() => location.reload(), 2000);
    });
}

function updateColumnBadges() {
    const columns = document.querySelectorAll('.kanban-column');
    columns.forEach(column => {
        const badge = column.querySelector('.badge');
        const cardsCount = column.querySelectorAll('.kanban-card').length;
        badge.textContent = cardsCount;
    });
}

function showNotification(message, type) {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.textContent = message;
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.zIndex = '9999';
    notification.style.minWidth = '300px';
    notification.style.animation = 'slideIn 0.3s ease-out';
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .drag-over {
        background: #e3f2fd;
        border: 2px dashed #2196f3;
    }
`;
document.head.appendChild(style);


function handleDrop(e) {
  e.preventDefault();
  this.classList.remove('drag-over');

  if (draggedCard) {
    draggedCard.classList.add('drop-animate');
    this.appendChild(draggedCard);

    setTimeout(() => {
      draggedCard.classList.remove('drop-animate');
    }, 300);

    updateColumnBadges();
  }
}
