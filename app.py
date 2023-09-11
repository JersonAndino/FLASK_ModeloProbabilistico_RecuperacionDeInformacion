"""_summary_

    :authors: Jerson Andino, Carlos Lopez, Milton Casnanzuela
    :description: A flask application for test the probabilistic method of information recovery.
"""

import os
import time

from flask import Flask, request, render_template
from math import log
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from werkzeug.utils import secure_filename





# Crear la carpeta 'uploaded_files' si no existe
if not os.path.exists('uploaded_files'):
    os.makedirs('uploaded_files')

app = Flask(__name__)

documentos=[]
documentos_limpios=[]
nombres_docs=[]
stop_words=['a','al','con','de','del','el','en','es','están','la','los','las','su','un','una','unos','unas','tiene','va','y','que']
V = []
frecuencias=[]
ni=[]
qi=[]
ci=[]
ci_ciega = []
qi_ciega = []   
pi_ciega = []


def limpiar_doc(documento):
    """
    Args:
        documento (string): Recibe como parametro el texto del documento ingresado por teclado o desde archivo

    Returns:
        doc: retorna una lista que contiene las palabras del documento sin stop_words y separada por espacios.
    """
    # Definimos las stopwords en español
    stop_words = set(stopwords.words('spanish'))
    # Convertimos todo el documento a minúsculas
    documento=documento.lower()
    # Usamos un tokenizador que separa las palabras y los signos de puntuación
    doc = word_tokenize(documento)
    # Creamos una nueva lista de palabras que no son stopwords ni signos de puntuación
    doc = [word for word in doc if word.isalpha() and word not in stop_words]
    print(doc)
    return  doc


def vectorizar(documento,V):
    """
    Args:
        documento (string): documento limpio perteneciente a la consulta
        V (lista): el lexico correspondiente a los documentos cargados al sistema

    Returns:
        q_v: retorna una lista correspondiente al vector de la consulta
    """
    q_v=[]
    for word in V:
        if word in documento:
            q_v.append(1)
        else:
            q_v.append(0)
    return q_v
##############################################
# Funciones de calculo de tablas
def calcular_v(documentos_limpios):
    """Calcula el lexico actual respectoa los documentos cargados de forma iterativa
    
    Args:
        documentos_limpios (lista): una lista de documentos después de haber pasado por el proceso de limpieza
    """
    V.clear()
    if documentos_limpios:
        for d in documentos_limpios:
            for word in d:
                if word not in V:
                    V.append(word)  
    else:
        V.clear()

def calcular_frecuencias(documentos_limpios, V):
    """Calculo de las frecuencias de cada palabra del documento encontradas en el documento respecto al lexico,
    actualiza la lista de frecuencias

    Args:
        documentos_limpios (lista): una lista de documentos después de haber pasado por el proceso de limpieza
        V (_type_): el lexico correspondiente a los documentos cargados al sistema
    """
    frecuencias.clear()
    for d in documentos_limpios:
        d_temp=d
        d_v_temp=[]
        for word in V:
            cont=0
            for i in range(len(d_temp)):
                if d_temp[i]==word:
                    cont+=1
            d_v_temp.append(cont)
        frecuencias.append(d_v_temp)

def calcular_ni(frecuencias,V):
    """Calculo de el valor ni para la tabla de frecuencias

    Args:
        frecuencias (lista): Lista de frecuencias de palabras en documentos
        V (_type_): Lexico de los documentos cargados
    """
    ni.clear()
    for i in range(len(V)):
        cont=0
        for d in frecuencias:
            if d[i]>0:
                cont+=1
        ni.append(cont)
        

def calcular_qi(ni):
    """Calculo del elemento qi en la tabla de similitud

    Args:
        ni (lista): Lista que contiene la frecuencia de cada palabra en los documentos
    """
    qi.clear()
    N=len(documentos)
    for n in ni:
        qi.append(n/N)
        
def calcular_ci(ni):
    """Calculo del valor ci, el peso de relevancia de cada palabra de los documentos

    Args:
        ni (lista): Lista que contiene la frecuencia de cada palabra en los documentos
    """
    ci.clear()
    N=len(documentos)    
    for n in ni:
        ci.append(log((N-n)/n,10))
    
