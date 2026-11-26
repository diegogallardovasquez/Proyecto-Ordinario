"""Menú web local del proyecto ordinario. Ejecuta python3 app_web.py."""
from contextlib import redirect_stdout
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from threading import Lock
from pathlib import Path
from runpy import run_path
from urllib.parse import parse_qs, urlsplit
import sys
import webbrowser

if __name__ == "__main__":
    sys.dont_write_bytecode = True

import proyecto2 as tienda
from proyecto3 import Navegador
from proyecto4 import ColaImpresion
from proyecto5 import Arbol
from proyecto6 import cargar_grafo

RAIZ = Path(__file__).resolve().parent
PROYECTOS = {
    'resistencias': ('Resistencias', 'Arreglos', 'Identifica bandas y calcula resistencias equivalentes.'),
    'carrito': ('Carrito de compras', 'Listas', 'Consulta el catálogo y administra tu compra.'),
    'historial': ('Historial web', 'Pilas', 'Simula visitas y recorre el historial en ambos sentidos.'),
    'impresion': ('Cola de impresión', 'Colas', 'Atiende los documentos en orden de llegada.'),
    'archivos': ('Sistema de archivos', 'Árboles', 'Organiza y busca archivos en un árbol binario.'),
    'rutas': ('Ruta Mágica', 'Grafos', 'Encuentra el camino más corto entre siete pueblos de Puebla.')
}
from vista_web import CSS, MOTIVOS, panel_arbol, panel_cola, panel_historial

def h(valor):
    return escape(str(valor), quote=True)

def campo(nombre, titulo, valor='', tipo='text'):
    return f'<label>{h(titulo)}<input name="{nombre}" type="{tipo}" value="{h(valor)}"></label>'

def lista(nombre, titulo, opciones, seleccionado=None):
    contenido = ''.join(f'<option value="{h(k)}" {"selected" if k == seleccionado else ""}>{h(v)}</option>' for k,v in opciones)
    return f'<label>{h(titulo)}<select name="{nombre}">{contenido}</select></label>'

def formulario(campos, acciones):
    botones = ''.join(f'<button name="accion" value="{h(k)}">{h(v)}</button>' for k,v in acciones)
    return f'<form method="post">{campos}{botones}</form>'

def tabla(cabeceras, filas):
    head = ''.join(f'<th>{h(c)}</th>' for c in cabeceras)
    body = ''.join('<tr>'+''.join(f'<td>{h(c)}</td>' for c in fila)+'</tr>' for fila in filas)
    return f'<section><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></section>'

def salida(accion, *args):
    texto = StringIO()
    with redirect_stdout(texto):
        accion(*args)
    return texto.getvalue().strip()

