const express = require("express");
const cors = require("cors");
const { Pool } = require("pg");
require("dotenv").config();

const app = express();

app.use(cors());
app.use(express.json());

// CONEXIÓN NEON
const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

// GUARDAR SERVIDOR
app.post("/servidores", async (req, res) => {
    const {
        nombre_servidor,
        host,
        name_bd,
        user_bd,
        pass_bd
    } = req.body;

    try {
        const result = await pool.query(
            `INSERT INTO servidores 
            (nombre_servidor, host, name_bd, user_bd, pass_bd)
            VALUES ($1,$2,$3,$4,$5)
            RETURNING *`,
            [nombre_servidor, host, name_bd, user_bd, pass_bd]
        );

        res.json(result.rows[0]);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.listen(8000, () => {
    console.log("Servidor corriendo en http://localhost:8000");
});

app.get("/servidores", async (req, res) => {
    try {
        const result = await pool.query(
            "SELECT * FROM servidores ORDER BY id DESC"
        );

        res.json(result.rows);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});