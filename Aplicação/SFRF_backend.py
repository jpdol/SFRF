from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename
import datetime
from datetime import datetime, timedelta
import SFRF_interface as inter
import sqlite3
import tkinter.font as tkFont
import tkinter.ttk as ttk

#Chama a função que faz a conexão com o banco de dados 
def criar_conexao():
	global con
	con = Conexao()

class Colaborador():
	def __init__(self, nome="", dtNasc="", setor="", funcao="", ch="", dtIngresso="", status="", cpf="", senha=""):
		self.nome = nome
		self.dtNasc = dtNasc
		self.setor = setor
		self.funcao = funcao
		self.ch = ch
		self.dtIngresso = dtIngresso
		self.status = status
		self.cpf = cpf
		self.senha = senha

#Cria banco de dados e tabelas
#Cria conexão com o banco de dados
class Conexao():
	def __init__(self):
		self.conexao = sqlite3.connect(r"SFRF.db")
		self.cursor = self.conexao.cursor()
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Setor (Nome VARCHAR(45), Sigla VARCHAR(45), Logo BLOB, Image_type VARCHAR(3), PRIMARY KEY(Nome, Sigla))")
		self.cursor.execute("CREATE TABLE IF NOT EXISTS Colaborador (Nome VARCHAR(45), DtNasc DATE, Setor VARCHAR(45), Funcao VARCHAR(45), CH INT, DtIngresso DATE, DtDesligamento DATE, Status VARCHAR(45), cpf VARCHAR(11), Foto BLOB, Image_type VARCHAR(3), Senha VARCHAR(45) NOT NULL, PRIMARY KEY(cpf))")
		self.cursor.execute("INSERT OR IGNORE INTO Setor (Nome, Sigla) VALUES(?,?)", ("Administração", "ADM"))
		self.conexao.commit()

#Realiza o cadastro do colaborador
def cadastrar_colaborador(nome, DtNasc, Setor, Funcao, CH, DtIngresso, status, cpf, senha, confirma_senha, foto, event=None):
	if senha.get() != confirma_senha.get():
		inter.pop_up("ERROR", "Confirme sua Senha!")
	elif(not(validar_cpf(cpf.get()))):
		inter.pop_up("ERROR", "CPF inválido")
	elif(not(validar_data(DtNasc.get())) or not(validar_data(DtIngresso.get()))):
		inter.pop_up("ERROR", "Data inválida")
	else:
		cursor = con.cursor
		conexao = con.conexao

		try:
			if (Setor.get() != "*Selecione o setor*") or (Funcao.get() in ['ADM', 'Coordenador Geral']):

				setor = ""
				if(Funcao.get() in ['ADM', 'Coordenador Geral']):
					setor = "Administração"
				else:
					setor = Setor.get()

				if foto.get() != "":
					file_type = ImageMethods.get_file_type(foto.get())
					file_binary = ImageMethods.get_binary(foto.get())
					cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Setor, Funcao, CH, DtIngresso, Status, cpf, Foto, Image_type, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), setor, Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), file_binary, file_type, senha.get()))
				else:
					cursor.execute("INSERT INTO Colaborador (Nome, DtNasc, Setor, Funcao, CH, DtIngresso, Status, cpf, Foto, Image_type, Senha) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (nome.get(), DtNasc.get(), setor, Funcao.get(), CH.get(), DtIngresso.get(), status.get(), cpf.get(), None, None, senha.get()))
				conexao.commit()
				return True
			else:
				inter.pop_up("ERROR", "Cadastro Inválido!")
				return False	
		except Exception:
			inter.pop_up("ERROR", "Cadastro Inválido")
			return False
	return False

def atualizar_cadastro_colaborador(nome, DtNasc, Setor, Funcao, CH, DtIngresso, status, senha, confirma_senha, foto, cpf_colab):
	if senha.get()!=confirma_senha.get():
		inter.pop_up("ERROR", "Confirme sua Senha!")
	else:
		cursor = con.cursor
		conexao = con.conexao

		try:
			if foto.get() != "":
				file_type = ImageMethods.get_file_type(foto.get())
				file_binary = ImageMethods.get_binary(foto.get())
				cursor.execute('''UPDATE Colaborador 
					SET Nome = (?), DtNasc = (?), Setor = (?), Funcao=(?), CH=(?), DtIngresso=(?), Status=(?), Foto=(?), Image_type = (?), Senha=(?) WHERE cpf = (?) ''', (nome.get(), DtNasc.get(), Setor.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), file_binary, file_type, senha.get(), cpf_colab))
			else:
				cursor.execute('''UPDATE Colaborador 
					SET Nome=(?), DtNasc=(?), Setor=(?), Funcao=(?), CH=(?), DtIngresso=(?), Status=(?), Senha=(?) WHERE cpf = (?) ''', (nome.get(), DtNasc.get(), Setor.get(), Funcao.get(), CH.get(), DtIngresso.get(), status.get(), senha.get(), cpf_colab))
			conexao.commit()
			return True
		except:
			inter.pop_up("ERROR", "Cadastro Inválido")
			return False
	return False

