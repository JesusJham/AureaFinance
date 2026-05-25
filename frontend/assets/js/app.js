const API = "http://localhost:8000";

async function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Completa todos los campos");
        return;
    }

    try {
        const res = await fetch(`${API}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            window.location.href = "Carga.html";
        } else {
            alert("❌ " + data.detail);
        }
    } catch (error) {
        alert("❌ No se pudo conectar al servidor");
    }
}

async function register(event) {
    event.preventDefault();

    const nombres   = document.getElementById("name").value.trim();
    const apellidos = document.getElementById("lastname").value.trim();
    const email     = document.getElementById("email").value.trim();
    const username  = document.getElementById("username").value.trim();
    const password  = document.getElementById("password").value;

    if (!nombres || !apellidos || !email || !username || !password) {
        alert("Completa todos los campos");
        return;
    }

    try {
        const res = await fetch(`${API}/api/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombres, apellidos, email, username, password })
        });

        const data = await res.json();

        if (res.ok) {
            alert("✅ Cuenta creada correctamente");
            window.location.href = "login.html";
        } else {
            alert("❌ " + data.detail);
        }
    } catch (error) {
        alert("❌ No se pudo conectar al servidor");
    }
}



function logout() {
    localStorage.removeItem("token");

    window.location.href = "Login.html";
}



function selectFile() {
    document.getElementById("fileInput").click();
}



function handleFile(event) {
    const file = event.target.files[0];

    if (file) {
        alert("Archivo seleccionado: " + file.name);
    }
}



function togglePassword(id, icon) {
    const input = document.getElementById(id);

    if (input.type === "password") {
        input.type = "text";

        icon.classList.remove("fa-eye");

        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";

        icon.classList.remove("fa-eye-slash");

        icon.classList.add("fa-eye");
    }
}



function showSection(id, element) {
    const sections = document.querySelectorAll(".server-section");

    sections.forEach((section) => {
        section.classList.remove("active");
    });

    document.getElementById(id).classList.add("active");

    const tabs = document.querySelectorAll(".tab-btn");

    tabs.forEach((tab) => {
        tab.classList.remove("active");
    });

    element.classList.add("active");
}



function testConnection() {
    alert("Conexión exitosa con SQL Server");
}



function saveServer() {
    alert("Servidor guardado correctamente");

    window.location.href = "Configurar.html";
}



function updateServer() {
    alert("Servidor actualizado correctamente");

    window.location.href = "Configurar.html";
}



function deleteServer() {
    const confirmDelete = confirm("¿Eliminar servidor?");

    if (confirmDelete) {
        alert("Servidor eliminado");

        window.location.href = "Configurar.html";
    }
}