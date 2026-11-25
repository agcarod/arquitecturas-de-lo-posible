# Ejecutar en el directorio de los ZIP; reutiliza la preparación verificada del piloto anterior.
from pathlib import Path
import sys
src=Path(__file__).with_name('piloto_ecv2025_soportes.py')
exec(src.read_text().split("print('total',len(y)")[0])
# Estándar común: distribución ponderada por sexo y edad en la unión de los dos grupos.
# Se fijan los pesos estándar estimados; IC condicionales a ese estándar (no incluye su incertidumbre).
y['ageband']=pd.cut(y.P6040,[17,21,25,28],labels=False)
y['cell']=y.P6020.astype(str)+'_'+y.ageband.astype(str)
std=y[y.grp.isin(['work','home'])].groupby('cell').FEX_C.sum(); std=std/std.sum()
for k in [7,8,9]: y[f'joint{k}']=y[f'all{k}']&y.enough

def standardized(g,col):
 vals=[estimate(y.grp.eq(g)&y.cell.eq(cell),col) for cell in std.index]
 assert min(v[2] for v in vals)>0
 return sum(a*v[0] for a,v in zip(std,vals)),sum(a*v[1] for a,v in zip(std,vals)),sum(v[2] for v in vals)
print('STANDARD, cells:',std.to_dict())
for col in ['P1895','P1905','P3175','enough','all7','all8','all9','joint7','joint8','joint9']:
 a,b=standardized('home',col),standardized('work',col); d=a[0]-b[0]; z=se(a[1]-b[1]); scale=1 if col.startswith('P') else 100
 print(col, 'home/work/diff/lo/hi',*[round(x*scale,3) for x in [a[0],b[0],d,d-1.96*z,d+1.96*z]])
print('Kish overall:', y.FEX_C.sum()**2/(y.FEX_C**2).sum())
print('cells unweighted:',y[y.grp.isin(['work','home'])].groupby(['grp','cell']).size().to_dict())
