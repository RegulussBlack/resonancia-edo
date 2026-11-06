-- Consultas de ejemplo (SQLite / SQL estándar)

-- 1) Sesiones con estudiante, pieza y emoción (JOIN múltiple)
SELECT s.id_sesion, e.alias, COALESCE(p.compositor||' - '||p.titulo,'Sin música') AS pieza,
       m.nombre AS emocion, s.y0, s.k_modelo
FROM sesion s
JOIN estudiante e ON e.id_estudiante = s.id_estudiante
LEFT JOIN pieza_musical p ON p.id_pieza = s.id_pieza
LEFT JOIN emocion m ON m.id_emocion = s.id_emocion
ORDER BY s.id_sesion;

-- 2) Tiempo teórico (analítico) hasta la meta: t* = ln((y0-yb)/(meta-yb))/k
SELECT id_sesion, ROUND(LN((y0-yb)/(meta-yb))/k_modelo, 2) AS t_estrella_min
FROM sesion;   -- si tu SQLite no tiene LN(), usa: python/calibrar_k.py o PostgreSQL/Oracle

-- 3) Malestar promedio por pieza en cada minuto registrado
SELECT COALESCE(p.titulo,'Sin música') AS pieza, r.t_min, ROUND(AVG(r.malestar),1) AS malestar_prom
FROM registro r
JOIN sesion s ON s.id_sesion = r.id_sesion
LEFT JOIN pieza_musical p ON p.id_pieza = s.id_pieza
GROUP BY pieza, r.t_min
ORDER BY pieza, r.t_min;

-- 4) Sesiones que alcanzaron la meta y en qué minuto (primer registro <= meta)
SELECT s.id_sesion, MIN(r.t_min) AS minuto_meta
FROM sesion s JOIN registro r ON r.id_sesion = s.id_sesion
WHERE r.malestar <= s.meta
GROUP BY s.id_sesion;

-- 5) Comparación de métodos numéricos (vista)
SELECT * FROM v_error_por_metodo ORDER BY id_sesion, metodo;

-- 6) k estimado vs k del modelo (calibración)
SELECT c.id_sesion, s.k_modelo, ROUND(c.k_estimado,4) AS k_estimado,
       ROUND(c.r2,4) AS r2, ROUND(c.rmse,2) AS rmse
FROM calibracion c JOIN sesion s ON s.id_sesion = c.id_sesion;

-- 7) Piezas recomendadas por emoción (relación N:M)
SELECT m.nombre AS emocion, p.compositor, p.titulo
FROM recomendacion r
JOIN emocion m ON m.id_emocion = r.id_emocion
JOIN pieza_musical p ON p.id_pieza = r.id_pieza
ORDER BY m.nombre;
