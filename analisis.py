#imports----------------------------------------------------------------
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import product

#variables----------------------------------------------------------------

canales=[ [0,1,1,0,1,1,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1],
          [0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0],
          [0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0]
          ]

canales2 = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


combinaciones_posibles=[]
combinaciones_canales=[]
data2=[]
#funciones---------------------------------------------------------------------

def barras_resultado():
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Gráfico de Barras para Resultado")

    # Crear y mostrar la gráfica de barras en la nueva ventana
    grafica_barras_resultado = plt.Figure(figsize=(5, 4), dpi=100)
    ax = grafica_barras_resultado.add_subplot(111)

    # Obtener nombres de columnas y valores de resultado
    columnas_resultado = resultado.columns
    valores_resultado = resultado.iloc[0].values  # Tomar la primera fila de resultado

    # Crear un gráfico de barras
    ax.bar(columnas_resultado, valores_resultado)

    # Configurar etiquetas y título
    ax.set_xlabel('Columna')
    ax.set_ylabel('Valor en Resultado')
    ax.set_title('Gráfico de Barras para Resultado')

    # Mostrar la gráfica en la nueva ventana
    canvas = FigureCanvasTkAgg(grafica_barras_resultado, master=ventana_resultados)
    canvas.draw()
    canvas.get_tk_widget().pack()


def mostrar_ventana_resultados():
    if not resultado.empty:
        # Crear una nueva ventana para mostrar la tabla de resultados
        ventana_resultados = tk.Toplevel(ventana)
        ventana_resultados.title("Tabla de Resultados")

        # Crear un Treeview en la nueva ventana
        tree = ttk.Treeview(ventana_resultados, columns=['columnas'] + list(resultado.columns), show="headings")

        # Configurar las columnas
        tree.heading('columnas', text='Columnas')  # Columna adicional para mostrar los nombres de las filas
        for col in resultado.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)  # Ajusta el ancho de las columnas según tus necesidades

        # Insertar los datos en el Treeview
        for nombre_fila, row in resultado.iterrows():
            tree.insert("", "end", values=[nombre_fila] + list(row))

        # Colocar el Treeview en la nueva ventana
        tree.pack()
    else:
        messagebox.showinfo("Advertencia", "La tabla de resultados está vacía.")

def obtener_dato_ingresado():
    global indice_deseado, fila_resultante  # Necesario para modificar las variables globales
    indice_deseado = str(dato_ingresado.get())
    fila_resultante = obtener_fila_por_indice(df5, indice_deseado)

#nos devuelve todas las combinaciones de binarios posibles
def generar_combinaciones_binarias(n):
    for combinacion in product("01", repeat=n):
        combinaciones_posibles.append("".join(combinacion))

def cargar_combinaciones_canales():
  #iterar las veces de items que tenga el primer canal ya que todos tienen la misma cantidad de items
  for i in range(len(canales[0])):
      combinacion=[]
      #necesitamos sacar la combinacion según la cantidad de canales, se agrega cada elemento de la posición, se pasan a string y se agrega a combinaciones canales
      for j in range(len(canales)):
        combinacion.append(canales[j][i])
      combinacion = [str(elemento) for elemento in combinacion]
      resultado = ''.join(combinacion)
      combinaciones_canales.append(resultado)


def obtener_indices(x):
  indices=[]

  for j in range(len(combinaciones_canales)):
    if combinaciones_posibles[x] == combinaciones_canales[j]:
      indices.append(j)

  return indices


def obtener_fila_por_indice(dataframe, indice):
    try:
        fila_seleccionada = dataframe.loc[indice]
        return pd.DataFrame(fila_seleccionada).transpose()  # Transponemos para obtener una fila en lugar de una columna
    except KeyError:
        print(f"No se encontró el índice {indice}.")
        return None
    
    
