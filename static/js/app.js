// Get authentication token from cookie
function getAuthToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'access_token') {
            return value;
        }
    }
    return null;
}

// Helper function to make API calls
async function apiCall(url, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };
    
    if (token) {
        headers['Authorization'] = token;
    }
    
    const response = await fetch(url, {
        ...options,
        headers
    });
    
    if (!response.ok) {
        if (response.status === 401) {
            // Unauthorized, redirect to login
            window.location.href = '/login';
            return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return response.json();
}

// Load todos on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadTodos();
    
    // Form submission
    const form = document.getElementById('todo-form');
    if (form) {
        form.addEventListener('submit', handleCreateTodo);
    }
    
    // Checkbox changes
    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleToggleTodo);
    });
    
    // Delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDeleteTodo);
    });
});

// Load todos from API
async function loadTodos() {
    try {
        const todos = await apiCall('/todos');
        renderTodos(todos);
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

// Render todos to the page
function renderTodos(todos) {
    const todosList = document.getElementById('todos-list');
    if (!todosList) return;
    
    todosList.innerHTML = todos.map(todo => `
        <div class="todo-item" data-id="${todo.id}">
            <div class="todo-header">
                <input type="checkbox" class="todo-checkbox" ${todo.completed ? 'checked' : ''} data-id="${todo.id}">
                <h3 class="todo-title ${todo.completed ? 'completed' : ''}">${escapeHtml(todo.title)}</h3>
                <button class="delete-btn" data-id="${todo.id}">Delete</button>
            </div>
            ${todo.description ? `<p class="todo-description ${todo.completed ? 'completed' : ''}">${escapeHtml(todo.description)}</p>` : ''}
            <small class="todo-date">${formatDate(todo.created_at)}</small>
        </div>
    `).join('');
    
    // Reattach event listeners
    document.querySelectorAll('.todo-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', handleToggleTodo);
    });
    
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', handleDeleteTodo);
    });
}

// Handle create todo
async function handleCreateTodo(e) {
    e.preventDefault();
    
    const titleInput = document.getElementById('todo-title');
    const descriptionInput = document.getElementById('todo-description');
    
    const title = titleInput.value.trim();
    const description = descriptionInput.value.trim();
    
    if (!title) {
        alert('Please enter a todo title');
        return;
    }
    
    try {
        await apiCall('/todos', {
            method: 'POST',
            body: JSON.stringify({
                title,
                description: description || null
            })
        });
        
        // Clear form
        titleInput.value = '';
        descriptionInput.value = '';
        
        // Reload todos
        await loadTodos();
    } catch (error) {
        console.error('Error creating todo:', error);
        alert('Failed to create todo. Please try again.');
    }
}

// Handle toggle todo completion
async function handleToggleTodo(e) {
    const todoId = parseInt(e.target.dataset.id);
    const isCompleted = e.target.checked;
    
    try {
        await apiCall(`/todos/${todoId}`, {
            method: 'PUT',
            body: JSON.stringify({
                completed: isCompleted
            })
        });
        
        // Update UI
        const todoItem = e.target.closest('.todo-item');
        const title = todoItem.querySelector('.todo-title');
        const description = todoItem.querySelector('.todo-description');
        
        if (isCompleted) {
            title.classList.add('completed');
            if (description) description.classList.add('completed');
        } else {
            title.classList.remove('completed');
            if (description) description.classList.remove('completed');
        }
    } catch (error) {
        console.error('Error updating todo:', error);
        // Revert checkbox
        e.target.checked = !isCompleted;
        alert('Failed to update todo. Please try again.');
    }
}

// Handle delete todo
async function handleDeleteTodo(e) {
    const todoId = parseInt(e.target.dataset.id);
    
    if (!confirm('Are you sure you want to delete this todo?')) {
        return;
    }
    
    try {
        await apiCall(`/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        // Remove from UI
        const todoItem = e.target.closest('.todo-item');
        todoItem.remove();
    } catch (error) {
        console.error('Error deleting todo:', error);
        alert('Failed to delete todo. Please try again.');
    }
}

// Helper functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

