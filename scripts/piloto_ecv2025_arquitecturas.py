# Piloto descriptivo ECV 2025. Ejecutar: python piloto_ecv2025_arquitecturas.py /ruta/a/los/zip
# Dependencias: pandas, numpy. No escribe microdatos.
import pandas as pd, numpy as np, zipfile, glob, sys
from pathlib import Path
ROOT = Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
key=['DIRECTORIO','SECUENCIA_P','ORDEN']
def read(pattern, cols):
 p=glob.glob(str(ROOT / ('*'+pattern+'*.zip')))[0]; z=zipfile.ZipFile(p); f=next(n for n in z.namelist() if n.lower().endswith('.csv'))
 d=pd.read_csv(z.open(f),sep=';',decimal=',',encoding='latin1',usecols=cols); print(pattern,d.shape,'dups',d.duplicated(key).sum(),flush=True); return d
c=read('Caracteristicas',key+['P6040','P6020','P6051','P6087','P6088','P1895','P1896','P1899','P3175','P1905','FEX_C']);
w=read('Fuerza',key+['P6240','P6250','P6260','P6270','P6280','P415','P421S2','P421S2A1','P8650','P9000','P9002S1','P9002S2','P9002S3','P9002S4','P9002S5','P9002S9','P6440','P6435','P8624']);
e=read('Educacion',key+['P8586','P6218','P8587']);
s=read('Variables_diseno',key+['MPIO','SEGMENTO','ESTRATO2020','FEX_C']).rename(columns={'FEX_C':'weight'});
y=c[c.P6040.between(18,28)].copy(); print('youth',len(y));
for name,t in [('work',w),('edu',e),('design',s)]:
 y=y.merge(t,on=key,how='left',validate='one_to_one',indicator=True); print(name,y._merge.value_counts().to_dict());y=y.drop(columns='_merge')
print('weights',y.weight.describe(), 'max relative diff', ((y.FEX_C-y.weight)/y.weight).abs().max(), 'sum',y.weight.sum());
for col in ['P6020','P6240','P6250','P6260','P6270','P6280','P8586','P421S2','P8650','P9000','P9002S9','P6440','P6435','P1895','P1896','P3175','P1905','P6087','P415','P421S2A1']:
 print(col, y[col].value_counts(dropna=False).head(18).to_dict())
print('routing',y.groupby('P6240',dropna=False)[['P6250','P6260','P6270','P6280']].agg(lambda x: str(x.value_counts(dropna=False).to_dict())).to_string());


import pandas as pd, numpy as np, zipfile,glob
p=glob.glob(str(ROOT / '*Variables_diseno*.zip'))[0]; z=zipfile.ZipFile(p); s=pd.read_csv(z.open(next(n for n in z.namelist() if n.endswith('.csv'))),sep=';',decimal=',',usecols=['ESTRATO2020','SEGMENTO']);
psu=s.drop_duplicates(); sizes=psu.groupby('ESTRATO2020').size(); print('strata',len(sizes),'psus',len(psu),'singletons',sizes[sizes==1].to_dict());
y['work']=(y.P6240==1)|y[['P6250','P6260','P6270']].eq(1).any(axis=1); y['study']=y.P8586==1
print('occ',y.work.sum(), 'hours populated',y.P415.notna().sum(),'mismatch', (y.work!=y.P415.notna()).sum())
y['grp']=np.select([y.study&y.work,y.study&~y.work,~y.study&y.work,~y.study&~y.work&(y.P6240==4),~y.study&~y.work&(y.P6280==1)],['Estudia y trabaja','Estudia sin ocupación','Ocupado no estudia','Oficios hogar no estudia/ocupación','Busca trabajo (resto)'],default='Otros sin estudio ni ocupación')
y['both8']=(y.P3175>=8)&(y.P1905>=8); y['all8']=y.both8&(y.P1895>=8); y['sense8']=y.P1905>=8;y['time8']=y.P3175>=8;y['life8']=y.P1895>=8;y['sense_time_gap']=(y.P1905>=8)&(y.P3175<=5);y['female']=y.P6020==2
# approximate Taylor with full strata PSU, singleton strata excluded from variance (report)
index=pd.MultiIndex.from_frame(psu[['ESTRATO2020','SEGMENTO']]);
def ratio(mask,x):
 a=y.loc[mask,['ESTRATO2020','SEGMENTO','weight']].copy(); a['x']=y.loc[mask,x] if isinstance(x,str) else x[mask]; a=a.dropna(); den=a.weight.sum(); m=(a.weight*a.x).sum()/den; a['u']=a.weight*(a.x-m)/den; t=a.groupby(['ESTRATO2020','SEGMENTO']).u.sum().reindex(index,fill_value=0); v=t.groupby(level=0).agg(['count','var']); se=np.sqrt((v['count']*v['var']).sum()); return (m,se)
for g,d in y.groupby('grp'):
 mask=y.grp==g; res={k:tuple(round(n,4) for n in ratio(mask,k)) for k in ['P1895','P3175','P1905','all8','sense_time_gap','female','sense8','time8']}; print(g,len(d),round(d.weight.sum()/y.weight.sum()*100,2),res)
print('4group means')
y['grp4']=np.select([y.study&y.work,y.study&~y.work,~y.study&y.work],['studywork','study','work'],default='neither');
for g,d in y.groupby('grp4'):
 print(g,len(d),round(d.weight.sum()/y.weight.sum()*100,2),{k:tuple(round(n,4) for n in ratio(y.grp4==g,k)) for k in ['P1895','P3175','P1905','all8','sense_time_gap']})
print('hours',y.P415.describe(),y.P415.value_counts().sort_index().tail(12));
for name,mask in [('<=30h',y.work&~y.study&y.P415.between(1,30)),('31-48h',y.work&~y.study&y.P415.between(31,48)),('49+h',y.work&~y.study&(y.P415>=49)&(y.P415<=168))]:
 print(name,mask.sum(),{k:tuple(round(n,4) for n in ratio(mask,k)) for k in ['P1895','P3175','P1905','all8','sense_time_gap']})
print('care reasons subset')
for k in ['P9002S1','P9002S2','P9002S3','P9002S4','P9002S5','P9002S9']:
 print(k,y.loc[y.grp=='Oficios hogar no estudia/ocupación',k].value_counts(dropna=False).to_dict())
print('effective Kish',y.weight.sum()**2/(y.weight**2).sum())