# Función para mostrar la tabla
def mostrar_tabla(data):
    # Crear una nueva ventana (toplevel) para la tabla
    ventana_tabla = tk.Toplevel(ventana)
    ventana_tabla.title("Tabla")

    # Crear un Treeview en la nueva ventana
    tree = ttk.Treeview(ventana_tabla, columns=['estados'] + list(data.columns), show="headings")

    # Configurar las columnas
    tree.heading('estados', text='estados')  # Columna adicional para mostrar los nombres de las filas
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Ajusta el ancho de las columnas según tus necesidades

    # Insertar los datos en el Treeview
    for nombre_fila, row in data.iterrows():
        tree.insert("", "end", values=[nombre_fila] + list(row))

    # Coloca el Treeview en la nueva ventana
    tree.pack()


def mostrar_tabla_marginizada(data):
    # Crear una nueva ventana (toplevel) para la tabla
    ventana_tabla = tk.Toplevel(ventana)
    ventana_tabla.title("Tabla")

    # Crear un Treeview en la nueva ventana
    tree = ttk.Treeview(ventana_tabla, columns=['estados'] + list(data.columns), show="headings")

    # Configurar las columnas
    tree.heading('estados', text='estados')  # Columna adicional para mostrar los nombres de las filas
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Ajusta el ancho de las columnas según tus necesidades

    # Insertar los datos en el Treeview
    for nombre_fila, row in data.iterrows():
        tree.insert("", "end", values=[nombre_fila] + list(row))

    # Coloca el Treeview en la nueva ventana
    tree.pack()

def grafica_barras_fila_resultante(fila_resultante):
    # Crear una figura y ejes
    fig, ax = plt.subplots()

    # Obtener nombres de columnas y valores de la fila resultante
    columnas = fila_resultante.columns
    valores = fila_resultante.values.flatten()

    # Crear un gráfico de barras
    ax.bar(columnas, valores)

    # Configurar etiquetas y título
    plt.xlabel('Columna')
    plt.ylabel('Valor en la Fila Resultante')
    plt.title(f'Gráfico de Barras para la Fila {indice_deseado}')

    # Mostrar el gráfico
    plt.show()
    
def grafica_barras_data_sumada():
    # Crear una figura y ejes
    fig, ax = plt.subplots()

    # Obtener nombres de columnas y valores de data_sumada
    columnas = data_sumada.columns
    valores = data_sumada.loc[[indice_deseado]].values  # Utilizar el índice deseado

    # Obtener el número de barras
    num_barras = len(columnas)

    # Crear un rango para la posición de las barras
    posicion_barras = np.arange(num_barras)

    # Crear un gráfico de barras verticales intercambiando x e y
    ax.bar(posicion_barras, valores.flatten(), align='center', label=indice_deseado)  # Utilizar flatten para convertir a una dimensión

    # Configurar etiquetas y título
    plt.ylabel('Valor en Data Sumada')
    plt.xlabel('Columna')
    plt.title(f'Gráfico de Barras para Data Sumada - Índice: {indice_deseado}')

    # Mostrar las etiquetas en el eje x
    ax.set_xticks(posicion_barras)
    ax.set_xticklabels(columnas)

    # Mostrar la leyenda
    ax.legend()

    # Mostrar el gráfico
    plt.show()

def eliminar_caracter_columnas(dataframe, indice_a_eliminar):
    # Iterar sobre todas las columnas del DataFrame
    for columna in dataframe.columns:
        # Obtener el valor actual de la columna
        valor_original = columna

        # Eliminar el índice especificado
        nuevo_valor = valor_original[:indice_a_eliminar] + valor_original[indice_a_eliminar + 1:]

        # Renombrar la columna en el DataFrame
        dataframe = dataframe.rename(columns={columna: nuevo_valor})

    return dataframe
  
def sumar_columnas_repetidas(dataframe):
    # Agrupar por nombre de columna y sumar los valores
    dataframe_sumado = dataframe.groupby(dataframe.columns, axis=1).sum()

    return dataframe_sumado

def obtener_numero_ingresado():
    global indice_a_eliminar, data_marginizada, data_sumada  # Necesario para modificar las variables globales
    indice_a_eliminar = int(numero_ingresado.get())
    data_marginizada = eliminar_caracter_columnas(df5, indice_a_eliminar)
    data_sumada = sumar_columnas_repetidas(data_marginizada)
    print("la data sumada es ", data_sumada)  # Agrega esta línea para verificar si data_sumada se actualiza correctamente

