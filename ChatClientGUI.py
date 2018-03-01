import socket
import threading
import sys
import tkinter as tk
import json

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()

port = 9999

client.connect((host, port))

class Application(tk.Frame):
	def __init__(self, master=None):
		super(Application, self).__init__(master)

		self.pack(expand=1, fill='both')

		self.control_frame = tk.Frame(self)
		self.control_frame.pack(fill='x')

		self.message_frame = tk.Frame(self)
		self.message_frame.pack(expand=1, fill='both')

		self.send_frame = tk.Frame(self)
		self.send_frame.pack(fill='x')

		self.message_box = tk.Text(self.message_frame, wrap=tk.WORD)
		self.message_box.pack(expand=1, fill='both', pady=2, padx=4)

		self.send_field = tk.Entry(self.send_frame)
		self.send_field.pack(side='left', pady=2, padx=4, expand=1, fill='x')

		tk.Button(self.send_frame, command=self.send_messages, text="Send").pack(side='right', pady=2, padx=4)

		tk.Button(self.control_frame, command=self.quit, text="Quit").pack(side='right', pady=2, padx=4)

		self.master.bind('<Return>', self.send_messages)

	def quit(self):
		data = {}
		data["QUIT"] = 1
		client.send(json.dumps(data).encode("utf8"))

		del data
		self.master.destroy()
		sys.exit()

	def send_messages(self, event=None):
		data = {}
		data["MSG"] = self.send_field.get()
		client.send(json.dumps(data).encode("utf8"))

		self.send_field.delete(0, tk.END)
		del data

app = Application()

def receive_data():
	while True:
		data = json.loads(client.recv(1024))
		sys.stdout.write(data["MSG"] + "\n")
		app.message_box.insert("end", data["MSG"] + "\n")

receiver = threading.Thread(target=receive_data, daemon=True)
receiver.start()

app.mainloop()
