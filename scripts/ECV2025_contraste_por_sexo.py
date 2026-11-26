# Uso: python ECV2025_contraste_por_sexo.py /ruta/a/los/5_zip_DANE
# P6020: sexo al nacer, 1 hombre, 2 mujer (diccionario DANE).
# Contrastes ponderados y estandarizados por sexo y edad (general), o por edad (estratos de sexo).
# IC aproximados por linealización; distribución común fija. No se exportan microdatos.
import pandas as pd,numpy as np,zipfile,glob,sys
from pathlib import Path
D=str(Path(sys.argv[1]).resolve())+'/' ; K=['DIRECTORIO','SECUENCIA_P','ORDEN']; H=K[:2]
def read(p,c):
 z=zipfile.ZipFile(glob.glob(D+p)[0]); f=next(x for x in z.namelist() if x.lower().endswith('.csv')); return pd.read_csv(z.open(f),sep=';',decimal=',',encoding='latin1',usecols=c,low_memory=False)
p=read('*Caracteristicas*',K+['P6040','P6020','P1895','P3175','P1905']); w=read('*Fuerza*',K+['P6240','P6250','P6260','P6270','P6280']);e=read('*Educacion*',K+['P8586']); d=read('*Variables*',K+['SEGMENTO','ESTRATO2020','FEX_C']);h=read('*Condiciones*',['DIRECTORIO','SECUENCIA_ENCUESTA','SECUENCIA_P','ORDEN','P9090']); assert h.ORDEN.eq(h.SECUENCIA_ENCUESTA).all() and h.SECUENCIA_P.eq(1).all();h=h.drop(columns=['SECUENCIA_P','SECUENCIA_ENCUESTA']).rename(columns={'ORDEN':'SECUENCIA_P'})
y=p[p.P6040.between(18,28)].copy(); n=len(y)
for df,k,v in [(w,K,'one_to_one'),(e,K,'one_to_one'),(d,K,'one_to_one'),(h,H,'many_to_one')]:
 y=y.merge(df,on=k,how='left',validate=v,indicator=True);assert y._merge.eq('both').all() and len(y)==n;y=y.drop(columns='_merge')
assert y[['P6020','P8586','P6240','P1895','P3175','P1905','P9090','FEX_C']].notna().all().all()
emp=y.P6240.eq(1)|y[['P6250','P6260','P6270']].eq(1).any(axis=1); study=y.P8586.eq(1); y['group']=np.select([emp&~study,~emp&~study&y.P6240.eq(4)],['work','home'],default='other');y['income']=y.P9090.ge(2).astype(float); y['age']=pd.cut(y.P6040,[17,21,25,28],labels=False);y['cell']=y.P6020.astype(str)+'_'+y.age.astype(str)
print('n',n,'households',len(y[H].drop_duplicates()),'sex',y.P6020.value_counts().to_dict())
a=y[y.group.ne('other')];print(a.groupby(['group','P6020']).FEX_C.agg(['count','sum']));print('weighted shares',a.groupby(['group','P6020']).FEX_C.sum()/a.groupby('group').FEX_C.sum())
idx=pd.MultiIndex.from_frame(d[['ESTRATO2020','SEGMENTO']].drop_duplicates())
def estimate(mask,var):
 x=y.loc[mask,['ESTRATO2020','SEGMENTO','FEX_C',var]].copy(); den=x.FEX_C.sum();m=(x.FEX_C*x[var]).sum()/den;x['u']=x.FEX_C*(x[var]-m)/den;u=x.groupby(['ESTRATO2020','SEGMENTO']).u.sum().reindex(idx,fill_value=0);return m,u
def se(u):
 s=u.groupby(level=0).agg(['count','var']);return np.sqrt((s['count']*s['var'].fillna(0)).sum())
for subset in ['all',1,2]:
 mask=y.group.ne('other') & (True if subset=='all' else y.P6020.eq(subset)); st=y[mask].groupby('cell').FEX_C.sum();st=st/st.sum(); print('subset',subset)
 for var in ['P1895','P1905','P3175','income']:
  result=[]
  for g in ['work','home']:
   vals=[estimate(mask&y.group.eq(g)&y.cell.eq(c),var) for c in st.index]; m=sum(w*x[0] for w,x in zip(st,vals));u=sum(w*x[1] for w,x in zip(st,vals));result.append((m,u))
  (wm,wu),(hm,hu)=result; delta=wm-hm; margin=1.96*se(wu-hu);scale=100 if var=='income' else 1;print(var, np.array([wm,hm,delta,delta-margin,delta+margin])*scale)
