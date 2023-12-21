#imports----------------------------------------------------------------
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from itertools import product
from scipy.stats import wasserstein_distance

#variables----------------------------------------------------------------

canales=[ [0,1,1,0,1,1,0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,0,0,1],
          [0,0,0,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,0,1,1,1,1,0,0,0],
          [0,1,0,1,0,1,0,1,0,1,1,0,1,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,0]

          ]

combinaciones_posibles=[]
combinaciones_canales=[]
data2=[]

datasustentacion=np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1]])

#funciones---------------------------------------------------------------------

def calculate_emd_marginal(df1, df2):
    # Asumiendo que ambos DataFrames tienen el mismo tamaño y las mismas etiquetas de filas/columnas.
    
    # Obtener distribuciones marginales sumando sobre las columnas
    marginal1 = df1.sum(axis=1)
    marginal2 = df2.sum(axis=1)
    
    # Calcular la Earth Mover's Distance entre las dos distribuciones marginales
    emd_value = wasserstein_distance(marginal1, marginal2)
    
    return emd_value


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

def ptensorial(df1,df2):
    # Verificar que los índices de ambos DataFrames coinciden y están en el mismo orden
    assert (df1.index == df2.index).all(), "Indices of both DataFrames must match."
    
    # Inicializar un diccionario para recoger los datos del producto tensorial
    tensor_data = {}

    # Calcular el producto tensorial
    for col1 in df1.columns:
        for col2 in df2.columns:
            # El nombre de la nueva columna será la combinación de los nombres de las filas originales
            new_col_name = col1 + col2
            # Realizar la multiplicación elemento a elemento
            tensor_data[new_col_name] = df1[col1] * df2[col2]

    # Crear el nuevo DataFrame usando el diccionario
    tensor_df = pd.DataFrame(tensor_data, index=df1.index)

    return tensor_df

def tensor_product(df1, df2):
    # Asegurarse de que ambos DataFrames tienen el mismo índice
    assert df1.index.equals(df2.index), "Los índices de ambos DataFrames deben coincidir."
    
    # Crear el nuevo DataFrame con las combinaciones de nombres de columna
    tensor_product_columns = [f'{c1}_{c2}' for c1 in df1.columns for c2 in df2.columns]
    tensor_df = pd.DataFrame(index=df1.index, columns=tensor_product_columns)
    
    # Llenar el nuevo DataFrame con los productos tensoriales
    for index in df1.index:
        for c1 in df1.columns:
            for c2 in df2.columns:
                tensor_df.loc[index, f'{c1}_{c2}'] = df1.loc[index, c1] * df2.loc[index, c2]
    
    return tensor_df

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

dataframesustentacion=pd.DataFrame(datasustentacion, columns=column_names, index=index_names)






    
#Marginalizar--------------------------------------------------------------- 

