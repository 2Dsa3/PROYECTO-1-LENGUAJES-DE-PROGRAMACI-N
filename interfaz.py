from tkinter import *
from AnalizadorLexico import analyze_lexically
from AnalizadorSintactico import analyze_syntactically


# Crear la ventana principal
root = Tk()
root.title("Analizador Léxico, Sintáctico y Semántico del lenguaje de programación DART")  # Título de la ventana
root.geometry("600x500")  # Tamaño de la ventana
root.config(bg="#f0f0f0")  # Fondo de la ventana

# Etiqueta principal con un estilo más atractivo
myLabel = Label(root, text="Analizador Léxico, Sintáctico y Semántico", font=("Helvetica", 16, "bold"), fg="#333", bg="#f0f0f0")
myLabel.pack(pady=20)  # Añadimos un poco de espacio vertical

# Caja de entrada para ingresar el texto (por ejemplo, código fuente)
inputLabel = Label(root, text="Ingresa el código fuente:", font=("Helvetica", 12), bg="#f0f0f0")
inputLabel.pack(pady=10)

inputText = Text(root, height=6, width=60, font=("Helvetica", 12), bg="#fff", fg="#333")
inputText.pack(pady=10)

# Contenedor de consola para mostrar tokens válidos, no válidos y errores de sintaxis
consoleLabel = Label(root, text="Consola de Resultados:", font=("Helvetica", 12), bg="#f0f0f0")
consoleLabel.pack(pady=10)

consoleOutput = Text(root, height=8, width=60, font=("Courier", 10), bg="#333", fg="white")
consoleOutput.pack(pady=10)
consoleOutput.config(state=DISABLED)  # Deshabilitamos la edición directa del texto

# Función para analizar el código e imprimir los resultados en la "consola"
def run_analysis():
    input_code = inputText.get("1.0", "end-1c")  # Obtener el texto ingresado
    consoleOutput.config(state=NORMAL)  # Habilitamos la edición temporalmente para escribir en la consola
    consoleOutput.delete(1.0, END)  # Limpiar la consola antes de mostrar los resultados
    consoleOutput.update()  # Actualizar la consola
    # Llamar las funciones
    result, syntax_error = analyze_syntactically(input_code)  # Aquí obtenemos el resultado y los errores sintácticos
    tokens, lexical_errors = analyze_lexically(input_code)  # Aquí obtenemos los errores léxicos
    # Mostrar los errores léxicos
    if lexical_errors:
        consoleOutput.insert(END, "Hay Errores Léxicos:\n")
        consoleOutput.insert(END, "\n".join(lexical_errors) + "\n\n")
    else:
        consoleOutput.insert(END, "No se encontraron errores léxicos.\n\n")
        consoleOutput.insert(END, tokens)
        consoleOutput.insert(END,"\n\n")
    # Mostrar los errores sintácticos
    if syntax_error:
        consoleOutput.insert(END, "Hay Error Sintáctico:\n")
        consoleOutput.insert(END, syntax_error)
        consoleOutput.insert(END, "\n\n")
    else:
        consoleOutput.insert(END, "No se encontraron errores sintácticos.\n\n")
        consoleOutput.insert(END, str(result)+ "\n\n")
    consoleOutput.config(state=DISABLED)
    

# Botón para ejecutar el análisis
runButton = Button(root, text="Ejecutar Análisis", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=run_analysis)
runButton.pack(pady=20)

# Iniciar el bucle principal de la aplicación
root.mainloop()
