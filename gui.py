from candidatos import lista_candidatos
from Blockchain import Blockchain
from fastecdsa import keys, curve
from hashlib import sha256
from keyGenerator import gerar_chave
import wx
import wx.dataview as dv

#A seção eleitoral é fixa para esta urna
zoneSection = "007009"
#Cria uma nova blockchain
b_chain = Blockchain()
#Gera chave privada e publica iniciais
private_key, public_key = gerar_chave()

#Janela principal do programa.
class MainFrame(wx.Frame):    
    def __init__(self):
        self.candidato_nome = ""
        self.lista_candidatos_aberta = False
        self.lista_votos_aberta = False
        super().__init__(parent=None, title='Urna')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.CreateStatusBar()

        #Configura a barra de menus no topo da janela principal
        menu_bar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(101, "Lista", "Lista todos os candidatos")
        menu1.Append(102, "Votos", "Lista quantos votos cada candidato tem")
        menu_bar.Append(menu1, "Info")
        self.Bind(wx.EVT_MENU, self.on_press_check, id=101)
        self.Bind(wx.EVT_MENU, self.on_press_get_votes, id=102)
        self.SetMenuBar(menu_bar)
        
        #Cria os componentes que serão mostrados na janela principal
        self.text_ctrl = wx.TextCtrl(panel)
        self.name_static_text = wx.StaticText(panel, style=wx.ALIGN_CENTRE_HORIZONTAL | wx.ST_NO_AUTORESIZE)
        confirm_btn = wx.Button(panel, label="Confirmar")
        confirm_btn.Bind(wx.EVT_BUTTON, self.on_press_confirm)
        get_key_btn = wx.Button(panel, label="Gerar chaves")
        get_key_btn.Bind(wx.EVT_BUTTON, self.on_press_get_key)

        #Adiciona os componentes criados à interface
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        my_sizer.Add(self.name_static_text, 1, wx.ALL | wx.EXPAND, 5)
        my_sizer.Add(confirm_btn, 0, wx.ALL | wx.CENTER, 5)
        my_sizer.Add(get_key_btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(my_sizer)
        self.Show()
    
    #Chamada quando aperta o botão "Gerar chaves"
    #Gera novas chaves pública e privada.
    def on_press_get_key(self, event):
        global private_key
        global public_key
        private_key, public_key = gerar_chave()
        print("Chave privada: ")
        print(private_key)
        print("Chave pública: ")
        print(public_key)

    #Chamada quando aperta o botão "Confirmar"
    #Confirma o voto em um candidato, se apertado duas vezes com o código inserido
    def on_press_confirm(self, event):
        codigo = self.text_ctrl.GetValue()
        candidato_nome = ""
        for candidato in lista_candidatos:
            if codigo == candidato[2]:
                candidato_nome = candidato[1]
                break
        if candidato_nome == "":
            self.name_static_text.SetLabel("Candidato Inexistente")
        else:
            if self.candidato_nome == candidato_nome:
                self.name_static_text.SetLabel("Confirmando voto")
                print("chave publica:")
                print(public_key)
                print("chave privada:")
                print(private_key)
                #Cria o voto na Block Chain
                vote = b_chain.createVote(public_key.__str__(), candidato_nome, zoneSection, private_key)
                #Checa se o voto ocorreu corretamente
                if not vote:
                    self.name_static_text.SetLabel("Houve algum erro. Voto não computado")
                else:
                    self.name_static_text.SetLabel("Voto confirmado!")
                b_chain.minePendingVotes()
                self.candidato_nome = ""
            else:
                self.candidato_nome = candidato_nome
                self.name_static_text.SetLabel("Pressione novamente para confirmar voto para\n" + candidato_nome)

    #Chamado ao clicar na opção "Lista" na barra de menus
    #Lista todos os candidatos possíveis e suas informações
    def on_press_check(self, event):
        if not self.lista_candidatos_aberta:
            CandidatosFrame(self)
        else:
            print("Janela já aberta!")

    #Chamado ao clicar na opção "Votos" na barra de menus
    #Lista os votos de cada candidato
    def on_press_get_votes(self, event):
        if not self.lista_votos_aberta:
            candidatos_votos_lista = []
            #Calcula a quantidade de votos para cada candidato, e manda a lista calculada como parâmetro
            for candidato in lista_candidatos:
                candidato_voto = [str(b_chain.getVotes(candidato[1])), candidato[1]]
                candidatos_votos_lista.append(candidato_voto)
            votosFrame(self, candidatos_votos_lista)
        else:
            print("Janela já aberta!")

#Janela que mostra os candidatos e quantos votos cada um possui
class votosFrame(wx.Frame):
    def __init__(self, mainFrame, candidatos_votos_lista):
        super().__init__(parent=None, title = "Lista de Votos")
        self.mainFrame = mainFrame
        self.mainFrame.lista_votos_aberta = True
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = wx.Panel(self)
        self.dv_list = dv.DataViewListCtrl(self.panel)
        
        self.dv_list.AppendTextColumn("Votos", width=40)
        self.dv_list.AppendTextColumn("Nome", width=170)

        #Adiciona os votos calculados à lista
        for candidato in candidatos_votos_lista:
            self.dv_list.AppendItem(candidato)
        
        self.panel.Sizer = wx.BoxSizer()
        self.panel.Sizer.Add(self.dv_list, 1, wx.EXPAND)
        self.Show()


    def on_close(self, event):
        self.mainFrame.lista_votos_aberta = False
        self.Destroy()

#Janela que lista todos os candidatos e suas informações
class CandidatosFrame(wx.Frame):
    def __init__(self, mainFrame):
        super().__init__(parent=None, title = "Lista de Candidatos")
        self.mainFrame = mainFrame
        mainFrame.lista_candidatos_aberta = True
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.panel = wx.Panel(self)
        self.dv_list = dv.DataViewListCtrl(self.panel)

        self.dv_list.AppendTextColumn("id", width=40)
        self.dv_list.AppendTextColumn("Nome", width=170)
        self.dv_list.AppendTextColumn("Código", width=100)
        self.dv_list.AppendTextColumn("Partido", width=60)

        for candidato in lista_candidatos:
            self.dv_list.AppendItem(candidato)

        self.panel.Sizer = wx.BoxSizer()
        self.panel.Sizer.Add(self.dv_list, 1, wx.EXPAND)
        self.Show()
    
    def on_close(self, event):
        self.mainFrame.lista_candidatos_aberta = False
        self.Destroy()


def start_gui():
    app = wx.App()
    frame = MainFrame()
    app.MainLoop()