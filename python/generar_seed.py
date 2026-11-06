"""Genera database/seed.sql con datos HIPOTÉTICOS y reproducibles (semilla fija)."""
import math, random
random.seed(2026)
out=[]
def ins(t,cols,vals): out.append(f"INSERT INTO {t} ({cols}) VALUES ({', '.join(vals)});")
q=lambda s:"'"+s.replace("'","''")+"'"
est=[("E01","Informática",5),("E02","Informática",7),("E03","Ingeniería de Sistemas",3),("E04","Informática",9),("E05","Estadística",4),("E06","Informática",6)]
for i,(a,c,s) in enumerate(est,1): ins("estudiante","id_estudiante,alias,carrera,semestre",[str(i),q(a),q(c),str(s)])
pz=[("Satie","Gymnopédie n.º 1","Re mayor",0.06),("Beethoven","Claro de luna (1.er mov.)","Do# menor",0.055),("Pachelbel","Canon en Re","Re mayor",0.05),("Bach","Preludio en Do mayor BWV 846","Do mayor",0.045)]
for i,(c,t,to,k) in enumerate(pz,1): ins("pieza_musical","id_pieza,compositor,titulo,tonalidad,k_hipotetico",[str(i),q(c),q(t),q(to),str(k)])
em=["Ansiedad","Estrés","Ánimo bajo","Insomnio","Falta de concentración"]
for i,n in enumerate(em,1): ins("emocion","id_emocion,nombre",[str(i),q(n)])
for e,p in [(1,1),(2,4),(3,3),(4,2),(5,4),(4,1)]: ins("recomendacion","id_emocion,id_pieza",[str(e),str(p)])
H,T,YB=10,60,20
def sim(y0,k,h):
    F=lambda t,y:-k*(y-YB);ex=lambda t:YB+(y0-YB)*math.exp(-k*t);yh=yr=y0;rows=[(0,y0,y0,y0)]
    for i in range(1,int(T/h)+1):
        t=(i-1)*h;p=yh+h*F(t,yh);yh=yh+h/2*(F(t,yh)+F(t+h,p))
        k1=F(t,yr);k2=F(t+h/2,yr+h/2*k1);k3=F(t+h/2,yr+h/2*k2);k4=F(t+h,yr+h*k3);yr+=h/6*(k1+2*k2+2*k3+k4)
        rows.append((i*h,ex(i*h),yh,yr))
    return rows
# (estudiante, pieza o None, emoción, y0)
ses=[(1,1,1,82),(2,4,2,75),(3,3,3,70),(4,2,4,68),(5,4,5,60),(6,3,2,88),(1,None,1,80),(3,None,2,72)]
rid=0
for sid,(e,p,m,y0) in enumerate(ses,1):
    k=pz[p-1][3] if p else 0.02
    ins("sesion","id_sesion,id_estudiante,id_pieza,id_emocion,fecha_hora,y0,yb,k_modelo,h_min,t_total_min,meta",
        [str(sid),str(e),str(p) if p else "NULL",str(m),q(f"2026-10-{10+sid:02d}T18:00:00"),str(y0),str(YB),str(k),str(H),str(T),"40"])
    kr=k*random.uniform(0.85,1.15)
    for t in (0,5,10,15,20,30,45):
        y=YB+(y0-YB)*math.exp(-kr*t)+(random.uniform(-2,2) if t else 0)
        rid+=1;ins("registro","id_registro,id_sesion,t_min,malestar",[str(rid),str(sid),str(t),str(round(min(100,max(0,y)),1))])
    if sid<=2:
        for t,ex_,yh,yr in sim(y0,k,H):
            for m_,v in (("ANALITICA",ex_),("HEUN",yh),("RK4",yr)):
                ea=abs(ex_-v);er=ea/abs(ex_)*100 if ex_ else 0
                ins("simulacion","id_sesion,metodo,t_min,valor,error_abs,error_rel_pct",[str(sid),q(m_),str(t),f"{v:.6f}",f"{ea:.8f}",f"{er:.8f}"])
open("database/seed.sql","w",encoding="utf-8").write("-- Datos HIPOTÉTICOS (generados por python/generar_seed.py)\nPRAGMA foreign_keys = ON;\n"+"\n".join(out)+"\n")
print("seed.sql listo:",len(out),"sentencias")