class Laboratorio:
    """Una sesión de demostración compartida por las pestañas de este equipo."""
    def __init__(self):
        modulo = run_path(str(RAIZ/'proyecto1.py'), init_globals={'input':lambda _: '4', 'print':lambda *args: None})
        self.calc = modulo['CalculadoraResistencia']()
        self.valor_ohmios = "4.7"
        self.producto_seleccionado = tienda.catalogo[0].id
        self.cantidad_carrito = 1
        self.cantidad_resistencias = 3
        self.nav = Navegador()
        self.cola = ColaImpresion()
        self.arbol = Arbol()
        self.grafo = cargar_grafo()
        self.resultados = {}
        self.ultima_ruta = None
        self.extremos = ('ZAC', 'TLA')
        self.lock = Lock()

    def controles(self, pagina):
        if pagina == 'resistencias':
            return formulario(campo('valor','Valor en ohmios',self.valor_ohmios), [('bandas','Ver bandas')])+formulario(campo('cantidad','Número de resistencias',self.cantidad_resistencias,'number'), [('serie','Generar en serie'),('paralelo','Generar en paralelo')])
        if pagina == 'carrito':
            catalogo = tabla(['ID','Producto','Precio'],[(p.id,p.nombre,f'${p.precio}') for p in tienda.catalogo])
            opciones = [(p.id,p.nombre) for p in tienda.catalogo]
            form = formulario(lista('id','Producto',opciones,self.producto_seleccionado)+campo('cantidad','Cantidad',self.cantidad_carrito,'number'), [('agregar','Agregar'),('modificar','Actualizar cantidad'),('quitar','Quitar producto')])
            filas = [(i.producto.nombre,i.cantidad,f'${i.calcular_subtotal()}') for i in tienda.carrito]
            return catalogo+form+tabla(['Carrito','Cantidad','Subtotal'],filas)+f'<p>Total del carrito <b>${sum(i.calcular_subtotal() for i in tienda.carrito)}</b></p>'+formulario('',[('finalizar','Finalizar compra'),('vaciar','Vaciar carrito')])
        if pagina == 'historial':
            return formulario(campo('url','Dirección web','https://ejemplo.com'), [('visitar','Visitar'),('atras','Atrás'),('adelante','Adelante')])+panel_historial(self.nav)
        if pagina == 'impresion':
            return formulario('', [('agregar','Agregar trabajo'),('imprimir','Imprimir primero')])+panel_cola(self.cola)
        if pagina == 'archivos':
            campos = campo('nombre','Nombre')+campo('extension','Extensión')+campo('tamano','Bytes',0,'number')
            return formulario(campos,[('directorio','Crear directorio'),('archivo','Insertar archivo'),('buscar','Consultar'),('eliminar','Eliminar')])+formulario('', [(x,x.capitalize()) for x in ('inorden','preorden','postorden')])+panel_arbol(self.arbol)
        pueblos = [(p.clave,p.nombre) for p in self.grafo.pueblos]
        return formulario(lista('origen','Origen',pueblos,self.extremos[0])+lista('destino','Destino',pueblos,self.extremos[1]), [('calcular','Calcular ruta')])

    def operar(self, pagina, d):
        op = d['accion']
        if pagina == 'resistencias':
            if op == 'bandas':
                self.valor_ohmios = d['valor'].strip()
                bandas = self.calc.obtener_colores(float(self.valor_ohmios.replace(',','.')))
                return ' · '.join(bandas) if bandas is not None else 'Valor no representable con tres bandas.'
            n = int(d['cantidad'])
            if not 1 <= n <= 100000:
                return 'Elige entre 1 y 100 000 resistencias.'
            self.cantidad_resistencias = n
            valores,total = {'serie':self.calc.resistencia_serie,'paralelo':self.calc.resistencia_paralelo}[op](n)
            return f'Resistencias (Ω)   {valores}\nEquivalente   {total:,.4f} Ω'
        if pagina == 'carrito':
            acciones = {'finalizar':tienda.finalizar_compra,'vaciar':tienda.vaciar_carrito,'agregar':tienda.agregar_producto_al_carrito,'modificar':tienda.modificar_cantidad,'quitar':tienda.eliminar_producto}
            datos = []
            if op in ('agregar', 'modificar', 'quitar'):
                producto = tienda.buscar_en_catalogo_por_id(int(d['id']))
                if producto is None:
                    return 'Elige un producto del catálogo.'
                self.producto_seleccionado = producto.id
                self.cantidad_carrito = d.get('cantidad', self.cantidad_carrito)
            if op in ('agregar','modificar'):
                cantidad = int(d['cantidad'])
                if cantidad < 1:
                    return 'Elige una cantidad mayor que cero.'
                datos = [d['id'], str(cantidad)]
            elif op == 'quitar':
                datos = ['1',d['id'],'s']
            elif op == 'vaciar':
                datos = ['s']
            respuestas = iter(datos)
            tienda.input = lambda _: next(respuestas)
            try:
                return salida(acciones[op])
            finally:
                del tienda.input
        if pagina == 'historial':
            if op == 'visitar':
                return salida(self.nav.visitar,d['url'])
            return salida({'atras':self.nav.retroceder,'adelante':self.nav.avanzar}[op])
        if pagina == 'impresion':
            return salida({'agregar':self.cola.agregar_trabajo,'imprimir':self.cola.imprimir_documento}[op])
        if pagina == 'archivos':
            if op in ('inorden','preorden','postorden'):
                return salida(getattr(self.arbol,op),self.arbol.raiz)
            if op == 'buscar':
                nodo = self.arbol.buscar(d['nombre'])
                return salida(nodo.mostrar_informacion) if nodo else 'Elemento no encontrado.'
            if op == 'eliminar':
                return salida(self.arbol.eliminar,d['nombre'])
            if op == 'directorio':
                return salida(self.arbol.insertar,d['nombre'],'',0,'Directorio')
            return salida(self.arbol.insertar,d['nombre'],d['extension'],int(d['tamano']),'Archivo')
        self.ultima_ruta = None
        self.extremos = (d['origen'],d['destino'])
        if d['origen'] == d['destino']:
            return 'Selecciona dos pueblos distintos.'
        ruta,km = self.grafo.dijkstra(d['origen'],d['destino'])
        nombres = [self.grafo.buscar_pueblo(k).nombre for k in ruta]
        if ruta:
            self.ultima_ruta = (km,nombres,[(nombres[i], nombres[i+1], self.grafo.distancia(ruta[i], ruta[i+1])) for i in range(len(ruta)-1)])
        return f'{km} km\n'+' → '.join(nombres) if ruta else 'Sin conexión entre estos pueblos.'

    def pagina(self, ruta):
        if not ruta:
            tarjetas = ''.join(f'<a class="card {k}" href="/{k}"><span class="motif" aria-hidden="true">{MOTIVOS[k]}</span><b aria-hidden="true">↗</b><small>{h(tipo)}</small><h2>{h(titulo)}</h2><p>{h(desc)}</p></a>' for k,(titulo,tipo,desc) in PROYECTOS.items())
            cuerpo = '<div class="hero"><small>Universidad Anáhuac Mayab</small><h1>Laboratorio de estructuras</h1><p>Diego Gallardo · Emilio Jiménez · Doram Basdemir · Alan López</p></div><div class="grid">'+tarjetas+'</div>'
        else:
            titulo,tipo,descripcion = PROYECTOS[ruta]
            cuerpo = f'<small>{h(tipo)}</small><h1>{h(titulo)}</h1><p>{h(descripcion)}</p>'+self.controles(ruta)
            if ruta in self.resultados:
                resultado = self.resultados[ruta]
                if ruta == 'rutas' and self.ultima_ruta:
                    km, nombres, tramos = self.ultima_ruta
                    paradas = ''.join(f'<li>{h(nombre)}</li>' for nombre in nombres)
                    cuerpo += f'<section class="metric"><small>Distancia mínima</small><strong>{km} km</strong><ol class="steps">{paradas}</ol></section>'
                    cuerpo += tabla(["Desde", "Hasta", "Distancia"], [(a,b,f"{distancia} km") for a,b,distancia in tramos])
                elif ruta == 'resistencias' and ' · ' in resultado:
                    paleta = dict(zip(self.calc.colores, ('#202020','#79472f','#c43d35','#e48332','#f3ce44','#328553','#446da4','#855fa8','#899393','#fff','#ad914d','#b9c3bf')))
                    bandas = ''.join(f'<span class="chip"><i style="background:{paleta[c]}"></i>{h(c)}</span>' for c in resultado.split(' · '))
                    cuerpo += '<section><small>Bandas de izquierda a derecha</small><div>'+bandas+'</div></section>'
                else:
                    cuerpo += '<section aria-live="polite"><small>Resultado</small><pre>'+h(resultado)+'</pre></section>'
            cuerpo = '<div class="work">'+cuerpo+'</div>'
        regreso = '<a class="slide-link" href="/">← Volver al menú principal</a>' if ruta else ''
        return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<title>Laboratorio de estructuras</title><style>{CSS}</style></head><body><header><div class="bar">'
                '<span class="brand"><i aria-hidden="true">{ }</i> Proyecto ordinario</span>'+regreso+
                '</div></header><main>'+cuerpo+'</main></body></html>')