def eliminar_posicion_digito_fila(dataframe, posicion_a_eliminar):
  # Crear una copia del DataFrame original
  nuevo_dataframe = dataframe.copy()

  # Obtener el nombre de las filas
  nombres_filas = nuevo_dataframe.index.tolist()

  # Eliminar el dígito en la posición especificada para cada nombre de fila
  nuevos_nombres_filas = [nombre[:posicion_a_eliminar] + nombre[posicion_a_eliminar + 1:] for nombre in nombres_filas]

  # Asignar los nuevos nombres al índice del DataFrame
  nuevo_dataframe.index = nuevos_nombres_filas

  return nuevo_dataframe
  
def sumar_filas_similares(dataframe):
    # Obtener una copia del DataFrame original
    nuevo_dataframe = dataframe.copy()

    # Agrupar por el índice y sumar las filas con el mismo nombre
    nuevo_dataframe = nuevo_dataframe.groupby(nuevo_dataframe.index).sum()

    # Dividir cada valor en el DataFrame entre 2
    nuevo_dataframe = nuevo_dataframe / 2

    return nuevo_dataframe

#ejecucción----------------------------------------------------

#obtenemos todas las combinaciones en la variable combinaciones posibles
generar_combinaciones_binarias(len(canales))
cargar_combinaciones_canales()

#obtendremos coincidencias

for i in range(len(combinaciones_posibles)):
  #obtenemos los índices siguientes a las coincidencias
  indices= obtener_indices(i)
  for k in canales:
      datos_tabla=[]
      coincidencias=0
      total=0
      for l in indices:
        if l+1 != len(canales[0]):
          if k[l + 1] == 1 :
              coincidencias=coincidencias+1
              total=total+1
          else:
              total=total+1
      if(total!=0):
        datos_tabla.append(coincidencias/total)

      data2.extend(datos_tabla)

data2 = [data2[i:i+ len(canales)] for i in range(0, len(data2), len(canales))]

# Crear nombres para las columnas y filas
column_names = ['canal{}'.format(i + 1) for i in range(len(canales))]
index_names = combinaciones_posibles

# Convertir el array de NumPy en un DataFrame de Pandas con nombres
df = pd.DataFrame(data2, columns=column_names, index=index_names)

# Mostrar el DataFrame resultante
print(df)
    
#-ejercicio2-------------------------------

#solución punto 2

data3=[]

for i in range(len(combinaciones_posibles)):
  #obtenemos los índices siguientes a las coincidencias
  indices= obtener_indices(i)
  for k in range(len(combinaciones_posibles)):
      datos_tabla2=[]
      coincidencias=0
      total=0
      for l in indices:
        if l+1 != len(combinaciones_canales):
          if combinaciones_canales[l + 1] == combinaciones_posibles[k] :
              coincidencias=coincidencias+1
              total=total+1
          else:
              total=total+1
      if(total!=0):
        datos_tabla2.append(coincidencias/total)

      data3.extend(datos_tabla2)

data3 = [data3[i:i+ len(combinaciones_posibles)] for i in range(0, len(data3), len(combinaciones_posibles))]

# Crear nombres para las columnas y filas
column_names = combinaciones_posibles
index_names = combinaciones_posibles

# Convertir el array de NumPy en un DataFrame de Pandas con nombres
df2 = pd.DataFrame(data3, columns=column_names, index=index_names)

# Mostrar el DataFrame resultante
print(df2)

#ejercicio 3 -------------------------------------------------------------------------------------

data4=[]

for i in range(len(combinaciones_posibles)):
  #obtenemos los índices siguientes a las coincidencias
  indices= obtener_indices(i)
  for k in canales:
      datos_tabla=[]
      coincidencias=0
      total=0
      for l in indices:
        if l != 0:
          if k[l - 1] == 1 :
              coincidencias=coincidencias+1
              total=total+1
          else:
              total=total+1
      if(total!=0):
        datos_tabla.append(coincidencias/total)

      data4.extend(datos_tabla)

