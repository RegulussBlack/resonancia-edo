# Resonancia: EDO de primer orden, Heun y RK4 aplicados a la escucha musical guiada

**Materia:** Métodos Numéricos · **Desafío individual:** modelar un problema real con ecuaciones diferenciales
**Autor:** Mario Fabricio Murillo Peñaranda

🔗 **Aplicación web:** `https://TU_USUARIO.github.io/TU_REPOSITORIO/`
🎥 **Video (1 min):** `PEGAR_ENLACE_DEL_VIDEO`

> ⚠️ Todos los parámetros (k por pieza musical, y_b, datos de ejemplo) son **hipotéticos**. Las simulaciones **no son predicciones comprobadas** ni un tratamiento clínico. La música puede acompañar el autocuidado, pero no reemplaza a psicología o psiquiatría.

## 1. Problema y contexto
Comunidad: estudiantes universitarios con estrés, ansiedad o ánimo bajo. **Pregunta:** si el malestar autopercibido inicial es y₀, ¿en cuántos minutos de escucha musical guiada baja hasta la meta de 40 puntos, con y sin música?

## 2. Modelo matemático
EDO de primer orden con condición inicial:

    dy/dt = -k (y - y_b),    y(0) = y0

| Símbolo | Significado | Unidad |
|---|---|---|
| y(t) | malestar autopercibido (autoevaluación) | puntos (0–100) |
| t | tiempo de la sesión | minutos |
| y₀ | malestar inicial | puntos |
| y_b | nivel de calma alcanzable | puntos |
| k | tasa de relajación (mayor con música guiada) | 1/min |

**Supuestos:** k y y_b constantes; sin nuevos estresores; medición por autoevaluación; intervalo t ∈ [0, T].

## 3. Solución analítica
Separando variables: `y(t) = y_b + (y0 - y_b) e^(-k t)`. Tiempo hasta la meta U: `t* = ln((y0 - y_b)/(U - y_b)) / k`.
Verificación: y(0) = y₀ ✓ y y′ = −k(y − y_b) ✓.

## 4. Métodos numéricos
Heun (Runge-Kutta de orden 2) y RK4, con los mismos parámetros, condición inicial, intervalo y paso h. Con y₀=80, y_b=20, k=0,05, T=60: error máximo con h=10 → Heun 1,365 y RK4 0,0175; con h=5 → Heun 0,279 y RK4 0,00089. RK4 produjo el menor error.

## 5. Aplicación web
`index.html` es una página estática (HTML + JavaScript, sin instalación ni dependencias). Permite ajustar y₀, y_b, k, h, T y la meta; valida entradas; muestra la solución analítica, tabla por pasos, gráficas, errores y una interpretación. Incluye un panel de calibración de k por regresión y un chatbot que reproduce música clásica sintetizada.

**Ejecutar local:** abrir `index.html` en el navegador. **Publicar:** GitHub Pages (Settings → Pages → Deploy from a branch → `main` / root).

## 6. Base de datos (ciencia de datos)
Carpeta `database/` (SQLite, SQL estándar) con 8 tablas y una vista: `estudiante`, `pieza_musical`, `emocion`, `recomendacion` (N:M), `sesion`, `registro`, `simulacion`, `calibracion`, `v_error_por_metodo`. Datos hipotéticos y seudonimizados; no se guardan nombres reales ni mensajes del chatbot.

    python database/construir_db.py     # crea database/resonancia.db
    python python/calibrar_k.py         # estima k por regresión y llena calibracion

Consultas de ejemplo en `database/consultas.sql`. Requiere Python 3.8+ (solo librería estándar).

## 7. Estructura
    index.html              aplicación web
    database/               schema.sql, seed.sql, consultas.sql, construir_db.py
    python/                 calibrar_k.py, generar_seed.py
    LICENSE · README.md

## 8. Limitaciones
Modelo de un solo nivel de calma y k constante; malestar autopercibido y variable entre personas; sin datos clínicos reales que respalden los valores de k.
