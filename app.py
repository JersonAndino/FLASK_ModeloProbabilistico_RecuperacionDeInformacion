"""_summary_

    :authors: Jerson Andino, Carlos Lopez, Milton Casnanzuela
    :description: A flask application for test the probabilistic method of information recovery.
"""
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
# import nltk
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from collections import Counter
from math import log
import time


# nltk.download('punkt')
# nltk.download('stopwords')

# Crear la carpeta 'uploaded_files' si no existe
if not os.path.exists('uploaded_files'):
    os.makedirs('uploaded_files')

app = Flask(__name__)

documentos=[]
documentos_limpios=[]
stop_words=['a','al','con','de','del','el','en','es','están','la','los','las','su','un','una','unos','unas','tiene','va','y']
V = []
frecuencias=[]
ni=[]
qi=[]
ci=[]

def limpiar_doc(documento):
    return documento.split()

def vectorizar(documento,V):
    q_v=[]
    for word in V:
        if word in documento:
            q_v.append(1)
        else:
            q_v.append(0)
    return q_v

def calcular_v(documentos_limpios):
    V.clear()
    if documentos_limpios:
        for d in documentos_limpios:
            for word in d:
                if word not in V:
                    V.append(word)  
    else:
        V.clear()
    # print(V)

def calcular_frecuencias(documentos_limpios, V):
    # print(D)
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
        # print(D2)
    # print(frecuencias)

def calcular_ni(frecuencias,V):
    ni.clear()
    for i in range(len(V)):
        cont=0
        for d in frecuencias:
            if d[i]>0:
                cont+=1
        ni.append(cont)

def calcular_qi(ni):
    qi.clear()
    N=len(documentos)
    # print(N)
    for n in ni:
        qi.append(n/N)
        
def calcular_ci(ni):
    ci.clear()
    N=len(documentos)
    
    for n in ni:
        # r=log((N-n)/n,10)
        # print(N)
        # print(n)
        ci.append(log((N-n)/n,10))
        # ci.append(10)
    # print(ci)
    
def calcular_tabla(documentos):
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

def ordenar_sim(sim):
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
    
    return nuevo_orden

def consultar_q(frecuencias, ci, q):
    D3=[]
    n=len(V)
    for d in frecuencias:
        d_temp=[]
        for i in range(n):
            d_temp.append(q[i]*d[i])
        D3.append(d_temp)
    D4=[]    
    for d in D3:
        d_temp=[]
        for i in range(n):
            d_temp.append(d[i]*ci[i])
        D4.append(d_temp)  
    sim=[]  
    for d in D4:
        sim.append(abs(sum(d)))
    sim_copy=sim.copy()    
    return (sim, ordenar_sim(sim_copy))
        
    

@app.route('/', methods=['GET', 'POST'])
def home():
    content = dict()
    if request.method == 'POST':
        # print(request.form)
        if request.form['tipo_post']=='3':
            if not ci:
                content['not_ready']=True
            else:
                consulta=request.form['consulta']
                q=vectorizar(limpiar_doc(consulta),V)
                inicio = time.time_ns()
                (sim, orden_docs) = consultar_q(frecuencias,ci,q)
                fin = time.time_ns()
                print(inicio)
                print(fin)
                print(fin-inicio)
                content['sim']=sim
                content['orden_docs']=orden_docs    
                content['consulta'] = consulta   
                content['tiempo'] = fin-inicio        
            
    calcular_v(documentos_limpios)
    calcular_frecuencias(documentos_limpios,V)
    calcular_ni(frecuencias,V)
    tabla_pesos = calcular_tabla(documentos)
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
                file=open(file_path)
                doc = file.read()
                file.close()
                documentos.append(doc)
                documentos_limpios.append(limpiar_doc(doc))
            else:
                if request.form['texto']:
                    documentos.append(request.form['texto'])
                    documentos_limpios.append(limpiar_doc(request.form['texto']))
        if request.form['tipo_post']=='1':
            index_doc = int(request.form['doc_index'])
            documentos.pop(index_doc-1)
            documentos_limpios.pop(index_doc-1)
            # print(documentos)
            # print(index_doc)
        if request.form['tipo_post']=='2':
            documentos.clear()
            documentos_limpios.clear()
    
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    
    return render_template('cargar_documento.html', **content)

@app.route('/calcular', methods=['GET'])
def calcular():
    content = dict()
    calcular_v(documentos_limpios)
    calcular_frecuencias(documentos_limpios,V)
    calcular_ni(frecuencias,V)
    tabla_pesos = calcular_tabla(documentos)
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    content['frecuencias']=frecuencias
    content['ni']=ni
    content['tabla_pesos']=tabla_pesos
    # tu código para calcular las frecuencias y relevancias va aquí
    return render_template('calcular.html', **content)

@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    consulta = None
    if request.method == 'POST':
        consulta = request.form['consulta']
        # tu código para consultar documentos va aquí
    return render_template('consultar.html', consulta=consulta)


if __name__ == '__main__':
    app.run(debug=True)
