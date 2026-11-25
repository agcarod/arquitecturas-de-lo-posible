"""Casos sintéticos: prueba de reglas, no validación empírica. Sin datos personales."""
# Estados de requisitos: C compatible, R restricción documentada, U indeterminado.
from itertools import product

def access(requirements):
    if not requirements: return 'indeterminada'
    if 'R' in requirements: return 'restringida'
    if 'U' in requirements: return 'indeterminada'
    return 'plausible'

def compatible(a,b,available,shared=0):
    # Horas de actividades mutuamente excluyentes; shared sólo si la simultaneidad se documenta.
    if available is None or a is None or b is None: return 'indeterminada'
    if not 0<=shared<=min(a,b): raise ValueError('simultaneidad inválida')
    return 'restringida' if a+b-shared>available else 'plausible'

def ampliabilidad(equity,cost,rights):
    # No certifica escalabilidad: sólo identifica si se puede estudiar como candidata.
    if 'R' in [equity,cost,rights]: return 'requiere rediseño'
    if 'U' in [equity,cost,rights]: return 'indeterminada'
    return 'candidata a estudio'

cases=[('A','optimismo con barrera económica',lambda:access(['C','R','U']),'restringida'),('B','pesimismo con requisitos documentados compatibles',lambda:access(['C','C','C']),'plausible'),('C','información incompleta',lambda:access(['C','U']),'indeterminada'),('D','dos opciones posibles por separado; juntas exceden tiempo',lambda:compatible(18,16,25),'restringida'),('E','simultaneidad documentada',lambda:compatible(18,16,30,4),'plausible'),('F','apoyo retirado en seguimiento',lambda:(access(['C','C']),access(['C','R'])),('plausible','restringida')),('G','traslado de carga injusto',lambda:ampliabilidad('R','C','C'),'requiere rediseño'),('H','sin datos de costos ni derechos',lambda:ampliabilidad('C','U','U'),'indeterminada'),('I','sin ventaja sobre comparador fuerte: ambos identifican misma barrera',lambda:access(['R']),'restringida'),('J','no se han identificado requisitos',lambda:access([]),'indeterminada')]
for id,desc,run,expected in cases:
    actual=run(); assert actual==expected,(id,actual,expected)
    print(f'{id}: {desc} | {actual} | OK')
for states in product('CRU',repeat=3):
    assert (access(states)=='plausible')==all(s=='C' for s in states)
print('10/10 casos y 27 combinaciones lógicas superadas. No prueban validez, novedad ni confiabilidad entre evaluadores.')
