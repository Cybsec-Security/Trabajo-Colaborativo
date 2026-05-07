import tkinter as tk
from tkinter import ttk, messagebox
import abc
import datetime


# ==============================
# LOGS
# ==============================

def registrar_log(mensaje):
    with open("logs_sistema.txt", "a", encoding="utf-8") as archivo:
        tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        archivo.write(f"[{tiempo}] {mensaje}\n")


# ==============================
# EXCEPCIONES
# ==============================

class SistemaError(Exception):
    pass


class DatosInvalidosError(SistemaError):
    pass


class ServicioNoDisponibleError(SistemaError):
    pass


# ==============================
# CLASES ABSTRACTAS
# ==============================

class EntidadSistema(abc.ABC):

    @abc.abstractmethod
    def obtener_descripcion(self):
        pass


class Servicio(abc.ABC):

    def __init__(self, nombre_servicio, precio_base):
        self.nombre_servicio = nombre_servicio
        self.precio_base = precio_base

    @abc.abstractmethod
    def calcular_costo(self, duracion):
        pass


# ==============================
# CLIENTE
# ==============================

class Cliente(EntidadSistema):

    def __init__(self, id_cliente, nombre, email):
        self.__id = id_cliente
        self.__nombre = nombre
        self.email = email

        registrar_log(f"Cliente creado: {nombre}")

    @property
    def nombre(self):
        return self.__nombre

    def obtener_descripcion(self):
        return f"{self.__nombre} - ID {self.__id}"


# ==============================
# SERVICIOS
# ==============================

class ReservaSala(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return (self.precio_base * duracion) * 1.19


class AlquilerEquipo(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return self.precio_base * duracion


class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, duracion):

        if duracion <= 0:
            raise DatosInvalidosError(
                "La duración debe ser positiva"
            )

        return self.precio_base * duracion


# ==============================
# RESERVA
# ==============================

class Reserva:

    def __init__(self, cliente, servicio, duracion):

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def procesar_reserva(self):

        if self.duracion > 24:
            raise ServicioNoDisponibleError(
                "No se permiten reservas mayores a 24 horas"
            )

        costo = self.servicio.calcular_costo(
            self.duracion
        )

        self.estado = "Confirmada"

        registrar_log(
            f"Reserva confirmada: "
            f"{self.cliente.nombre}"
        )

        return costo


# ==============================
# INTERFAZ TKINTER
# ==============================

class SistemaReservasGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Sistema de Reservas FJ")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # SERVICIOS
        self.servicios = {
            "Sala de Conferencias": ReservaSala(
                "Sala de Conferencias",
                50
            ),

            "Laptop High-End": AlquilerEquipo(
                "Laptop High-End",
                20
            ),

            "Consultoría Senior": AsesoriaEspecializada(
                "Consultoría Senior",
                100
            )
        }

        self.crear_interfaz()

    # ==========================
    # INTERFAZ
    # ==========================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.root,
            text="SISTEMA DE RESERVAS",
            font=("Arial", 20, "bold")
        )

        titulo.pack(pady=15)

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # NOMBRE
        tk.Label(
            frame,
            text="Nombre:"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.entry_nombre = tk.Entry(
            frame,
            width=30
        )

        self.entry_nombre.grid(
            row=0,
            column=1
        )

        # EMAIL
        tk.Label(
            frame,
            text="Email:"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.entry_email = tk.Entry(
            frame,
            width=30
        )

        self.entry_email.grid(
            row=1,
            column=1
        )

        # SERVICIO
        tk.Label(
            frame,
            text="Servicio:"
        ).grid(row=2, column=0, padx=10, pady=10)

        self.combo_servicio = ttk.Combobox(
            frame,
            values=list(self.servicios.keys()),
            state="readonly",
            width=27
        )

        self.combo_servicio.grid(
            row=2,
            column=1
        )

        self.combo_servicio.current(0)

        # DURACIÓN
        tk.Label(
            frame,
            text="Duración (horas):"
        ).grid(row=3, column=0, padx=10, pady=10)

        self.entry_duracion = tk.Entry(
            frame,
            width=30
        )

        self.entry_duracion.grid(
            row=3,
            column=1
        )

        # BOTÓN
        btn = tk.Button(
            self.root,
            text="Procesar Reserva",
            font=("Arial", 12, "bold"),
            command=self.procesar_reserva,
            bg="#4CAF50",
            fg="white",
            width=20
        )

        btn.pack(pady=20)

        # ÁREA DE RESULTADOS
        self.texto = tk.Text(
            self.root,
            height=12,
            width=80
        )

        self.texto.pack(pady=10)

    # ==========================
    # PROCESAR
    # ==========================

    def procesar_reserva(self):

        try:

            nombre = self.entry_nombre.get()
            email = self.entry_email.get()
            servicio_nombre = self.combo_servicio.get()

            if not nombre or not email:
                raise DatosInvalidosError(
                    "Debe completar todos los campos"
                )

            duracion = float(
                self.entry_duracion.get()
            )

            servicio = self.servicios[
                servicio_nombre
            ]

            cliente = Cliente(
                1,
                nombre,
                email
            )

            reserva = Reserva(
                cliente,
                servicio,
                duracion
            )

            costo = reserva.procesar_reserva()

            mensaje = (
                f"\nRESERVA EXITOSA\n"
                f"Cliente: {nombre}\n"
                f"Servicio: {servicio_nombre}\n"
                f"Duración: {duracion} horas\n"
                f"Costo Total: ${costo:.2f}\n"
                f"Estado: {reserva.estado}\n"
                f"{'-'*50}\n"
            )

            self.texto.insert(
                tk.END,
                mensaje
            )

            self.texto.see(tk.END)

            messagebox.showinfo(
                "Éxito",
                "Reserva procesada correctamente"
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "La duración debe ser numérica"
            )

        except SistemaError as e:

            registrar_log(str(e))

            messagebox.showerror(
                "Error del Sistema",
                str(e)
            )

        except Exception as e:

            registrar_log(
                f"ERROR INESPERADO: {str(e)}"
            )

            messagebox.showerror(
                "Error",
                f"Ocurrió un error:\n{str(e)}"
            )


# ==============================
# EJECUCIÓN
# ==============================

if __name__ == "__main__":

    root = tk.Tk()

    app = SistemaReservasGUI(root)

    root.mainloop()