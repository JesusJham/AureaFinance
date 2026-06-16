/*-- const API = window.API_BASE_URL || "http://localhost:8000/api"; */
const API = "https://aureafinance.onrender.com/api";
let selectedFile = null;
let currentDataEntryId = null;
let selectedFileCarga = null;
let dataEntriesCarga = [];

async function login(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Completa todos los campos");
        return;
    }

    try {
        const res = await fetch(`${API}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (res.ok) {
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("usuario", JSON.stringify(data.usuario));
            window.location.href = "/frontend/pages/carga.html";
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
        const res = await fetch(`${API}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombres, apellidos, email, username, password })
        });

        const data = await res.json();

        if (res.ok) {
            alert("✅ Cuenta creada correctamente");
            window.location.href = "/frontend/pages/login.html";
        } else {
            alert("❌ " + data.detail);
        }
    } catch (error) {
        alert("❌ No se pudo conectar al servidor");
    }
}



function logout() {
    localStorage.removeItem("token");

    window.location.href = "/frontend/pages/login.html";
}



function selectFile() {
    document.getElementById("fileInput").click();
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



async function testConnection() {

    const data = {
        nombre_servidor: document.getElementById("addNombreServidor").value,
        tipo_bd: document.getElementById("addTipoBD").value,
        host: document.getElementById("addHost").value,
        puerto: document.getElementById("addPuerto").value,
        name_bd: document.getElementById("addNameBD").value,
        user_bd: document.getElementById("addUserBD").value,
        pass_bd: document.getElementById("addPassword").value,
        ssl_mode: document.getElementById("addSslMode").value
    };

    try {

        const res = await fetch(`${API}/servidores/test-connection`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {

            alert("✅ Conexión exitosa");

        } else {

            alert("❌ " + result.detail);
        }

    } catch (error) {

        console.error(error);

        alert("❌ Error conectando con el servidor");
    }
}



async function saveServer() {
    const inputs = document.querySelectorAll(".server-form-card input");

    const data = {
    nombre_servidor: document.getElementById("addNombreServidor").value,
    tipo_bd: document.getElementById("addTipoBD").value,
    host: document.getElementById("addHost").value,
    puerto: Number(document.getElementById("addPuerto").value),
    name_bd: document.getElementById("addNameBD").value,
    user_bd: document.getElementById("addUserBD").value,
    pass_bd: document.getElementById("addPassword").value,
    ssl_mode: document.getElementById("addSslMode").value
    };

    if (!data.nombre_servidor || !data.host || !data.name_bd || !data.user_bd || !data.pass_bd) {
        alert("Completa todos los campos");
        return;
    }

    try {
        const res = await fetch(`${API}/servidores`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        console.log("GUARDADO EN NEON:", result);

        alert("Servidor guardado en Neon");

        window.location.href  = "/frontend/pages/configurar.html";

    } catch (error) {
        console.error(error);
        alert("Error al guardar servidor");
    }
}



function updateServer() {
    alert("Servidor actualizado correctamente");

    window.location.href  = "/frontend/pages/configurar.html";
}



function deleteServer() {
    const confirmDelete = confirm("¿Eliminar servidor?");

    if (confirmDelete) {
        alert("Servidor eliminado");

        window.location.href  = "/frontend/pages/configurar.html";
    }
}

async function loadServers() {
    try {
        const res = await fetch(`${API}/servidores`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });
        const data = await res.json();

        console.log("SERVIDORES:", data);

        const tbody = document.getElementById("serversTable");

        tbody.innerHTML = "";

        if (!data || data.length === 0) {
            document.querySelector(".empty-state").style.display = "block";
            return;
        }

        document.querySelector(".empty-state").style.display = "none";

        data.forEach(server => {
            tbody.innerHTML += `
                <tr>
                    <td>${server.id}</td>
                    <td>${server.nombre_servidor}</td>
                    <td>
                        <span class="badge-db">
                            ${server.tipo_bd}
                        </span>
                    </td>
                    <td>${server.host}</td>
                    <td>${server.puerto}</td>
                    <td>${server.name_bd}</td>
                    <td>${server.user_bd}</td>
                    <td>${server.ssl_mode}</td>
                    <td>
                        <span style="color:green;font-weight:bold;">
                            ACTIVO
                        </span>
                    </td>
                    <td>
                        <button onclick="alert('Servidor ${server.id}')">
                            Ver
                        </button>
                    </td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Error cargando servidores:", error);
    }
}


let columnasArchivo = [];

function limpiarNombreColumna(nombre) {
    return nombre
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/[^a-zA-Z0-9_ ]/g, "")
        .trim()
        .replace(/\s+/g, "_")
        .toLowerCase();
}

function onTipoArchivoChange() {
    const tipo = document.getElementById("tipoArchivo").value;
    const separador = document.getElementById("separadorArchivo");

    if (tipo === "XLSX") {
        separador.disabled = true;
        separador.value = "";
    } else {
        separador.disabled = false;
    }
}



function selectFile() {
    document.getElementById("fileInput").click();
}

async function handleFile(event) {
    const file = event.target.files[0];

    if (!file) return;

    const tipoArchivo = document.getElementById("tipoArchivo").value;

    if (!tipoArchivo) {
        alert("Primero selecciona el tipo de archivo CSV o XLSX");
        event.target.value = "";
        selectedFile = null;
        return;
    }

    selectedFile = file;

    document.getElementById("fileNameText").innerText =
        `Archivo seleccionado: ${file.name}`;

    if (tipoArchivo === "CSV") {
        leerCSV(file);
    }

    if (tipoArchivo === "XLSX") {
        leerXLSX(file);
    }
}

function leerCSV(file) {
    const separador = document.getElementById("separadorArchivo").value || ",";
    const reader = new FileReader();

    reader.onload = function (e) {
        const texto = e.target.result;
        const lineas = texto.split(/\r?\n/).filter(x => x.trim() !== "");

        const headers = lineas[0].split(separador).map(x => x.trim());

        const filas = lineas.slice(1, 6).map(linea =>
            linea.split(separador).map(x => x.trim())
        );

        columnasArchivo = headers;

        pintarPreview(headers, filas);
        pintarMapping(headers);
    };

    reader.readAsText(file, document.getElementById("encodingArchivo").value || "UTF-8");
}

function leerXLSX(file) {
    const reader = new FileReader();

    reader.onload = function (e) {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: "array" });

        const sheetName = workbook.SheetNames[0];
        const sheet = workbook.Sheets[sheetName];

        const rows = XLSX.utils.sheet_to_json(sheet, {
            header: 1,
            defval: ""
        });

        const headers = rows[0];
        const filas = rows.slice(1, 6);

        columnasArchivo = headers;

        pintarPreview(headers, filas);
        pintarMapping(headers);
    };

    reader.readAsArrayBuffer(file);
}

function pintarPreview(headers, filas) {
    const table = document.getElementById("previewTable");

    table.innerHTML = `
        <thead>
            <tr>
                ${headers.map(h => `<th>${h}</th>`).join("")}
            </tr>
        </thead>
        <tbody>
            ${filas.map(row => `
                <tr>
                    ${headers.map((_, i) => `<td>${row[i] ?? ""}</td>`).join("")}
                </tr>
            `).join("")}
        </tbody>
    `;
}

function pintarMapping(headers) {
    const tbody = document.getElementById("mappingBody");

    tbody.innerHTML = "";

    headers.forEach((col, index) => {
        const limpia = limpiarNombreColumna(col);

        tbody.innerHTML += `
            <tr>

                <td>${index + 1}</td>

                <td>${col}</td>

                <td>
                    <input type="text" value="${limpia}" class="map-columna-limpia" />
                </td>

                <td>NVARCHAR(500)</td>

                <td>
                    <select class="map-tipo-destino">
                        <option value="VARCHAR(500)">VARCHAR(500)</option>
                        <option value="TEXT">TEXT</option>
                        <option value="INTEGER">INTEGER</option>
                        <option value="BIGINT">BIGINT</option>
                        <option value="DECIMAL(20,6)">DECIMAL(20,6)</option>
                        <option value="DOUBLE PRECISION">DOUBLE PRECISION</option>
                        <option value="DATE">DATE</option>
                        <option value="TIMESTAMP">TIMESTAMP</option>
                        <option value="BOOLEAN">BOOLEAN</option>
                    </select>
                </td>

                <td>
                    <select class="map-nulos">
                        <option value="true">Sí</option>
                        <option value="false">No</option>
                    </select>
                </td>

                <td>
                    <input type="checkbox" class="map-pk" />
                </td>

                <td>
                    <button class="delete-btn" onclick="this.closest('tr').remove()">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </td>

            </tr>
        `;
    });
}

function obtenerColumnasMapping() {
    const rows = document.querySelectorAll("#mappingBody tr");

    return Array.from(rows)
        .filter(row => !row.querySelector(".empty-row"))
        .map((row, index) => {
            const origenInput = row.querySelector(".map-columna-origen");

            return {
                columna_origen: origenInput
                    ? origenInput.value
                    : row.children[1].innerText,

                columna_limpia: row.querySelector(".map-columna-limpia").value,
                tipo_origen: "NVARCHAR(500)",
                tipo_destino: row.querySelector(".map-tipo-destino").value,
                permite_nulos: row.querySelector(".map-nulos").value === "true",
                es_primary_key: row.querySelector(".map-pk").checked,
                orden: index + 1
            };
        });
}

async function guardarDataEntry() {

    if (currentDataEntryId) {
        alert("⚠️ Esta carga ya fue guardada.");
        return currentDataEntryId;
    }

    const tipoCarga = document.getElementById("tipoCarga").value;
    const columnaFiltro =document.getElementById("columnaFiltro").value || null;
    const data = {
        servidor_id: Number(document.getElementById("selectServidor").value),
        nombre_tabla_raw: document.getElementById("tablaRaw").value,
        nombre_tabla_silver: document.getElementById("tablaSilver").value,
        esquema_raw: document.getElementById("selectEsquemaRaw").value,
        esquema_silver: document.getElementById("selectEsquemaSilver").value,
        tipo_archivo: document.getElementById("tipoArchivo").value,
        encoding: document.getElementById("encodingArchivo").value,
        separador: document.getElementById("separadorArchivo").value || null,
        tipo_carga: tipoCarga,
        columna_periodo:
            tipoCarga === "INCREMENTAL_PERIOD"
                ? columnaFiltro
                : null,
        columna_fecha:
            tipoCarga === "INCREMENTAL_DATE"
                ? columnaFiltro
                : null,

        columna_delete: columnaFiltro,
        columnas: obtenerColumnasMapping()
    };

    try {

        const res = await fetch(`${API}/data-entries/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization":
                    `Bearer ${localStorage.getItem("token")}`
            },

            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (res.ok) {
            currentDataEntryId = result.id;
            alert("✅ Carga guardada correctamente");
            return result.id;

        } else {
            alert(
                "❌ " +
                (result.detail || "Error al guardar configuración")
            );

            return null;
        }

    } catch (error) {
        console.error(error);
        alert("❌ Error de conexión con el servidor");
        return null;
    }
}

async function cargarServidoresCargaNueva() {
    const select = document.getElementById("selectServidor");
    if (!select) return;

    try {
        const res = await fetch(`${API}/servidores/`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        const servidores = await res.json();

        console.log("SERVIDORES PARA CARGA:", servidores);

        select.innerHTML = `<option value="">Seleccione servidor</option>`;

        servidores.forEach(srv => {
            select.innerHTML += `
                <option value="${srv.id}" data-bd="${srv.name_bd}">
                    ${srv.nombre_servidor} - ${srv.host}
                </option>
            `;
        });

    } catch (error) {
        console.error("Error cargando servidores:", error);
    }
}

async function onServidorChange() {
    const servidorId = document.getElementById("selectServidor").value;
    const selectBD = document.getElementById("selectBaseDatos");
    const selectRaw = document.getElementById("selectEsquemaRaw");
    const selectSilver = document.getElementById("selectEsquemaSilver");

    selectBD.innerHTML = `<option value="">Seleccione BD</option>`;
    selectRaw.innerHTML = `<option value="">Seleccione esquema RAW</option>`;
    selectSilver.innerHTML = `<option value="">Seleccione esquema SILVER</option>`;

    if (!servidorId) return;

    const option = document.querySelector(`#selectServidor option[value="${servidorId}"]`);
    const nombreBD = option.getAttribute("data-bd");

    selectBD.innerHTML = `<option value="${nombreBD}">${nombreBD}</option>`;

    try {
        const res = await fetch(`${API}/servidores/${servidorId}/schemas`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`
            }
        });

        const schemas = await res.json();

        if (!res.ok) {
            alert("❌ " + JSON.stringify(schemas.detail));
            return;
        }

        schemas.forEach(schema => {
            selectRaw.innerHTML += `<option value="${schema}">${schema}</option>`;
            selectSilver.innerHTML += `<option value="${schema}">${schema}</option>`;
        });

    } catch (error) {
        console.error(error);
        alert("❌ Error cargando esquemas");
    }
}

function agregarColumnaManual() {
    const tbody = document.getElementById("mappingBody");

    const emptyRow = tbody.querySelector(".empty-row");
    if (emptyRow) {
        tbody.innerHTML = "";
    }

    const index = tbody.querySelectorAll("tr").length + 1;

    tbody.innerHTML += `
        <tr>
            <td>${index}</td>

            <td>
                <input type="text" class="map-columna-origen" placeholder="Columna archivo" />
            </td>

            <td>
                <input type="text" class="map-columna-limpia" placeholder="columnaDestino" />
            </td>

            <td>NVARCHAR(500)</td>

            <td>
                <select class="map-tipo-destino">
                    <option value="VARCHAR(500)">VARCHAR(500)</option>
                    <option value="TEXT">TEXT</option>
                    <option value="INTEGER">INTEGER</option>
                    <option value="BIGINT">BIGINT</option>
                    <option value="DECIMAL(20,6)">DECIMAL(20,6)</option>
                    <option value="DOUBLE PRECISION">DOUBLE PRECISION</option>
                    <option value="DATE">DATE</option>
                    <option value="TIMESTAMP">TIMESTAMP</option>
                    <option value="BOOLEAN">BOOLEAN</option>
                </select>
            </td>

            <td>
                <select class="map-nulos">
                    <option value="true">Sí</option>
                    <option value="false">No</option>
                </select>
            </td>

            <td>
                <input type="checkbox" class="map-pk" />
            </td>

            <td>
                <button class="delete-btn" onclick="this.closest('tr').remove(); renumerarColumnas();">
                    <i class="fa-solid fa-trash"></i>
                </button>
            </td>
        </tr>
    `;
}
function renumerarColumnas() {
    const rows = document.querySelectorAll("#mappingBody tr");

    rows.forEach((row, index) => {
        row.children[0].innerText = index + 1;
    });
}

function construirMetadataCarga() {
    const tipoCarga = document.getElementById("tipoCarga").value;
    const columnaFiltro = document.getElementById("columnaFiltro").value || null;

    return {
        servidor_id: Number(document.getElementById("selectServidor").value),
        nombre_tabla_raw: document.getElementById("tablaRaw").value,
        nombre_tabla_silver: document.getElementById("tablaSilver").value,
        esquema_raw: document.getElementById("selectEsquemaRaw").value,
        esquema_silver: document.getElementById("selectEsquemaSilver").value,
        tipo_archivo: document.getElementById("tipoArchivo").value,
        encoding: document.getElementById("encodingArchivo").value,
        separador: document.getElementById("separadorArchivo").value || null,
        tipo_carga: tipoCarga,
        columna_periodo: tipoCarga === "INCREMENTAL_PERIOD" ? columnaFiltro : null,
        columna_fecha: tipoCarga === "INCREMENTAL_DATE" ? columnaFiltro : null,
        columna_delete: columnaFiltro,
        columnas: obtenerColumnasMapping()
    };
}

async function testCarga() {
    const data = construirMetadataCarga();

    const res = await fetch(`${API}/data-entries/test`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        alert("✅ " + result.mensaje);
    } else {
        alert("❌ " + JSON.stringify(result.detail));
    }
}

async function guardarDataEntry() {
    const data = construirMetadataCarga();

    const res = await fetch(`${API}/data-entries/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        currentDataEntryId = result.id;
        alert("✅ Configuración guardada/actualizada correctamente");
        return result.id;
    } else {
        alert("❌ " + JSON.stringify(result.detail));
        return null;
    }
}


async function ejecutarCarga() {
    if (!selectedFile) {
        alert("Primero selecciona un archivo");
        return;
    }

    const data = construirMetadataCarga();

    const formData = new FormData();
    formData.append("metadata", JSON.stringify(data));
    formData.append("archivo", selectedFile);

    if (currentDataEntryId) {
        formData.append("data_entry_id", currentDataEntryId);
    }

    const res = await fetch(`${API}/data-entries/execute`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: formData
    });

    const result = await res.json();

    if (res.ok) {
        currentDataEntryId = result.data_entry_id;
        alert(
            "✅ " + result.mensaje +
            "\nRegistros cargados: " + result.registros
        );

        window.location.href = "/frontend/pages/carga.html";
    } else {
        alert("❌ " + JSON.stringify(result.detail));
    }
}

async function cargarServidoresCarga() {
    const select = document.getElementById("loadServidor");
    if (!select) return;

    const res = await fetch(`${API}/servidores/`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });

    const servidores = await res.json();

    select.innerHTML = `<option value="">Seleccione servidor</option>`;

    servidores.forEach(srv => {
        select.innerHTML += `
            <option value="${srv.id}" data-bd="${srv.name_bd}">
                ${srv.nombre_servidor} - ${srv.host}
            </option>
        `;
    });
}

async function onLoadServidorChange() {
    const servidorId = document.getElementById("loadServidor").value;

    const selectBD = document.getElementById("loadBaseDatos");
    const selectEsquema = document.getElementById("loadEsquema");
    const selectTabla = document.getElementById("loadDataEntry");

    selectBD.innerHTML = `<option value="">Seleccione BD</option>`;
    selectEsquema.innerHTML = `<option value="">Seleccione esquema</option>`;
    selectTabla.innerHTML = `<option value="">Seleccione tabla</option>`;

    if (!servidorId) return;

    const option = document.querySelector(`#loadServidor option[value="${servidorId}"]`);
    const bd = option.getAttribute("data-bd");

    selectBD.innerHTML = `<option value="${bd}">${bd}</option>`;

    const res = await fetch(`${API}/data-entries/by-servidor/${servidorId}`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        }
    });

    dataEntriesCarga = await res.json();

    const esquemas = [
        ...new Set(
            dataEntriesCarga.flatMap(x => [
                x.esquema_raw,
                x.esquema_silver
            ])
        )
    ];

    selectEsquema.innerHTML = `<option value="">Seleccione esquema</option>`;

    esquemas.forEach(esq => {
        if (esq) {
            selectEsquema.innerHTML += `<option value="${esq}">${esq}</option>`;
        }
    });
}

function onLoadEsquemaChange() {
    const esquema = document.getElementById("loadEsquema").value;
    const selectTabla = document.getElementById("loadDataEntry");

    selectTabla.innerHTML = `<option value="">Seleccione tabla</option>`;

    const filtradas = dataEntriesCarga.filter(x =>
        x.esquema_raw === esquema || x.esquema_silver === esquema
    );

    filtradas.forEach(entry => {
        selectTabla.innerHTML += `
            <option value="${entry.id}">
                ${entry.nombre_tabla_silver}
            </option>
        `;
    });
}

function selectFileCarga() {
    document.getElementById("fileInputCarga").click();
}

function handleFileCarga(event) {
    const file = event.target.files[0];

    if (!file) return;

    selectedFileCarga = file;

    document.getElementById("fileNameCarga").innerText =
        `Archivo seleccionado: ${file.name}`;
}


async function validarArchivoCarga() {
    const dataEntryId = document.getElementById("loadDataEntry").value;

    if (!dataEntryId) {
        alert("Seleccione una tabla registrada");
        return;
    }

    if (!selectedFileCarga) {
        alert("Seleccione un archivo");
        return;
    }

    const formData = new FormData();
    formData.append("archivo", selectedFileCarga);

    const res = await fetch(`${API}/data-entries/${dataEntryId}/validate-file`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: formData
    });

    const result = await res.json();

    if (res.ok) {
        alert("✅ " + result.mensaje);
    } else {
        alert("❌ " + result.detail);
    }
}


async function ejecutarCargaRegistrada() {
    const dataEntryId = document.getElementById("loadDataEntry").value;

    if (!dataEntryId) {
        alert("Seleccione una tabla registrada");
        return;
    }

    if (!selectedFileCarga) {
        alert("Seleccione un archivo");
        return;
    }

    const formData = new FormData();
    formData.append("archivo", selectedFileCarga);

    const res = await fetch(`${API}/data-entries/${dataEntryId}/load-file`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`
        },
        body: formData
    });

    const result = await res.json();

    if (res.ok) {
        alert(
            "✅ Archivo cargado correctamente" +
            "\nRAW: " + result.raw +
            "\nSILVER: " + result.silver +
            "\nRegistros: " + result.registros
        );
    } else {
        console.error(result);

        alert(
            "❌ ERROR:\n\n" +
            JSON.stringify(result, null, 2)
        );
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("serversTable")) {
        loadServers();
    }

    if (document.getElementById("selectServidor")) {
        cargarServidoresCargaNueva();
    }

    if (document.getElementById("loadServidor")) {
        cargarServidoresCarga();
    }
});