// app/static/javascript/login.js

// --- DOM Elements ---
const loginContainer = document.getElementById('login-container');
const registerContainer = document.getElementById('register-container');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const showRegisterBtn = document.getElementById('show-register-btn');
const showLoginBtn = document.getElementById('show-login-btn');

// --- Token Management ---
function saveToken(token) {
    localStorage.setItem('accessToken', token);
}

// --- Auth Functions ---
async function login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await fetch(`/login`, { // <-- CORRECTED
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
    }

    const tokenData = await response.json();
    saveToken(tokenData.access_token);
    window.location.href = '/';
}

async function register(email, password) {
    const response = await fetch(`/register`, { // <-- CORRECTED
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });
    
    if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Registration failed');
    }
    
    await login(email, password);
}

// --- Event Listeners ---
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    try {
        await login(email, password);
    } catch (error) {
        alert(error.message);
    }
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    try {
        await register(email, password);
    } catch (error) {
        alert(error.message);
    }
});

showRegisterBtn.addEventListener('click', (e) => {
    e.preventDefault();
    loginContainer.style.display = 'none';
    registerContainer.style.display = 'block';
});

showLoginBtn.addEventListener('click', (e) => {
    e.preventDefault();
    registerContainer.style.display = 'none';
    loginContainer.style.display = 'block';
});

// Check if user is already logged in and redirect
if (localStorage.getItem('accessToken')) {
    window.location.href = '/';
}