class Solicitud(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlsplit(self.path)
        pagina = url.path.strip('/')
        if pagina and pagina not in PROYECTOS:
            self.send_error(404)
            return
        with self.server.lab.lock:
            contenido = self.server.lab.pagina(pagina).encode()
        self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8')
        self.send_header('Content-Length',str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

    def do_POST(self):
        pagina = self.path.strip('/')
        if pagina not in PROYECTOS:
            self.send_error(404)
            return
        origen = self.headers.get('Origin')
        if origen and origen != 'http://'+self.headers.get('Host',''):
            self.send_error(403)
            return
        try:
            n = int(self.headers.get('Content-Length','0'))
            if not 0 <= n <= 16384:
                self.send_error(413)
                return
            datos = parse_qs(self.rfile.read(n).decode(),keep_blank_values=True)
            with self.server.lab.lock:
                self.server.lab.resultados[pagina] = self.server.lab.operar(pagina,{k:v[0] for k,v in datos.items()})
        except (ValueError,KeyError,StopIteration):
            with self.server.lab.lock:
                self.server.lab.resultados[pagina] = 'Revisa los datos ingresados e intenta de nuevo.'
        self.send_response(303)
        self.send_header('Location','/'+pagina)
        self.end_headers()

if __name__ == '__main__':
    try:
        servidor = ThreadingHTTPServer(('127.0.0.1',8501),Solicitud)
    except OSError:
        servidor = ThreadingHTTPServer(('127.0.0.1',0),Solicitud)
    servidor.lab = Laboratorio()
    direccion = f'http://127.0.0.1:{servidor.server_port}'
    print(f'Abre en Google Chrome: {direccion}\nPara cerrar, presiona Ctrl+C.',flush=True)
    try:
        webbrowser.get('google-chrome').open(direccion)
    except webbrowser.Error:
        webbrowser.open(direccion)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()