data4 = [data4[i:i+ len(canales)] for i in range(0, len(data4), len(canales))]

# Crear nombres para las columnas y filas
column_names = ['canal{}'.format(i + 1) for i in range(len(canales))]
index_names = combinaciones_posibles

# Convertir el array de NumPy en un DataFrame de Pandas con nombres
""" df4 = pd.DataFrame(data4, columns=column_names, index=index_names)

# Mostrar el DataFrame resultante
print(df4) """

#ejercicio4------------------------------------------------

#solución punto 4

data5=[]

for i in range(len(combinaciones_posibles)):
  #obtenemos los índices siguientes a las coincidencias
  indices= obtener_indices(i)
  for k in range(len(combinaciones_posibles)):
      datos_tabla2=[]
      coincidencias=0
      total=0
      for l in indices:
        if l != 0:
          if combinaciones_canales[l - 1] == combinaciones_posibles[k] :
              coincidencias=coincidencias+1
              total=total+1
          else:
              total=total+1
      if(total!=0):
        datos_tabla2.append(coincidencias/total)

      data5.extend(datos_tabla2)

data5 = [data5[i:i+ len(combinaciones_posibles)] for i in range(0, len(data5), len(combinaciones_posibles))]

# Crear nombres para las columnas y filas
column_names = combinaciones_posibles
index_names = combinaciones_posibles

# Convertir el array de NumPy en un DataFrame de Pandas con nombres
df5 = pd.DataFrame(data5, columns=column_names, index=index_names)

# Mostrar el DataFrame resultante
print(df5)
    
#Marginalizar--------------------------------------------------------------- 

def mostrar_ventana_punto3():
    ventana_punto3 = tk.Toplevel(ventana)
    ventana_punto3.title("Punto 3")

    # Variables para almacenar la información
    vfuturo = []
    vpresente = [None, None, None]

    # Función para guardar la información
    def guardar_informacion():

        nonlocal vfuturo
        vfuturo = [check_a.get(), check_b.get(), check_c.get()]

        nonlocal vpresente
        vpresente = [entrada_a.get(), entrada_b.get(), entrada_c.get()]
        global resultado
        resultado= pd.DataFrame()
        
        for l in range(len(vfuturo)):
          if vfuturo[l] == True:
            for v in range(len(vfuturo)):
              copia=df5
              if vfuturo[v] == True:
                if(v == 0):
                  copia=eliminar_caracter_columnas(copia, 1)
                  copia=sumar_columnas_repetidas(copia)
                  copia=eliminar_caracter_columnas(copia, 2)
                  copia=sumar_columnas_repetidas(copia)
                if(v == 1):
                  copia=eliminar_caracter_columnas(copia, 0)
                  copia=sumar_columnas_repetidas(copia)
                  copia=eliminar_caracter_columnas(copia, 2)
                  copia=sumar_columnas_repetidas(copia)
                if(v == 2):
                  copia=eliminar_caracter_columnas(copia, 0)
                  copia=sumar_columnas_repetidas(copia)
                  copia=eliminar_caracter_columnas(copia, 1)
                  copia=sumar_columnas_repetidas(copia)
                  
            for k in range(len(vpresente)):
              if vpresente[k] == '':
                if(k == 0):
                    copia=eliminar_posicion_digito_fila(copia, 1)
                    copia=sumar_filas_similares(copia)
                    copia=eliminar_posicion_digito_fila(copia, 2)
                    copia=sumar_filas_similares(copia)
                if(k == 1):
                  copia=eliminar_posicion_digito_fila(copia, 0)
                  copia=sumar_filas_similares(copia)
                  copia=eliminar_posicion_digito_fila(copia, 2)
                  copia=sumar_filas_similares(copia)
                if(k == 2):
                  copia=eliminar_posicion_digito_fila(copia, 0)
                  copia=sumar_filas_similares(copia)
                  copia=eliminar_posicion_digito_fila(copia, 1)
                  copia=sumar_filas_similares(copia) 
            print("jee")
            print(resultado)
            if(resultado.empty):
              resultado=copia
            else:
              resultado= resultado*copia
                             
        # Dentro de la función guardar_informacion después de calcular resultado
        if not resultado.empty:
          # Mostrar la ventana de resultados
          mostrar_ventana_resultados()
          barras_resultado()

        ventana_punto3.destroy()
        
    # Checkbox para el punto 3
    check_a = tk.BooleanVar()
    check_b = tk.BooleanVar()
    check_c = tk.BooleanVar()


    tk.Checkbutton(ventana_punto3, text="A", variable=check_a).grid(row=0, column=0)
    tk.Checkbutton(ventana_punto3, text="B", variable=check_b).grid(row=1, column=0)
    tk.Checkbutton(ventana_punto3, text="C", variable=check_c).grid(row=2, column=0)

    # Labels e inputs para el presente
    tk.Label(ventana_punto3, text="A").grid(row=0, column=1)
    tk.Label(ventana_punto3, text="B").grid(row=1, column=1)
    tk.Label(ventana_punto3, text="C").grid(row=2, column=1)

    entrada_a = tk.Entry(ventana_punto3)
    entrada_b = tk.Entry(ventana_punto3)
    entrada_c = tk.Entry(ventana_punto3)

    entrada_a.grid(row=0, column=2)
    entrada_b.grid(row=1, column=2)
    entrada_c.grid(row=2, column=2)

    # Botón para guardar la información
    boton_guardar = tk.Button(ventana_punto3, text="Guardar", command=guardar_informacion)
    boton_guardar.grid(row=3, column=0, columnspan=3, pady=10)

    # Centrar la ventana en la pantalla principal
    ventana_punto3.geometry("+{}+{}".format(
        int((ventana.winfo_screenwidth() - ventana_punto3.winfo_reqwidth()) / 2),
        int((ventana.winfo_screenheight() - ventana_punto3.winfo_reqheight()) / 2)
    ))
    
