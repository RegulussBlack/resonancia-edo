"""Estima k por regresión lineal: ln(y - yb) = ln(y0 - yb) - k*t  (solo librería estándar).
Uso: python python/calibrar_k.py   (requiere haber creado la base con database/construir_db.py)"""
import sqlite3, math, pathlib
db = pathlib.Path(__file__).resolve().parent.parent / "database" / "resonancia.db"
con = sqlite3.connect(db)
con.execute("DELETE FROM calibracion")
print(f"{'sesion':>6} {'k_modelo':>9} {'k_est':>8} {'R2':>7} {'RMSE':>6} {'n':>3}")
for sid, yb, kmod in con.execute("SELECT id_sesion, yb, k_modelo FROM sesion").fetchall():
    pts = [(t, y) for t, y in con.execute("SELECT t_min, malestar FROM registro WHERE id_sesion=? ORDER BY t_min", (sid,)) if y > yb]
    if len(pts) < 3: continue
    n = len(pts); mt = sum(t for t,_ in pts)/n; z = [math.log(y-yb) for _,y in pts]; mz = sum(z)/n
    sxx = sum((t-mt)**2 for t,_ in pts); sxy = sum((t-mt)*(zi-mz) for (t,_),zi in zip(pts,z))
    if sxx == 0 or sxy >= 0: continue
    s = sxy/sxx; c = mz - s*mt
    ssr = sum((zi-(c+s*t))**2 for (t,_),zi in zip(pts,z)); sst = sum((zi-mz)**2 for zi in z)
    rmse = math.sqrt(sum((y-(yb+math.exp(c+s*t)))**2 for t,y in pts)/n)
    r2 = 1 - ssr/sst; k = -s
    con.execute("INSERT INTO calibracion VALUES (?,?,?,?,?)", (sid, k, r2, rmse, n))
    print(f"{sid:>6} {kmod:>9.3f} {k:>8.4f} {r2:>7.4f} {rmse:>6.2f} {n:>3}")
con.commit(); con.close()
