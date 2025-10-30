import ui
import globalPluginHandler
import wx
import random
import winsound
import os

from .. import BlindGame


class OpcaoDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Escolha par ou ímpar"):
        super(OpcaoDialog, self).__init__(parent, id, title, size=(300, 200))
        self.escolha = None
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Escolha uma opção")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        self.btnPar = wx.Button(self, label="Par")
        vbox.Add(self.btnPar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnImpar = wx.Button(self, label="Ímpar")
        vbox.Add(self.btnImpar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.SetSizer(vbox)
        self.btnPar.Bind(wx.EVT_BUTTON, self.on_par)
        self.btnImpar.Bind(wx.EVT_BUTTON, self.on_impar)

    def on_par(self, event):
        self.escolha = "par"
        self.EndModal(wx.ID_OK)

    def on_impar(self, event):
        self.escolha = "impar"
        self.EndModal(wx.ID_OK)

class ResultadoDialog(wx.Dialog):
    def __init__(self, parent, mensagem):
        super(ResultadoDialog, self).__init__(parent, title="Resultado", size=(300, 200))
        self.mensagem = mensagem
        self.InitUI()
        self.result = None

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        texto = wx.StaticText(self, label=self.mensagem)
        vbox.Add(texto, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        btnJogarNovamente = wx.Button(self, label="Jogar Novamente")
        btnVoltarMenu = wx.Button(self, label="Voltar ao Menu")
        btnSair = wx.Button(self, label="Sair")
        vbox.Add(btnJogarNovamente, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btnVoltarMenu, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)
        vbox.Add(btnSair, flag=wx.EXPAND | wx.ALL, border=10)
        btnJogarNovamente.Bind(wx.EVT_BUTTON, self.on_jogar_novamente)
        btnVoltarMenu.Bind(wx.EVT_BUTTON, self.on_voltar_menu)
        btnSair.Bind(wx.EVT_BUTTON, self.on_sair)
        self.SetSizer(vbox)

    def on_jogar_novamente(self, event):
        self.result = "jogar_novamente"
        self.EndModal(wx.ID_OK)

    def on_voltar_menu(self, event):
        self.result = "voltar_menu"
        self.EndModal(wx.ID_OK)

    def on_sair(self, event):
        self.result = "sair"
        self.EndModal(wx.ID_OK)

class ParOrImpar(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.tocarSom("trilha inicial.wav")
        self.maquina = random.randint(0, 10)
        self.isPar = None
        wx.CallLater(0, self.selecionaOpcao)

    def selecionaOpcao(self):
        dlg = OpcaoDialog(None)
        if dlg.ShowModal() == wx.ID_OK and dlg.escolha is not None:
            self.escolha = dlg.escolha
            if self.escolha == "par":
                self.isPar = True
                self.pararSom()
                self.tocarSom("trilha inicial.wav")
                wx.CallLater(4600, lambda: None)
            elif self.escolha == "impar":
                self.isPar = False
                self.pararSom()
                self.tocarSom("trilha inicial.wav")
                wx.CallLater(4800, lambda: None)
            self.solicitaJogada()

    def solicitaJogada(self):
        with wx.TextEntryDialog(None, "Escolha um número!", "Sua jogada") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                entrada = dlg.GetValue()
                if self.validarEntrada(entrada):
                    jogador = int(entrada)
                    self.calculaResultado(jogador)
                else:
                    wx.MessageBox("Digite uma opção válida (número)!")
                    wx.CallAfter(self.solicitaJogada)

    def validarEntrada(self, entrada):
        return entrada.isdigit()

    def calculaResultado(self, jogador):
        soma = jogador + self.maquina
        mensagem = ""
        venceu = False
        if self.isPar and soma % 2 == 0 or not self.isPar and soma % 2 != 0:
            self.pararSom()
            self.tocarSom("voce ganhou.wav")
            mensagem = f"Parabéns, você ganhou! Jogador: {jogador}, Máquina: {self.maquina}"
            venceu = True
        else:
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            mensagem = f"Que pena, você perdeu! Jogador: {jogador}, Máquina: {self.maquina}"
        wx.CallLater(4500 if venceu else 4800, lambda: self.exibir_resultado(mensagem))

    def exibir_resultado(self, mensagem):
        dlg = ResultadoDialog(None, mensagem)
        if dlg.ShowModal() == wx.ID_OK:
            escolha = dlg.result
            if escolha == "jogar_novamente":
                self.script_init(None)
            elif escolha == "voltar_menu":
                wx.CallAfter(self.voltar_ao_menu)
            elif escolha == "sair":
                self.fechar_jogo()

    def voltar_ao_menu(self):
        self.tocarSom("trilha inicial.wav")
        menu = BlindGame.GlobalPlugin()
        menu.mostrarMenu()

    def fechar_jogo(self):
        self.pararSom()
        self.dialog.Destroy()

    def tocarSom(self, nomeSom):
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    __gestures = {}
