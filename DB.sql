-- Database: DB_APG_CJ

-- DROP DATABASE IF EXISTS "DB_APG_CJ";

CREATE DATABASE "DB_APG_CJ"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Spanish_Spain.1252'
    LC_CTYPE = 'Spanish_Spain.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "DB_APG_CJ"
    IS 'Esto es para el proyecto apg';

-- =========================
-- Tabla: public.usuarios
-- =========================
CREATE TABLE public.usuarios (
    id_usuario      SERIAL PRIMARY KEY,
    nick_name       VARCHAR NOT NULL UNIQUE,
    fecha           DATE NOT NULL,
    nombre          VARCHAR
);

-- =============================
-- Tabla: public.detalle_usuarios
-- =============================
CREATE TABLE public.detalle_usuarios (
    id_detalle_usuarios   SERIAL PRIMARY KEY,
    id_usuario            INTEGER NOT NULL REFERENCES public.usuarios(id_usuario) ON DELETE CASCADE,
    contrasena            TEXT NOT NULL,
    token                 TEXT,
    fecha_expiracion_token TIMESTAMP,
    grupo                 INTEGER NOT NULL,
    email                 VARCHAR NOT NULL UNIQUE,
    estado_cuenta         BOOLEAN NOT NULL
);
