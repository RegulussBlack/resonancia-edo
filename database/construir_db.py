"""Crea database/resonancia.db a partir de schema.sql y seed.sql. Uso: python database/construir_db.py"""
import sqlite3, pathlib
base = pathlib.Path(__file__).parent
db = base / "resonancia.db"
db.unlink(missing_ok=True)
con = sqlite3.connect(db)
for f in ("schema.sql", "seed.sql"):
    con.executescript((base / f).read_text(encoding="utf-8"))
con.commit()
for t in ("estudiante","pieza_musical","emocion","recomendacion","sesion","registro","simulacion"):
    print(f"{t:15s}", con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "filas")
con.close()
print("Base creada:", db)