def calcular_tabla():
    """Union de todas las tablas pertinentes calculadas para armar la tabla de similitud

    Args:
        

    Returns:
        tabla_pesos: una lista compuesta de distintos valores, cada fila contiene los valores pertinentes a todas las tablas
    """
    tabla_pesos=[]
    try:
        if len(documentos)>1:
            calcular_v(documentos_limpios)
            calcular_frecuencias(documentos_limpios,V)
            calcular_ni(frecuencias,V)
            calcular_qi(ni)
            calcular_ci(ni)
            for i,v in enumerate(V):
                d_temp=[]
                d_temp.append(v)
                d_temp.append('t'+str(i+1))
                d_temp.append(ni[i])
                d_temp.append(qi[i])
                d_temp.append(ci[i])
                tabla_pesos.append(d_temp)
        else:
            pass
    except Exception as e:
        print(e)
        pass
    return tabla_pesos
###################################################3
def ordenar_sim(sim):
    """Realizar el ordenamiento de los documentos segun su similitud

    Args:
        sim (lista): Una lista que contiene los valores resultantes de similitud de cada documento

    Returns:
        nuevo_orden: Una lista que contiene el orden de los documentos segun su relevancia
    """
    orden=list(range(len(sim)))
    nuevo_orden=[]
    for i in range(len(sim)):
        max=sim[0]
        maxi=0
        for j in range(len(sim)):
            if sim[j]>max:
                max=sim[j]
                maxi=j
        sim.pop(maxi)
        nuevo_orden.append(orden[maxi])
        orden.pop(maxi)
        
    tabla_orden=[]
    for p in nuevo_orden:
        tabla_orden.append(['d'+str(p+1),nombres_docs[p]])
    
    return tabla_orden

def consultar_q(frecuencias, ci, q):
    """Realiza el calculo de la tabla de similitud

    Args:
        frecuencias (lista): lista de frecuencias de las palabras de cada documento
        ci (lista): lista de pesos de relevancia de cada palabra en el lexico
        q (lista): vector de la consulta realizada

    Returns:
        sim: lista de similitud obtenida
        orden: nuevo orden calculado para la relevancia de documentos
    """
    producto_interno=[]
    n=len(V)
    for d in frecuencias:
        d_temp=[]
        for i in range(n):
            d_temp.append(q[i]*d[i])
        producto_interno.append(d_temp)
    producto_interno_pesos=[]    
    for d in producto_interno:
        d_temp=[]
        print(d)
        print(ci)
        for i in range(n):
            d_temp.append(d[i]*ci[i])
        producto_interno_pesos.append(d_temp)  
    sim=[]  
    for d in producto_interno_pesos:
        sim.append(abs(sum(d)))
    sim_copy=sim.copy()    
    return (sim, ordenar_sim(sim_copy))      

def calcular_pi_ciega(ni, num_total_docs, num_docs_rel):
    pi_ciega.clear()
    for n in ni:
        pi_ciega.append(
            ( num_docs_rel / num_total_docs)
        )
    return pi_ciega
def calcular_qi_ciega(ni, num_total_docs, num_docs_rel):
    ni_ciega.clear()
    for n in ni:
        ni_ciega.append(
            (n / num_total_docs)
        )
    return ni_ciega
def calcular_ci_ciega(ni, num_total_docs, num_docs_rel):
     for n in ni:
        ci_ciega.append(
            log(((num_docs_rel + 0.5) / (num_total_docs - num_docs_rel + 0.5))/((ni - num_docs_rel + 0.5)/(num_total_docs - ni + 0.5 )), 10)
        )

