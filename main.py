from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext, font

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Texto")
        self.root.geometry("1000x400")
        self.root.resizable(False,False)  # Evitar redimensionamiento
        
        # Menú superior
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        
        

        # Crear un tema personalizado para los botones
        style = ttk.Style()
        style.configure("Custom.TButton",
                        background='#333333', 
                        foreground='black', 
                        font=("Helvetica", 18),
                        padding=0,
                        width=10,
                        height=10
        )
        # Importamos imagenes y le damos tamaño
        open_image = Image.open("abrir.png")
        open_image = open_image.resize((20,15), Image.LANCZOS)

        save_image = Image.open("guardar.png")
        save_image = save_image.resize((20,15), Image.LANCZOS)

        undo_image = Image.open("deshacer.png")
        undo_image = undo_image.resize((20,15), Image.LANCZOS)

        redo_image = Image.open("rehacer.png")
        redo_image = redo_image.resize((20,15), Image.LANCZOS)

        exit_image = Image.open("salir.png")
        exit_image = exit_image.resize((20,15), Image.LANCZOS)

        # Convertir la imagen a un formato que tkinter pueda usar
        self.open_image_tk = ImageTk.PhotoImage(open_image)
        self.save_image_tk = ImageTk.PhotoImage(save_image)
        self.undo_image_tk = ImageTk.PhotoImage(undo_image)
        self.redo_image_tk = ImageTk.PhotoImage(redo_image)
        self.exit_image_tk = ImageTk.PhotoImage(exit_image)

        # Crear un frame para centrar los botones
        frame = tk.Frame(root)
        frame.pack(expand=True) 
        
        # Opciones de menú
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Abrir", command=self.open_file)
        file_menu.add_command(label="Guardar", command=self.save_file)

        # Botones en la barra de herramientas
        open_button = ttk.Button(frame, text="   Abrir", style="Custom.TButton", command=self.open_file)
        open_button.config(image=self.open_image_tk, compound=tk.LEFT, padding=(0,0))

        save_button = ttk.Button(frame, text="   Guardar",style="Custom.TButton", command=self.save_file)
        save_button.config(image=self.save_image_tk, compound=tk.LEFT, padding=(0,0))

        undo_button = ttk.Button(frame, text="   Deshacer", style="Custom.TButton", command=self.undo)
        undo_button.config(image=self.undo_image_tk, compound=tk.LEFT, padding=(0,0))

        redo_button = ttk.Button(frame, text="   Rehacer", style="Custom.TButton", command=self.redo)
        redo_button.config(image=self.redo_image_tk, compound=tk.LEFT, padding=(0,0))

        exit_button = ttk.Button(frame, text="   Salir", style="Custom.TButton", command=self.exit_application)
        exit_button.config(image=self.exit_image_tk, compound=tk.LEFT, padding=(0,0))

        # Asignar la imagen al boton
        open_button.image = self.open_image_tk
        save_button.image = self.save_image_tk
        undo_button.image = self.undo_image_tk
        redo_button.image = self.redo_image_tk
        exit_button.image = self.exit_image_tk

        open_button.grid(row=0, column=0, padx=10, pady=10)
        save_button.grid(row=0, column=1, padx=10, pady=10)
        undo_button.grid(row=0, column=2, padx=10, pady=10)
        redo_button.grid(row=0, column=3, padx=10, pady=10)
        exit_button.grid(row=0, column=4, padx=10, pady=10)

        # Botones en la barra de herramientas
        bold_button = ttk.Button(frame, text="Negrita", style="Custom.TButton", command=self.toggle_bold)
        italic_button = ttk.Button(frame, text="Cursiva", style="Custom.TButton", command=self.toggle_italic)
        underline_button = ttk.Button(frame, text="Subrayado", style="Custom.TButton", command=self.toggle_underline)
        

        bold_button.grid(row=1, column=0, padx=10, pady=10)
        italic_button.grid(row=1, column=1, padx=10, pady=10)
        underline_button.grid(row=1, column=2, padx=10, pady=10)
        

        # Crear el widget de área de texto con seguimiento de edición habilitado
        self.text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text_widget.config(font=("Arial", 22))
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.config(undo=True, autoseparators=True)  # Habilitar la funcionalidad de deshacer/rehacer


        
        # Guardar el contenido del área de texto para comparar si ha cambiado
        self.saved_text = ""


    def toggle_bold(self):
        try:
            # Obtener el texto seleccionado
            start_index = self.text_widget.index(tk.SEL_FIRST)
            end_index = self.text_widget.index(tk.SEL_LAST)

            if start_index and end_index:
                # Verificar si "bold" ya está en las etiquetas aplicadas
                tags = self.text_widget.tag_names(start_index)
                if "bold" in tags:
                    self.text_widget.tag_remove("bold", start_index, end_index)
                else:
                    # Aplicar la etiqueta "bold" al texto seleccionado
                    self.text_widget.tag_add("bold", start_index, end_index)
                    self.text_widget.tag_configure("bold", font=("Arial", 22, "bold"))
        except tk.TclError:
            tk.messagebox.showerror(title="Error", message="No se ha encontrado texto seleccionado")
    

    def toggle_italic(self):
        try:
            # Obtener el texto seleccionado
            start_index = self.text_widget.index(tk.SEL_FIRST)
            end_index = self.text_widget.index(tk.SEL_LAST)

            if start_index and end_index:
                # Verificar si "italic" ya está en las etiquetas aplicadas
                tags = self.text_widget.tag_names(start_index)
                if "italic" in tags:
                    self.text_widget.tag_remove("italic", start_index, end_index)
                else:
                # Aplicar la etiqueta "italic" al texto seleccionado
                    self.text_widget.tag_add("italic", start_index, end_index)
                    self.text_widget.tag_configure("italic", font=("Arial", 22, "italic"))
        except tk.TclError:
            tk.messagebox.showerror(title="Error", message="No se ha encontrado texto seleccionado")
                

    def toggle_underline(self):
        try:
        # Obtener el texto seleccionado
            start_index = self.text_widget.index(tk.SEL_FIRST)
            end_index = self.text_widget.index(tk.SEL_LAST)

            if start_index and end_index:
                # Verificar si "underline" ya está en las etiquetas aplicadas
                tags = self.text_widget.tag_names(start_index)
                if "underline" in tags:
                    self.text_widget.tag_remove("underline", start_index, end_index)
                else:
                # Aplicar la etiqueta "underline" al texto seleccionado
                    self.text_widget.tag_add("underline", start_index, end_index)
                    self.text_widget.tag_configure("underline", underline=True)
        except tk.TclError:
            tk.messagebox.showerror(title="Error", message="No se ha encontrado texto seleccionado")
                


    def exit_application(self):
        current_text = self.text_widget.get("1.0", tk.END)
        if current_text != self.saved_text:
            # Si el texto ha cambiado, preguntar si se desea guardar
            response = messagebox.askyesnocancel("Salir", "¿Desea guardar los cambios antes de salir?")
            if response is None:
                # Cancelar la acción de salir
                return
            elif response:
                # Guardar antes de salir
                self.save_file()
        # Cerrar la aplicación
        self.root.destroy()

    def open_file(self):
        # Abrir archivo y cargar contenido en el área de texto
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    text = file.read()
                    self.text_widget.delete("1.0", tk.END)
                    self.text_widget.insert(tk.END, text)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")

    def save_file(self):
        # Guardar contenido del área de texto en un archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text_widget.get("1.0", tk.END))  # Escribir el contenido en el archivo
                    self.saved_text = self.text_widget.get("1.0", tk.END)
                    
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

    def undo(self):
        # Deshacer la última acción en el área de texto
        try:
            self.text_widget.edit_undo()
        except Exception as e:
            pass

    def redo(self):
        # Rehacer la última acción deshecha en el área de texto
        try:
            self.text_widget.edit_redo()
        except Exception as e:
            pass

    

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_application)
    root.mainloop()