#ventana-----------------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Proyecto Analisis")

dato_ingresado = tk.StringVar()
numero_ingresado = tk.DoubleVar()

# Crear el campo de entrada
campo_entrada = tk.Entry(ventana, textvariable=dato_ingresado)
campo_entrada.pack()

campo_numero = tk.Entry(ventana, textvariable=numero_ingresado)
campo_numero.pack()

# Botón para obtener el dato ingresado
boton_obtener_dato = tk.Button(ventana, text="Obtener Dato", command=obtener_dato_ingresado)
boton_obtener_dato.pack()

# Botón para obtener el número ingresado
boton_obtener_numero = tk.Button(ventana, text="Obtener numero", command=obtener_numero_ingresado)
boton_obtener_numero.pack()


# Botón para mostrar la tabla
boton_mostrar_tabla = tk.Button(ventana, text="Mostrar Tabla", command=lambda:mostrar_tabla(df5))
boton_mostrar_tabla.pack()


# Botón para mostrar la tabla marginizada
boton_mostrar_tabla_marginizada = tk.Button(ventana, text="Mostrar Tabla marginizada", command=lambda:mostrar_tabla_marginizada(data_sumada))
boton_mostrar_tabla_marginizada.pack()

# Botón para mostrar la gráfica de barras de data_sumada
boton_grafica_barras_data_sumada = tk.Button(ventana, text="Gráfico de Barras para Data Sumada", command=grafica_barras_data_sumada)
boton_grafica_barras_data_sumada.pack()

""" boton_archivo = tk.Button(ventana, text="Cargar Archivo", command=hacer_clic)
boton_archivo.pack() """

# Botón para mostrar el gráfico de barras para la fila resultante
boton_grafica_barras_fila_resultante = tk.Button(ventana, text="Gráfico de Barras para la Fila ", command=lambda: grafica_barras_fila_resultante(fila_resultante))
boton_grafica_barras_fila_resultante.pack()

# Botón para mostrar la ventana del punto 3
boton_punto3 = tk.Button(ventana, text="Punto 3", command=mostrar_ventana_punto3)
boton_punto3.pack()

etiqueta = tk.Label(ventana, text="")
etiqueta.pack()

ventana.mainloop()