def calcular_tabla_ciega(num_total_docs, num_docs_rel):
    """Union de todas las tablas pertinentes calculadas para armar la tabla de similitud

    Args:
        

    Returns:
        tabla_pesos: una lista compuesta de distintos valores, cada fila contiene los valores pertinentes a todas las tablas
    """
    tabla_pesos=[]
    try:
        if len(documentos)>1:
            calcular_v(documentos_limpios)
            calcular_frecuencias(documentos_limpios,V)
            calcular_pi_ciega(ni, num_total_docs, num_docs_rel)
            calcular_qi_ciega(ni, num_total_docs, num_docs_rel)
            calcular_ci_ciega(ni, num_total_docs, num_docs_rel)
            for i,v in enumerate(V):
                d_temp=[]
                d_temp.append(v)
                d_temp.append('t'+str(i+1))
                d_temp.append(ni[i])
                d_temp.append(pi_ciega[i])
                d_temp.append(qi_ciega[i])
                d_temp.append(ci_ciega[i])
                tabla_pesos.append(d_temp)
        else:
            pass
    except Exception as e:
        print(e)
        pass
    return tabla_pesos
    
@app.route('/', methods=['GET', 'POST'])
def home():
    content = dict()
    if request.method == 'POST':
        if request.form['tipo_post']=='3':
            if not ci:
                content['not_ready']=True
            else:
                consulta=request.form['consulta']
                q=vectorizar(limpiar_doc(consulta),V)
                inicio = time.time_ns()
                (sim, orden_docs) = consultar_q(frecuencias,ci,q)
                fin = time.time_ns()
                content['sim']=sim
                content['orden_docs']=orden_docs    
                content['consulta'] = consulta   
                content['tiempo'] = (fin-inicio)/10**(9)        
            
    calcular_v(documentos_limpios)
    calcular_frecuencias(documentos_limpios,V)
    calcular_ni(frecuencias,V)
    tabla_pesos = calcular_tabla()
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    content['frecuencias']=frecuencias
    content['ni']=ni
    content['tabla_pesos']=tabla_pesos
            
    return render_template('inicio.html',**content)

@app.route('/cargar_documento', methods=['GET', 'POST'])
def cargar_documento():
    content=dict()
    if request.method == 'POST':
        # print(request.form)
        if request.form['tipo_post']=='0':
            if request.files['documento']:
                f = request.files['documento']
                filename = secure_filename(f.filename)
                file_path=os.path.join('uploaded_files', filename)
                f.save(file_path)
                file=open(file_path,encoding="utf-8")
                doc = file.read()
                file.close()
                documentos.append(doc)
                documentos_limpios.append(limpiar_doc(doc))
                nombres_docs.append(filename)
            else:
                if request.form['texto']:
                    documentos.append(request.form['texto'])
                    documentos_limpios.append(limpiar_doc(request.form['texto']))
                    nombres_docs.append(request.form['texto'])
        if request.form['tipo_post']=='1':
            index_doc = int(request.form['doc_index'])
            documentos.pop(index_doc-1)
            documentos_limpios.pop(index_doc-1)
            nombres_docs.pop(index_doc-1)
            
        if request.form['tipo_post']=='2':
            documentos.clear()
            documentos_limpios.clear()
            nombres_docs.clear()
            ci.clear()
            V.clear()
            ni.clear()
            qi.clear()
    
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    
    return render_template('cargar_documento.html', **content)

@app.route('/retroalimentacion', methods=['GET', 'POST'])
def retroalimentacion():
    content=dict()
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    content['frecuencias']=frecuencias
    content['ni']=ni
    option = ['SELECCIONAR OPCION', 'ES RELEVANTE', 'NO ES RELEVANTE']
    
    if request.method == 'POST':
            docs_recuperados= request.form.getlist('relevancia')
            num_total_docs = len(docs_recuperados)
            num_docs_relevantes = len([doc for doc in docs_recuperados if doc == 'ES RELEVANTE'])
            if not ci:
                content['not_ready']=True
            else:
                tabla_pesos_ciega = calcular_tabla_ciega(num_total_docs, num_docs_relevantes)
                content['tabla_pesos_ciega']=tabla_pesos_ciega
            


    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    return render_template('retroalimentacion.html', option=option, **content)


@app.route('/calcular', methods=['GET'])
def calcular():
    content = dict()
    tabla_pesos = calcular_tabla()
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    content['frecuencias']=frecuencias
    content['ni']=ni
    content['tabla_pesos']=tabla_pesos
    return render_template('calcular.html', **content)

if __name__ == '__main__':
    app.run(debug=True)
