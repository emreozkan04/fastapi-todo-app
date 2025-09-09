// app/static/javascript/script.js

// --- DOM Elements ---
const todoForm = document.getElementById('add-todo-form');
const todoList = document.getElementById('todo-list');
const editModal = document.getElementById('edit-modal');
const editForm = document.getElementById('edit-form');
const cancelEditBtn = document.getElementById('cancel-edit-btn');
const deleteModal = document.getElementById('delete-modal');
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
const logoutBtn = document.getElementById('logout-btn');

let todoIdToDelete = null;

// --- Token Management ---
function getToken() {
    return localStorage.getItem('accessToken');
}

function logout() {
    localStorage.removeItem('accessToken');
    window.location.href = '/login';
}

// --- Generic API Fetch Function ---
async function apiFetch(endpoint, options = {}) {
    const token = getToken();
    const headers = { 'Content-Type': 'application/json', ...options.headers };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(endpoint, { ...options, headers }); // <-- CORRECTED

    if (response.status === 401) {
        logout();
        throw new Error('Your session has expired. Please log in again.');
    }
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'An API error occurred');
    }
    
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.includes("application/json")) {
        return response.json();
    }
}

// --- API Functions with Error Handling ---
async function getTodos() {
    try {
        const todos = await apiFetch('/todos');
        if (todos) {
            renderTodos(todos);
        }
    } catch (error) {
        alert(`Error fetching todos: ${error.message}`);
    }
}

async function addTodo(todo) {
    try {
        await apiFetch('/create_todo', {
            method: 'POST',
            body: JSON.stringify(todo),
        });
        getTodos();
    } catch (error) {
        alert(`Error adding todo: ${error.message}`);
    }
}

async function updateTodo(id, todo) {
    try {
        await apiFetch(`/todo/${id}`, {
            method: 'PUT',
            body: JSON.stringify(todo),
        });
        getTodos();
    } catch (error) {
        alert(`Error updating todo: ${error.message}`);
    }
}

async function performDeleteTodo(id) {
    try {
        await apiFetch(`/todo/${id}`, { method: 'DELETE' });
        getTodos();
    } catch (error) {
        alert(`Error deleting todo: ${error.message}`);
    }
}

// --- Rendering Logic ---
function renderTodos(todos) {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const todoItem = document.createElement('div');
        todoItem.className = `todo-item priority-${getPriorityName(todo.priority).toLowerCase()}`;
        
        const todoJsonString = JSON.stringify(todo).replace(/'/g, "&apos;");

        todoItem.innerHTML = `
            <div class="todo-details">
                <h3>${todo.title}</h3>
                <p>${todo.description || ''}</p>
            </div>
            <div class="todo-actions">
                <button class="edit-btn" onclick='openEditModal(${todoJsonString})'>Edit</button>
                <button class="delete-btn" onclick="openDeleteModal(${todo.id})">Delete</button>
            </div>
        `;
        todoList.appendChild(todoItem);
    });
}


// --- Modal Logic ---
function openEditModal(todo) {
    document.getElementById('edit-todo-id').value = todo.id;
    document.getElementById('edit-title').value = todo.title;
    document.getElementById('edit-description').value = todo.description || '';
    document.getElementById('edit-priority').value = todo.priority;
    editModal.style.display = 'flex';
}

function closeEditModal() {
    editModal.style.display = 'none';
}

function openDeleteModal(id) {
    todoIdToDelete = id;
    deleteModal.style.display = 'flex';
}

function closeDeleteModal() {
    todoIdToDelete = null;
    deleteModal.style.display = 'none';
}

// --- Event Listeners ---
logoutBtn.addEventListener('click', logout);

todoForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const newTodo = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        priority: parseInt(document.getElementById('priority').value),
    };
    await addTodo(newTodo);
    todoForm.reset();
});

editForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const id = document.getElementById('edit-todo-id').value;
    const updatedTodo = {
        title: document.getElementById('edit-title').value,
        description: document.getElementById('edit-description').value,
        priority: parseInt(document.getElementById('edit-priority').value)
    };
    await updateTodo(id, updatedTodo);
    closeEditModal();
});

cancelEditBtn.addEventListener('click', closeEditModal);

confirmDeleteBtn.addEventListener('click', async () => {
    if (todoIdToDelete) {
        await performDeleteTodo(todoIdToDelete);
        closeDeleteModal();
    }
});

cancelDeleteBtn.addEventListener('click', closeDeleteModal);

// --- Utility ---
function getPriorityName(priority) {
    switch (priority) {
        case 1: return 'Low';
        case 2: return 'Medium';
        case 3: return 'High';
        default: return '';
    }
}

// --- Initial App Load ---
function initializeApp() {
    if (!getToken()) {
        window.location.href = '/login';
        return;
    }
    getTodos();
}

initializeApp();