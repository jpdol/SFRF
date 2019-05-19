import SFRF_interface as interface
import sqlite3
import SFRF_backend as back

if __name__ == "__main__":
	back.criar_conexao()
	app = interface.SFRFapp()
	app.mainloop()
