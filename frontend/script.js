// Ejecutar funciones al cargar el documento
document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("register-form");
    const loginForm = document.getElementById("login-form");
    const logoutButton = document.getElementById("logout-button");
    const startTestButton = document.getElementById("start-test-button");
    const changePasswordButton = document.getElementById("change-password-button");

    if (registerForm) {
        registerForm.addEventListener("submit", registerStudent);
    }
    if (loginForm) {
        loginForm.addEventListener("submit", loginUser);
    }
    if (logoutButton) {
        logoutButton.addEventListener("click", logout);
    }
    if (startTestButton) {
        startTestButton.addEventListener("click", startTest);
    }
    if (changePasswordButton) {
        changePasswordButton.addEventListener("click", changePassword);
    }

    const userNameElement = document.getElementById("user-name");
    if (userNameElement) {
        const userName = localStorage.getItem("userName");
        if (userName) {
            userNameElement.textContent = `Hola, ${userName}`;
            fetchUserResults();
        } else {
            window.location.href = "login.html"; 
        }
    }
});

function registerStudent(event) {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!name || !email || !password) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    fetch("http://127.0.0.1:5000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.href = "login.html";
        })
        .catch(error => console.error("Error:", error));
}

function loginUser(event) {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!email || !password) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
    })
        .then(response => response.json())
        .then(data => {
            localStorage.setItem("userId", data.userId);
            localStorage.setItem("userName", data.userName);
            window.location.href = "user_home.html";
        })
        .catch(error => console.error("Error:", error));
}

function logout() {
    localStorage.clear();
    window.location.href = "login.html";
}

// Función para cambiar la contraseña
function changePassword() {
    window.location.href = "change_password.html";
}

// Evento para manejar el formulario de cambio de contraseña
document.addEventListener("DOMContentLoaded", () => {
    const changePasswordForm = document.getElementById("change-password-form");
    if (changePasswordForm) {
        changePasswordForm.addEventListener("submit", handlePasswordChange);
    }
});

function handlePasswordChange(event) {
    event.preventDefault();

    const userId = localStorage.getItem("userId");
    const currentPassword = document.getElementById("current-password").value.trim();
    const newPassword = document.getElementById("new-password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    if (!currentPassword || !newPassword || !confirmPassword) {
        alert("Por favor, complete todos los campos.");
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("Las contraseñas no coinciden.");
        return;
    }

    fetch("http://127.0.0.1:5000/api/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId, currentPassword, newPassword }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al cambiar la contraseña.");
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            window.location.href = "user_home.html";
        })
        .catch(error => console.error("Error al cambiar contraseña:", error));
}

// Función para redirigir aleatoriamente a un ejercicio
function startTest() {
    const exercises = [
        "ejercicios/visuales/ejercicio1.html",
        "ejercicios/visuales/ejercicio2.html",
        "ejercicios/auditivos/ejercicio1.html",
        "ejercicios/auditivos/ejercicio2.html"
    ];
    const randomIndex = Math.floor(Math.random() * exercises.length);
    window.location.href = exercises[randomIndex];
}
