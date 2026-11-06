-- Resonancia · Base de datos del proyecto (SQL estándar, probado en SQLite)
-- Todos los datos son HIPOTÉTICOS. No almacenar datos personales ni mensajes del chatbot.
PRAGMA foreign_keys = ON;

CREATE TABLE estudiante (
  id_estudiante INTEGER PRIMARY KEY,
  alias         TEXT NOT NULL UNIQUE,          -- seudónimo, nunca el nombre real
  carrera       TEXT NOT NULL,
  semestre      INTEGER NOT NULL CHECK (semestre BETWEEN 1 AND 12)
);

CREATE TABLE pieza_musical (
  id_pieza     INTEGER PRIMARY KEY,
  compositor   TEXT NOT NULL,
  titulo       TEXT NOT NULL,
  tonalidad    TEXT,
  k_hipotetico REAL NOT NULL CHECK (k_hipotetico > 0),  -- 1/min, supuesto del modelo
  UNIQUE (compositor, titulo)
);

CREATE TABLE emocion (
  id_emocion INTEGER PRIMARY KEY,
  nombre     TEXT NOT NULL UNIQUE
);

CREATE TABLE recomendacion (                     -- relación N:M emoción–pieza
  id_emocion INTEGER NOT NULL REFERENCES emocion(id_emocion),
  id_pieza   INTEGER NOT NULL REFERENCES pieza_musical(id_pieza),
  PRIMARY KEY (id_emocion, id_pieza)
);

CREATE TABLE sesion (
  id_sesion     INTEGER PRIMARY KEY,
  id_estudiante INTEGER NOT NULL REFERENCES estudiante(id_estudiante),
  id_pieza      INTEGER REFERENCES pieza_musical(id_pieza),   -- NULL = sin música
  id_emocion    INTEGER REFERENCES emocion(id_emocion),
  fecha_hora    TEXT NOT NULL,                                -- ISO 8601
  y0            REAL NOT NULL CHECK (y0 > 0 AND y0 <= 100),   -- puntos
  yb            REAL NOT NULL CHECK (yb >= 0 AND yb < 100),   -- puntos
  k_modelo      REAL NOT NULL CHECK (k_modelo > 0),           -- 1/min
  h_min         REAL NOT NULL CHECK (h_min > 0),
  t_total_min   REAL NOT NULL CHECK (t_total_min > 0),
  meta          REAL NOT NULL CHECK (meta > 0 AND meta < 100),
  CHECK (yb < y0)
);

CREATE TABLE registro (                          -- autoevaluaciones durante la sesión
  id_registro INTEGER PRIMARY KEY,
  id_sesion   INTEGER NOT NULL REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  t_min       REAL NOT NULL CHECK (t_min >= 0),
  malestar    REAL NOT NULL CHECK (malestar BETWEEN 0 AND 100),
  UNIQUE (id_sesion, t_min)
);

CREATE TABLE simulacion (                        -- resultados numéricos por paso
  id_sesion     INTEGER NOT NULL REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  metodo        TEXT NOT NULL CHECK (metodo IN ('ANALITICA','HEUN','RK4')),
  t_min         REAL NOT NULL,
  valor         REAL NOT NULL,
  error_abs     REAL,
  error_rel_pct REAL,
  PRIMARY KEY (id_sesion, metodo, t_min)
);

CREATE TABLE calibracion (                       -- k estimado por regresión (ciencia de datos)
  id_sesion   INTEGER PRIMARY KEY REFERENCES sesion(id_sesion) ON DELETE CASCADE,
  k_estimado  REAL NOT NULL,
  r2          REAL,
  rmse        REAL,
  n_registros INTEGER NOT NULL
);

CREATE VIEW v_error_por_metodo AS
SELECT id_sesion, metodo,
       MAX(error_abs)     AS error_abs_max,
       MAX(error_rel_pct) AS error_rel_max_pct
FROM simulacion WHERE metodo <> 'ANALITICA'
GROUP BY id_sesion, metodo;
