"""_summary_

    :authors: Jerson Andino, Carlos Lopez, Milton Casnanzuela
    :description: A flask application for test the probabilistic method of information recovery.
"""
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from math import log
import time
import modelo as mdl
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Crear la carpeta 'uploaded_files' si no existe
if not os.path.exists('uploaded_files'):
    os.makedirs('uploaded_files')

app = Flask(__name__)
documentos=[]
documentos_limpios=[]
nombres_docs=[]
V = []
frecuencias=[]
stop_words = []
ni=[]
qi=[]
ci=[]

@app.route('/', methods=['GET', 'POST'])
def home():
    content = dict()
    if request.method == 'POST':
        if request.form['tipo_post']=='3':
            if not ci:
                content['not_ready']=True
            else:
                consulta=request.form['consulta']
                q=mdl.vectorizar(limpiar_doc(consulta),V)
                inicio = time.time_ns()
                (sim, orden_docs) = mdl.consultar_q(frecuencias,ci,q)
                fin = time.time_ns()
                content['sim']=sim
                content['orden_docs']=orden_docs    
                content['consulta'] = consulta   
                content['tiempo'] = (fin-inicio)/10**(9)        
            
    mdl.calcular_v(documentos_limpios)
    mdl.calcular_frecuencias(documentos_limpios,V)
    mdl.calcular_ni(frecuencias,V)
    tabla_pesos = mdl.calcular_tabla()
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
                documentos_limpios.append(mdl.limpiar_doc(doc))
                nombres_docs.append(filename)
            else:
                if request.form['texto']:
                    documentos.append(request.form['texto'])
                    documentos_limpios.append(mdl.limpiar_doc(request.form['texto']))
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

@app.route('/calcular', methods=['GET'])
def calcular():
    content = dict()
    tabla_pesos = mdl.calcular_tabla()
    content['ed']=len(documentos)
    content['docs']=documentos
    content['V']=V
    content['frecuencias']=frecuencias
    content['ni']=ni
    content['tabla_pesos']=tabla_pesos
    return render_template('calcular.html', **content)

@app.route('/revision', methods=['GET','POST'])
def revision():
    content=dict()
    content['docs']=documentos
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
                documentos_limpios.append(mdl.limpiar_doc(doc))
                nombres_docs.append(filename)
            else:
                if request.form['texto']:
                    documentos.append(request.form['texto'])
                    documentos_limpios.append(mdl.limpiar_doc(request.form['texto']))
                    nombres_docs.append(request.form['texto'])

    return render_template('revision.html', **content)

if __name__ == '__main__':
    app.run(debug=True)
