import socket
import threading
import sys
import tkinter as tk
from tkinter import ttk
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = int(input("Please enter port to connect to >> "))

style = ttk.Style()
style.configure("TButton", foreground = "white", background = "#202020", relief = "flat", focusthickness = 0)
style.configure("TEntry", foreground = "white", fieldbackground = "#202020", borderwidth = 0, relief = "flat")
style.configure("TFrame", background = "#404040")
style.configure("Vertical.TScrollbar", background = "#202020", troughcolor = "#404040", relief = "flat", troughrelief = "flat", borderwidth = 0, arrowcolor="white")
style.configure("TLabel", background = "#404040", foreground = "white")
style.configure("Dark.TFrame", background = "#202020")
style.map("TButton", foreground=[("pressed", "white"), ("active", "white")], background=[("pressed", "#505050"), ("active", "#404040")])
style.map("Vertical.TScrollbar", background=[("pressed", "#202020"), ("active", "#202020")])

field_bg = "#404040"
field_fg = "#f0f0f0"

client.connect((host, port))

# Main application class
class Application(tk.Frame):
	def __init__(self, master=None):
		super(Application, self).__init__(master)

		self.pack(expand=1, fill="both")

		self.control_frame = ttk.Frame(self, style="Dark.TFrame")
		self.control_frame.pack(fill="x")

		self.message_frame = ttk.Frame(self)
		self.message_frame.pack(expand=1, fill="both")

		self.send_frame = ttk.Frame(self, style="Dark.TFrame")
		self.send_frame.pack(fill="x", pady=0, padx=0)

		self.message_box = tk.Text(self.message_frame, wrap=tk.WORD, bg=field_bg, fg=field_fg, highlightbackground=field_bg, relief=tk.FLAT, state="disabled")
		self.scrollbar = ttk.Scrollbar(self.message_frame, command=self.message_box.yview)
		self.scrollbar.pack(side="right", fill="y", pady=0, padx=0)
		self.message_box.pack(fill="both", expand=1, pady=0, padx=0)

		self.message_box["yscrollcommand"] = self.scrollbar.set

		self.send_field = ttk.Entry(self.send_frame)
		self.send_field.pack(side="left", pady=0, padx=0, expand=1, fill="x")

		ttk.Button(self.send_frame, command=self.send_messages, text="Send").pack(side="right", pady=0, padx=0)

		ttk.Button(self.control_frame, command=self.quit, text="Quit").pack(side="right", pady=0, padx=0)

		ttk.Button(self.control_frame, command=self.set_name, text="Set Name").pack(side="right", pady=0, padx=0)

		self.master.bind("<Return>", self.send_messages)

	def quit(self):
		data = {}
		data["QUIT"] = 1
		client.send(json.dumps(data).encode("utf8"))

		del data
		self.master.destroy()
		sys.exit()

	def send_messages(self, event=None):
		data = {}
		data["TMSG"] = self.send_field.get()
		if data["TMSG"] != "":
			client.send(json.dumps(data).encode("utf8"))

		self.send_field.delete(0, tk.END)
		del data

	def set_name(self):
		def set():
			data = {}
			data["SINF"] = ["NAME", self.name_entry.get()]
			client.send(json.dumps(data).encode("utf8"))

			del data
			self.name_window.destroy()

		self.name_window = tk.Toplevel(bg=field_bg)
		self.name_window.attributes("-topmost", "true")
		self.name_window.resizable(False, False)

		self.name_entry = ttk.Entry(self.name_window)
		self.name_entry.grid(pady=0, padx=0)
		ttk.Button(self.name_window, text="Submit", command=set).grid(pady=0, padx=0)

app = Application()

def receive_data():
	while True:
		data = client.recv(1024)
		if data != b"":
			data = json.loads(data)
			sys.stdout.write(data["TMSG"] + "\n")

			app.message_box.configure(state="normal")
			app.message_box.insert("end", data["TMSG"].strip() + "\n")
			app.message_box.see("end")
			app.message_box.configure(state="disabled")

		del data


receiver = threading.Thread(target=receive_data, daemon=True)
receiver.start()

app.mainloop()