def atualizar_cadastro_setor(nome, sigla, logo_path):
	if logo_path.get() != "":
		cursor = con.cursor
		conexao = con.conexao
		try:
			file_type = ImageMethods.get_file_type(logo_path.get())
			file_binary = ImageMethods.get_binary(logo_path.get())
			cursor.execute('''UPDATE Setor 
					SET Logo = (?), Image_type = (?) WHERE Nome = (?) and Sigla = (?)''', (file_binary, file_type, nome.get(), sigla.get()))
			conexao.commit()

			inter.pop_up("Sucesso", "Dados Atualizados")
			return True

		except Exception as e:
			print(e)
			inter.pop_up("ERROR", "O caminho informado é inválido")
			return False
	else:
		return False

def cadastrar_setor(nome, sigla, logo):
	cursor = con.cursor
	conexao = con.conexao
	if nome.get() != "" and sigla.get()!="":
		try:
			if logo.get() != "":
				file_type = ImageMethods.get_file_type(logo.get())
				file_binary = ImageMethods.get_binary(logo.get())
				cursor.execute("INSERT INTO Setor VALUES (?, ?, ?, ?)", (nome.get(), sigla.get(), file_binary, file_type))
			else:
				cursor.execute("INSERT INTO Setor VALUES (?, ?, ?, ?)", (nome.get(), sigla.get(), None, None))

			conexao.commit()
			return True
		except:
			inter.pop_up("ERROR", "Cadastro Inválido")
	else:
		inter.pop_up("ERROR", "Cadastro Inválido")
	return False

def retorna_lista_colab(setor):
	cursor = con.cursor
	if setor == 'Não Ativos':
		cursor.execute("SELECT Nome FROM Colaborador WHERE Status='Não Ativo'")
	else:
		cursor.execute("SELECT Nome FROM Colaborador WHERE Setor = '%s' and Status='Ativo' or Status='Afastado' ORDER BY Nome"%setor)
	lista = []
	for nome in cursor.fetchall():
		lista.append(str(nome[0]))
	return lista

def retorna_lista_setor():
	cursor = con.cursor
	cursor.execute('''SELECT Nome
				   FROM Setor''')
	lista = []
	for nome in cursor.fetchall():
		lista.append(str(nome[0]))
	return lista

def retorna_dados_setor(setor):
	cursor = con.cursor
	try:	
		cursor.execute("SELECT Nome,Sigla FROM Setor WHERE Nome='%s'"%(setor))
		return cursor.fetchall()[0]
	except:
		pop_up("ERROR", "Setor não encontrado!")

def retorna_colab(nome, setor):
	cursor = con.cursor
	if type(nome) != str:
		if setor == 'Não Ativos':
			cursor.execute("SELECT * FROM Colaborador WHERE Nome = '%s' and Status = 'Não Ativo'"%nome.get())
		else:
			cursor.execute("SELECT * FROM Colaborador WHERE Nome = '%s' and Setor='%s'"%(nome.get(), setor))
	else:
		if setor == 'Não Ativos':
			cursor.execute("SELECT * FROM Colaborador WHERE Nome = '%s' and Status = 'Não Ativo'"%nome)
		else:
			cursor.execute("SELECT * FROM Colaborador WHERE Nome = '%s' and Setor='%s'"%(nome, setor))

	lista = cursor.fetchall()
	tupla = lista[0]
	colab = Colaborador(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[7], tupla[8], tupla[11])
	return colab

def retorna_user(cpf):
	cursor = con.cursor
	cursor.execute("SELECT * FROM Colaborador WHERE cpf = '%s'"%cpf)
	lista = cursor.fetchall()
	tupla = lista[0]
	colab = Colaborador(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4], tupla[5], tupla[7], tupla[8], tupla[11])
	return colab

def retorna_objeto_date(data):
	data_hora = data.split(" ")
	data = data_hora[0].split("/")
	hora = data_hora[1].split(":")
	date = datetime(int(data[0]),int(data[1]),int(data[2]), int(hora[0]),int(hora[1]),int(hora[2]))
	return date

