import pandas as pd, numpy as np, zipfile, sys
from pathlib import Path
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
key=['DIRECTORIO','SECUENCIA_P','ORDEN']; hk=key[:2]
def read(pattern,cols):
 p=next(ROOT.glob(pattern)); z=zipfile.ZipFile(p); f=next(n for n in z.namelist() if n.lower().endswith('.csv')); d=pd.read_csv(z.open(f),sep=';',decimal=',',encoding='latin1',usecols=cols); print(p.name,d.shape,flush=True); return d
c=read('*Caracteristicas*.zip',key+['P6040','P6020','P1895','P3175','P1905']); w=read('*Fuerza*.zip',key+['P6240','P6250','P6260','P6270','P6280','P415']); e=read('*Educacion*.zip',key+['P8586']); s=read('*Variables_diseno*.zip',key+['SEGMENTO','ESTRATO2020','FEX_C']); h=read('DBF-ECV-Condiciones_vida_hogar_tenencia_bienes-2025.zip',['DIRECTORIO','SECUENCIA_ENCUESTA','SECUENCIA_P','ORDEN','P9090','P1075','P1913S11']);
# Household table encodes household number in ORDEN and SECUENCIA_ENCUESTA.
assert h.ORDEN.eq(h.SECUENCIA_ENCUESTA).all(); assert h.SECUENCIA_P.eq(1).all(); h=h.drop(columns=['SECUENCIA_P','SECUENCIA_ENCUESTA']).rename(columns={'ORDEN':'SECUENCIA_P'}); assert set(map(tuple,h[hk].to_numpy()))==set(map(tuple,c[hk].drop_duplicates().to_numpy()));
assert not h.duplicated(hk).any(); print('H economic',h.P9090.value_counts(dropna=False).to_dict()); y=c[c.P6040.between(18,28)].copy()
for t in [w,e,s,h]:
 k=key if 'ORDEN' in t else hk; y=y.merge(t,on=k,how='left',validate='one_to_one' if k==key else 'many_to_one',indicator=True); print('merge',y._merge.value_counts().to_dict(),flush=True); assert y._merge.eq('both').all(); y=y.drop(columns='_merge')
assert y.P9090.isin([1,2,3]).all(); assert y.FEX_C.gt(0).all(); print('coverage',y[['P8586','P6240','P1895','P3175','P1905','P9090']].isna().sum().to_dict()); print('households',y[hk].drop_duplicates().shape[0]);
y['work']=(y.P6240==1)|y[['P6250','P6260','P6270']].eq(1).any(axis=1); y['study']=y.P8586==1
names=['studywork','study','work','home','search','other']; y['grp']=np.select([y.study&y.work,y.study&~y.work,~y.study&y.work,~y.study&~y.work&(y.P6240==4),~y.study&~y.work&(y.P6280==1)],names[:-1],default=names[-1]);
assert y[['P1895','P3175','P1905']].apply(lambda x:x.between(0,10)).all(axis=1).all()
for k in [7,8,9]: y[f'all{k}']=y[['P1895','P3175','P1905']].ge(k).all(axis=1)
y['joint']=y.all8 & y.P9090.ge(2); y['enough']=y.P9090.ge(2); y['female']=y.P6020.eq(2)
psu=s[['ESTRATO2020','SEGMENTO']].drop_duplicates(); idx=pd.MultiIndex.from_frame(psu); print('singleton',psu.groupby('ESTRATO2020').size().eq(1).sum());
def estimate(mask,col):
 a=y.loc[mask,['ESTRATO2020','SEGMENTO','FEX_C',col]].dropna().copy(); den=a.FEX_C.sum(); m=(a.FEX_C*a[col]).sum()/den; a['u']=a.FEX_C*(a[col]-m)/den; u=a.groupby(['ESTRATO2020','SEGMENTO']).u.sum().reindex(idx,fill_value=0); return m,u,len(a)
def se(u):
 v=u.groupby(level=0).agg(['count','var']); return np.sqrt((v['count']*v['var']).sum())
def fmt(a):
 m,u,n=a; z=se(u); return [n,round(m*100,2),round((m-1.96*z)*100,2),round((m+1.96*z)*100,2)]
def diff(a,b):
 d=a[0]-b[0]; z=se(a[1]-b[1]); return [round(x*100,2) for x in [d,d-1.96*z,d+1.96*z]]
print('total',len(y),y.FEX_C.sum());
for g in names:
 mask=y.grp.eq(g); print('group',g, 'n',mask.sum(),'enough',fmt(estimate(mask,'enough')),'joint',fmt(estimate(mask,'joint')),'all8',fmt(estimate(mask,'all8')))
 for p in [1,2,3]: print('economic',g,p,fmt(estimate(mask&y.P9090.eq(p),'all8')))
for p in [1,2,3]:
 for female in [False,True]:
  for g in ['work','home']: print('sex',g,p,female,fmt(estimate(y.grp.eq(g)&y.P9090.eq(p)&y.female.eq(female),'all8')))
for p in [1,2,3]: print('home-work',p,diff(estimate(y.grp.eq('home')&y.P9090.eq(p),'all8'),estimate(y.grp.eq('work')&y.P9090.eq(p),'all8')))
for g in ['work','home','study','studywork']:
 mask=y.grp.eq(g); print('economic gap',g,diff(estimate(mask&y.P9090.ge(2),'all8'),estimate(mask&y.P9090.eq(1),'all8')))
for k in ['all7','all9']:
 for g in ['work','home']: print('sensitivity',k,g,fmt(estimate(y.grp.eq(g),k)),fmt(estimate(y.grp.eq(g)&y.P9090.eq(1),k)),fmt(estimate(y.grp.eq(g)&y.P9090.ge(2),k)))
print('internet',y.P1075.value_counts(dropna=False).to_dict(),'cultural time',y.P1913S11.value_counts(dropna=False).head(15).to_dict())
print('overall',fmt(estimate(y.P9090.eq(1),'all8')),fmt(estimate(y.P9090.ge(2),'all8')))
print('joint home vs work',diff(estimate(y.grp.eq('home'),'joint'),estimate(y.grp.eq('work'),'joint')))
