import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

documentos=[]
documentos_limpios=[]
nombres_docs=[]
stop_words=['a','al','con','de','del','el','en','es','están','la','los','las','su','un','una','unos','unas','tiene','va','y','que']
V = []
frecuencias=[]
ni=[]
qi=[]
ci=[]

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
#################################################
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