class ImageMethods():
	# Abre uma caixa de diálogo para o usuário informar o caminho da imagem
	@staticmethod
	def get_path(line_path):
		tk_dialog = Tk()
		tk_dialog.withdraw()
		file_types=[('PNG file',"*.png"), ('JPG file', "*.jpg")]
		file_name = askopenfilename(filetypes=file_types, title="Selecione o logo")
		line_path.set(file_name)
		tk_dialog.destroy()

	# Retorna uma imagem representada por binários
	@staticmethod
	def get_binary(image_path):
		binary = ''
		with open(image_path, 'rb') as image:
			binary = image.read()
		return binary

	@staticmethod
	def get_file_type(image_path):
		file_type = ""
		for i in range(-3,0):
			file_type = file_type + image_path[i]
		return  (file_type)

def retorna_data():
	now = datetime.now()
	
	dia = str(now.day)
	if len(dia)<2:
		dia = '0'+dia
	
	mes = str(now.month)
	if len(mes)<2:
		mes = '0'+mes
	
	ano = str(now.year)
	
	data = ano+'/'+mes+'/'+dia
	
	return data

# Algoritmo normal para validar cpf 
def validar_cpf(cpf):
	try:
		if cpf.isnumeric() and (len(cpf) == 11):
			igual = True
			for i in range(1,11):
				if cpf[i] != cpf[i-1]:	
					igual = False
			if (igual):
				return False

			cpf_soma = 0

			for i in range(0, 9):
				cpf_soma = cpf_soma + int(cpf[i])*(10-i)

			if ((cpf_soma*10)%11 == int(cpf[9])) or ((cpf_soma*10)%11 == 10 and int(cpf[9]) == 0):
				cpf_soma = 0
				for i in range(0, 10):
					cpf_soma = cpf_soma + int(cpf[i])*(11-i)

				if ((cpf_soma*10)%11 == int(cpf[10])) or ((cpf_soma*10)%11 == 10 and int(cpf[10]) == 0):
					return True
				
			else:
				return False
		return False
	except:
		return False

def validar_data(data):
	try:
		datetime.strptime(data, '%d/%m/%Y')
		return True
	except Exception as e:
		return False

# Retorna uma lista de tuplas com o histórico do colaborador
def validar_chamada_historico(setor_, mes, ano, tipo):
	setor, mes, ano = setor_.get(), mes.get(), ano.get()

	if setor != "*Selecione o setor*":
		try:
			cursor = con.cursor
			dict_mes = {'Janeiro': '01','Fevereiro': '02','Março': '03','Abril': '04','Maio': '05','Junho': '06',
						'Julho': '07','Agosto': '08','Setembro': '09','Outubro': '10','Novembro': '11','Dezembro': '12'}

			date = ano+"/"+dict_mes[mes]

			if setor == "Não Ativos":
				cursor.execute("SELECT cpf,Nome From Colaborador WHERE Status = 'Não Ativo'")
			else:
				cursor.execute("SELECT cpf,Nome From Colaborador WHERE Setor = '%s' ORDER BY Nome"%setor)

			lista_tuplas = []
			cpf_nome_colab = cursor.fetchall()

			if len(cpf_nome_colab) == 0:
				inter.pop_up("Atenção", "Não há membros neste setor")
				return False
			# Histoóio resumido
			if tipo=='r':
				for colab in cpf_nome_colab:
					counter = timedelta()
					cursor.execute("SELECT entrada, saida FROM Frequencia WHERE entrada LIKE ? and cpf = ? and saida IS NOT NULL",((date+'%', colab[0])))
					for frequencia in cursor.fetchall():
						entrada = retorna_objeto_date(frequencia[0])
						saida = retorna_objeto_date(frequencia[1])
						counter += (saida-entrada)

					tupla = (colab[1], str(counter))
					lista_tuplas.append(tupla)

			# Histórico detalhado
			elif tipo=='d':
				dias = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20"
				,"21","22","23","24","25","26","27","28","29","30","31"]
				
				for dia in dias:
					data_com_dia = date+"/"+ dia
					linha = dia+" de "+mes+" de "+ano
					if setor != "Não Ativos":
						cursor.execute('''SELECT Nome, entrada, saida
										  FROM Colaborador as C, Frequencia as F
										  WHERE C.Setor = ? and C.cpf == F.cpf and  C.Status != "Não Ativo" and F.entrada LIKE ? and F.saida IS NOT NULL 
										  ORDER BY Nome''',(setor, data_com_dia+"%"))
					else:
						cursor.execute('''SELECT Nome, entrada, saida
										  FROM Colaborador as C, Frequencia as F
										  WHERE C.cpf == F.cpf and C.Status = "Não Ativo" and F.entrada LIKE ? and F.saida IS NOT NULL 
										  ORDER BY Nome''',(data_com_dia+"%",))
					frequencias = cursor.fetchall()
					
					if frequencias:		
						lista_tuplas.append(("__________________",linha,"__________________"))

						for frequencia in frequencias:
							tupla = (frequencia[0], frequencia[1],frequencia[2])
							lista_tuplas.append(tupla)
				
			return lista_tuplas
		except:
			return False

	else:
		inter.pop_up("ERROR", "Setor inválido!")
		return False

