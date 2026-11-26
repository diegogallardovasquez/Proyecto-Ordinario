"""Componentes visuales de la aplicación local."""
from html import escape

# Cada motivo ilustra la estructura que se usa en esa práctica.
MOTIVOS = {
    'resistencias': '─▰─',
    'carrito': '[ a, b ]',
    'historial': '↶   ↷',
    'impresion': '▥ ▥ ▥ →',
    'archivos': '┌─┴─┐',
    'rutas': '●─⋯─●',
}

CSS = """
:root{--ink:#17263c;--muted:#526478;--blue:#244aaa;--line:#d8dfe7;--paper:#f8f9fb;--deep:#152e5a}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 Inter,"Helvetica Neue",Arial,sans-serif}
a{color:inherit}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible{outline:3px solid #df8434;outline-offset:3px}
header{border-bottom:1px solid var(--line);background:white}.bar,main{max-width:1180px;margin:auto;padding-inline:clamp(18px,4vw,52px)}
.bar{min-height:64px;display:flex;align-items:center;justify-content:space-between;gap:16px}.brand,.slide-link{display:inline-flex;align-items:center;gap:10px;text-decoration:none;font-weight:700}
.brand i{font:700 17px monospace;color:white;background:var(--deep);padding:6px 9px;border-radius:8px}.slide-link{font-size:14px;color:var(--blue)}
main{padding-block:30px 55px}.hero{position:relative;isolation:isolate;overflow:hidden;background:#162f5b;color:white;border-radius:16px;padding:clamp(25px,4vw,48px)}
.hero::after{content:"";position:absolute;inset:0 0 0 57%;z-index:-1;background-image:radial-gradient(#7393c7 1px,transparent 1.4px);background-size:16px 16px;opacity:.55}
.hero h1{max-width:17ch}.hero p{color:#dbe6fa}.hero small{color:#c2d5fb}
h1{font:600 clamp(35px,5vw,60px)/1.05 Georgia,serif;letter-spacing:-.038em;margin:9px 0 14px}h2{font-size:21px;line-height:1.2;margin:7px 0 9px}p{margin:6px 0 14px;color:var(--muted)}small{color:var(--blue);font-weight:700;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin-top:22px}.card{background:white;border:1px solid var(--line);border-radius:13px;padding:20px;text-decoration:none;display:flex;flex-direction:column;align-items:start;position:relative}
.card:hover{border-color:var(--blue);box-shadow:0 4px 15px #19355812}.card p{font-size:15px;margin:0}.card b{position:absolute;top:18px;right:19px;color:var(--muted);font-size:20px}
.motif{display:inline-grid;place-items:center;background:#e4efff;color:#244aaa;border-radius:8px;height:42px;min-width:64px;padding:0 9px;font:700 17px monospace;margin-bottom:14px}
.carrito .motif,.archivos .motif{background:#f7e7d4;color:#895322}.historial .motif,.rutas .motif{background:#dcefe9;color:#206054}


.work{min-width:0}.work>h1{font-size:clamp(34px,4vw,48px)}.work>p{max-width:65ch}
section,form,.metric{background:white;border:1px solid var(--line);border-radius:11px;padding:18px;margin:14px 0;overflow:auto}
form{display:flex;align-items:end;flex-wrap:wrap;gap:10px}label{display:grid;gap:5px;max-width:100%;font-size:13px;font-weight:700;color:var(--muted)}
input,select,button,.go{font:inherit;border-radius:6px;max-width:100%;padding:9px 12px}input,select{border:1px solid #aab8c8;background:white;color:var(--ink)}
button,.go{cursor:pointer;background:#eef2fa;color:var(--blue);font-size:14px;font-weight:650;border:1px solid #d7dfef;text-decoration:none}
button:first-of-type,.go{background:var(--blue);color:white;border-color:var(--blue)}button:hover,.go:hover{filter:brightness(.94)}
pre{font:15px/1.6 ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere;margin:6px 0}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:9px;border-bottom:1px solid #e4e9ef}th{font-size:13px;color:var(--muted)}tr:last-child td{border:0}
.metric{font-size:18px}.metric strong{display:block;font-size:32px;color:var(--deep)}.steps,.queue{display:flex;gap:8px;flex-wrap:wrap;align-items:center;padding:0;list-style:none}.steps li,.queue li{background:#e3edf8;padding:7px 12px;border-radius:6px;font-weight:650}.steps li+li:before{content:"→ ";color:var(--blue)}.queue .vacante{background:#f1f3f6;color:var(--muted);font-weight:400}
.stack{display:grid;grid-template-columns:1fr 1fr;gap:12px}.stack section{margin:0}.stack ol{padding-left:23px;overflow-wrap:anywhere}
.chip{display:inline-flex;align-items:center;gap:8px;margin:10px 18px 0 0}.chip i{width:17px;height:24px;border:1px solid #777;border-radius:4px}
.tree{list-style:none;padding:0}.tree li{padding:5px 0;border-bottom:1px solid #edf0f4}.tree span{color:var(--muted);font-size:13px}
article{font-size:clamp(17px,2vw,23px);max-width:70ch;margin-block:22px}article p{color:var(--ink)}nav.pager{display:flex;align-items:center;gap:12px}
@media(max-width:800px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:530px){.grid,.stack{grid-template-columns:1fr}.bar{min-height:56px}.hero{border-radius:10px}main{padding-top:18px}.card{padding:16px}.motif{margin-bottom:7px}.slide-link{font-size:13px}}
"""

def panel_historial(navegador):
    def pila(nombre, pila):
        nodo = pila.tope
        filas = []
        while nodo:
            filas.append('<li>'+escape(nodo.pagina)+'</li>')
            nodo = nodo.siguiente
        contenido = '<ol>'+''.join(filas)+'</ol>' if filas else '<p>Vacía</p>'
        return f'<section><h2>{nombre}</h2>{contenido}</section>'
    actual = escape(navegador.pagina_actual or 'Sin páginas visitadas')
    return (f'<section><small>Página actual</small><h2>{actual}</h2></section><div class="stack">'
            +pila('Atrás', navegador.pila_atras)+pila('Adelante', navegador.pila_adelante)+'</div>')

def panel_cola(cola):
    puestos = [f'<li>{i+1} · {escape(pc)}</li>' for i,pc in enumerate(cola.trabajos)]
    puestos.extend('<li class="vacante">Libre</li>' for _ in range(cola.capacidad-len(puestos)))
    return f'<section><small>Orden de impresión</small><h2>{len(cola.trabajos)} de {cola.capacidad} puestos ocupados</h2><ol class="queue">{"".join(puestos)}</ol></section>'

def panel_arbol(arbol):
    filas = []
    pendientes = [(arbol.raiz,0,'Raíz')]
    while pendientes:
        nodo,nivel,lado = pendientes.pop()
        if nodo is None:
            continue
        texto = escape(nodo.nombre)+(('.'+escape(nodo.extension)) if nodo.extension else '')
        filas.append(f'<li style="padding-left:{min(nivel,15)*15}px"><span>{lado}</span> · {texto} <span>({escape(nodo.tipo)})</span></li>')
        pendientes.extend([(nodo.derecho,nivel+1,'Derecha'),(nodo.izquierdo,nivel+1,'Izquierda')])
    return '<section><small>Estructura actual</small><ul class="tree">'+''.join(filas)+'</ul></section>'
