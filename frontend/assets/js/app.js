function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;

    const password = document.getElementById("password").value;

    if (username === "" || password === "") {
        alert("Completa todos los campos");

        return;
    }

    localStorage.setItem("token", "aurea_session");

    window.location.href = "Carga.html";
}



function register(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;

    const lastname = document.getElementById("lastname").value;

    const email = document.getElementById("registerEmail").value;

    const username = document.getElementById("username").value;

    const password = document.getElementById("registerPassword").value;

    if (name === "" || lastname === "" || email === "" || username === "" || password === "") {
        alert("Completa todos los campos");

        return;
    }

    alert("Cuenta creada correctamente");

    window.location.href = "Login.html";
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