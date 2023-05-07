import customtkinter as ctk
from ..net import PianoClient
from tkinter import messagebox as msg
import re


def start_gui_client():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = ClientApp()
    app.run()


class ClientApp(ctk.CTk):

    def __init__(self, connect_callback: callable = None):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.width = 400
        self.height = 300
        self.client = None
        self.on_connect = connect_callback

        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.title("Client Connect")
        self.iconbitmap("resources/pictures/electric.ico")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        frame = ctk.CTkFrame(master=self)
        frame.pack(pady=20, padx=40, fill='both', expand=True)

        self.label_connect = ctk.CTkLabel(master=frame, text='Connect to Server', font=('Ariel', 25))
        self.ip_entry = ctk.CTkEntry(master=frame, placeholder_text="IP")
        self.port_entry = ctk.CTkEntry(master=frame, placeholder_text="Port")
        self.button = ctk.CTkButton(master=frame, text='Connect', command=self.connect)

        self.bind('<KeyPress>', self.on_key_press)
        self.ip_entry.bind('<Tab>', self.focus_next_widget)
        self.port_entry.bind('<Tab>', self.focus_next_widget)

        self.label_connect.pack(pady=12, padx=10)
        self.ip_entry.pack(pady=12, padx=10)
        self.port_entry.pack(pady=12, padx=10)
        self.button.pack(pady=12, padx=10)

    def run(self):
        self.mainloop()

    def connect(self):
        try:
            if not re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", self.getIP()):
                msg.showerror("Error", "Not a valid IP format")
                raise
            elif not (0 <= self.getPort() < 65535):
                msg.showerror("Error", "Port number must be between 0 and 65535")
                raise
            self.client = PianoClient(self.getIP(), self.getPort())
            self.client.connect()
            self.destroy()
            print("opening midi window")
            # TODO: open midi gui
        except ConnectionRefusedError as e:
            msg.showerror("Error", f"Couldn't connect to server\ncheck ip and port again (connection refused)")

    def getIP(self) -> str:
        return self.ip_entry.get()

    def getPort(self) -> int:
        return int(self.port_entry.get())

    def on_key_press(self, event):
        if event.keysym == 'Return' and self.getIP() and self.getPort():
            self.button.invoke()

    def focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def on_closing(self) -> None:
        if msg.askokcancel("Quit", "Are you sure you want to exit?"):
            self.destroy()


if __name__ == '__main__':
    start_gui_client()