def mostrar_ventana_final():
    ventana_final = tk.Toplevel(ventana)
    ventana_final.title("Punto 3")

    # Variables para almacenar la información
    vfuturo2 = []
    vpresente2 = [None, None, None]

    # Función para guardar la información
    def marginizardata(vfuturo, vpresente):

        """ vfuturo = [check_a.get(), check_b.get(), check_c.get()]

        vpresente = [entrada_a.get(), entrada_b.get(), entrada_c.get()] """
        global resultado
        resultado= pd.DataFrame()
        
        for l in range(len(vfuturo)):
          if vfuturo[l] == True:
            for v in range(len(vfuturo)):
              copia=dataframesustentacion
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
            if(resultado.empty):
              resultado=copia
            else:
              resultado= ptensorial(resultado,copia)
                             
            return resultado
        

    #función proyecto final programación dinámica
        
    def bottonup():
      tabla=[]
      vfuturoejemplo=[False,True,True]
      vpresenteejemplo=[1, 0 ,'']
      asociacion = {0: 'A', 1: 'B', 2: 'C'}
      optimo= 123132132
      cadenaoptima= ""
      dataoptima= None

      for k in range(len(vfuturoejemplo)):
         for j in range(len(vpresenteejemplo)):
          if(vfuturoejemplo[k] == True):
              #nuevos array donde todos cambian menos en la posición k
              nuevo_array = [False if i == k else True for i in range(len(vfuturoejemplo))] 
              nuevo_array_2 = [val if i == j else ' ' for i, val in enumerate(vpresenteejemplo)]
              letrafuturo1 = asociacion[k]
              letraactual1 = asociacion[j]
              cadena_parcial = f"{letrafuturo1}/{letraactual1}"

              # Buscar si cadena_parcial está en alguna clave del array tabla
              valor_asociado = None
              for diccionario in tabla:
                  if cadena_parcial in diccionario:
                      valor_asociado = diccionario[cadena_parcial]
                      break
              
              # Si cadena_parcial no se encontró, calcular x con marginizardata
              if valor_asociado is None:
                  x = marginizardata(nuevo_array, nuevo_array_2)
                  tabla.append({cadena_parcial: x})
              else:
                  x = valor_asociado
              
              array_inverso = [True if i == k else False for i in range(len(vfuturoejemplo))] 
              array_inverso2= [' ' if i == j or val == ' ' else val for i, val in enumerate(vpresenteejemplo)]

              # Obtener letras asociadas a las posiciones que cumplen las condiciones
              letra2_futuro = ''.join([asociacion[i] for i in range(len(array_inverso)) if array_inverso[i]])
              letra2_presente = ''.join([asociacion[i] for i in range(len(array_inverso2)) if array_inverso2[i] != ' '])
              cadena_parcial2= f"{letra2_futuro}/{letra2_presente}"

              # Buscar si cadena_parcial está en alguna clave del array tabla
              valor_asociado2 = None
              for diccionario in tabla:
                  if cadena_parcial2 in diccionario:
                      valor_asociado2 = diccionario[cadena_parcial2]
                      break
              
              # Si cadena_parcial no se encontró, calcular x con marginizardata
              if valor_asociado2 is None:
                  x2 = marginizardata(array_inverso, array_inverso2)
                  tabla.append({cadena_parcial2: x2})
              else:
                  x2 = valor_asociado2
              
              x2= x2.transpose()
              df_x = pd.DataFrame(x)
              df_x2 = pd.DataFrame(x2)
              df_resultado= tensor_product(df_x,df_x2)
              
              cadena_resultado = f"{letrafuturo1}/{letraactual1} * {letra2_futuro}/{letra2_presente}"
              tabla.append({cadena_resultado: df_resultado})
              original = marginizardata(vfuturoejemplo,vpresenteejemplo)
              df_original = pd.DataFrame(original)
              emd_result = calculate_emd_marginal(df_resultado, df_original)
              if(emd_result <= optimo):
                 optimo= emd_result
                 cadenaoptima= cadena_resultado
                 dataoptima= df_resultado
              print("emd")
              print(emd_result)
              print("expresión")
              print(cadena_resultado)

          return optimo, cadenaoptima, dataoptima

    bottonup()
    # Checkbox para el punto 3
    check_a = tk.BooleanVar()
    check_b = tk.BooleanVar()
    check_c = tk.BooleanVar()


    tk.Checkbutton(ventana_final, text="A", variable=check_a).grid(row=0, column=0)
    tk.Checkbutton(ventana_final, text="B", variable=check_b).grid(row=1, column=0)
    tk.Checkbutton(ventana_final, text="C", variable=check_c).grid(row=2, column=0)

    # Labels e inputs para el presente
    tk.Label(ventana_final, text="A").grid(row=0, column=1)
    tk.Label(ventana_final, text="B").grid(row=1, column=1)
    tk.Label(ventana_final, text="C").grid(row=2, column=1)

    entrada_a = tk.Entry(ventana_final)
    entrada_b = tk.Entry(ventana_final)
    entrada_c = tk.Entry(ventana_final)

    entrada_a.grid(row=0, column=2)
    entrada_b.grid(row=1, column=2)
    entrada_c.grid(row=2, column=2)

    # Botón para guardar la información
    boton_guardar = tk.Button(ventana_final, text="Guardar", command=bottonup)
    boton_guardar.grid(row=3, column=0, columnspan=3, pady=10)

    # Centrar la ventana en la pantalla principal
    ventana_final.geometry("+{}+{}".format(
        int((ventana.winfo_screenwidth() - ventana_final.winfo_reqwidth()) / 2),
        int((ventana.winfo_screenheight() - ventana_final.winfo_reqheight()) / 2)
    ))
    
#ventana-----------------------------------------------------------------------------
ventana = tk.Tk()
ventana.title("Proyecto Analisis")


# Botón para mostrar la tabla
boton_mostrar_tabla = tk.Button(ventana, text="Mostrar Tabla Original", command=lambda:mostrar_tabla(df5))
boton_mostrar_tabla.pack()


# Botón para mostrar la ventana del punto 3
boton_punto3 = tk.Button(ventana, text="Punto 3", command=mostrar_ventana_final)
boton_punto3.pack()

etiqueta = tk.Label(ventana, text="")
etiqueta.pack()


ventana.mainloop()