def validar_login(login, senha, event=None):
	
	if (login.get() != "") and (senha.get() != ""):
		try:
			colab = retorna_user(login.get())
			# Só é possível logar se status do caloborador for "Ativo"
			if (colab.senha == senha.get()) and (colab.status == "Ativo") and (colab.funcao != "Funcionario"):
				return colab

			else:
				# Colobarador com a função "funcionario" não pode logar no sistema
				if(colab.funcao == "Funcionario"):
					inter.pop_up("ERROR", "Usuário sem permissão de acesso!")
					return None
				inter.pop_up("ERROR", "Login ou Senha Inválida")
				return None

		except Exception as e:
			inter.pop_up("ERROR", "Login ou Senha Inválida")
			return None

	else:
		inter.pop_up("ERROR", "Login ou Senha Inválida")
		return None

def excluir_colaborador(cpf, setor):
	try:
		cursor = con.cursor

		#Desativa o Colaborador
		cursor.execute("UPDATE Colaborador SET Status = 'Não Ativo' WHERE cpf = (?)", (cpf,))
		con.conexao.commit()
		return True	
	except Exception as e:
		inter.pop_up("ERROR", "Não foi possível remover o colaborador.")
		return False

def excluir_setor(nome, sigla):
	# Retorna lista de colaboradores no setor
	lista_colab = retorna_lista_colab(nome)

	# Só é possível excluir o setor se ele não tiver mais colaboradores
	if len(lista_colab) == 0:
		try:
			cursor = con.cursor
			cursor.execute("DELETE FROM Setor WHERE Nome = '%s'"%nome)
			con.conexao.commit()
			return True
		except:
			inter.pop_up("ERROR", "Não foi possível remover o setor")
	else:
		inter.pop_up("Error", "O setor deve estar vazio para ser removido")
		return False
		
def validar_consulta(setor):
	if setor.get() != "" and setor.get() != "*Selecione o setor*":
		return True
	else:
		inter.pop_up("ERROR", "Consulta Inválida")
		return False

def validar_consulta_2(nome_colab, setor):
	try:
		colab = retorna_colab(nome_colab, setor)
		return True
	except:
		inter.pop_up("ERROR", "Consulta Inválida")
		return False

def retorna_data_sem_hora(data_str):
	split1 = data_str.split(" ")
	return split1[0]

def retorna_dia(data_str):
	split1 = data_str.split(" ")
	split2 = split1[0]
	data = split2.split("/")
	return data[2]

def retorna_hora(data_str):
	split1 = data_str.split(" ")
	return split1[1]

class McListBox(object):
	def __init__(self, container_o, header, lista):
		self.tree = None
		self._setup_widgets(container_o, header)
		self._build_tree(header, lista)

	def _setup_widgets(self,container_o, header):
		self.container = ttk.Frame(container_o)
		self.container.pack(fill='both', expand=True)
		self.tree = ttk.Treeview(columns=header, show="headings")
		vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=self.container)
		vsb.grid(column=1, row=0, sticky='ns', in_=self.container)
		hsb.grid(column=0, row=1, sticky='ew', in_=self.container)
		self.container.grid_columnconfigure(0, weight=1)
		self.container.grid_rowconfigure(0, weight=1)
	def _build_tree(self, header, lista):
		for col in header:
			self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
			self.tree.column(col, width=tkFont.Font().measure(col.title()))
		for item in lista:
			self.tree.insert('', 'end', values=item)
			for ix, val in enumerate(item):
				col_w = tkFont.Font().measure(val)
				if self.tree.column(header[ix],width=None)<col_w:
					self.tree.column(header[ix], width=col_w)

def sortby(tree, col, descending):
	data = [(tree.set(child, col), child) \
		for child in tree.get_children('')]
	data.sort(reverse=descending)
	for ix, item in enumerate(data):
		tree.move(item[1], '', ix)
	tree.heading(col, command=lambda col=col: sortby(tree, col, \
int(not descending)))