import ui
import wx
import random
import winsound

from .. import BlindGame

class OpcaoDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Escolha par ou ímpar"):
        super().__init__(parent, id, title, size=(300, 200))
        self.escolha = None
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="Escolha uma opção")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.btnPar = wx.Button(self, label="Par")
        self.btnImpar = wx.Button(self, label="Ímpar")

        vbox.Add(self.btnPar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
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
        super().__init__(parent, title="Resultado", size=(300, 200))
        self.mensagem = mensagem
        self.result = None
        self.InitUI()

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

        self.SetSizer(vbox)

        btnJogarNovamente.Bind(wx.EVT_BUTTON, self.on_jogar_novamente)
        btnVoltarMenu.Bind(wx.EVT_BUTTON, self.on_voltar_menu)
        btnSair.Bind(wx.EVT_BUTTON, self.on_sair)

    def on_jogar_novamente(self, event):
        self.result = "jogar_novamente"
        self.EndModal(wx.ID_OK)

    def on_voltar_menu(self, event):
        self.result = "voltar_menu"
        self.EndModal(wx.ID_OK)

    def on_sair(self, event):
        self.result = "sair"
        self.EndModal(wx.ID_OK)

class ParOrImpar:

    def script_init(self, gesture=None):
        self.maquina = random.randint(0, 10)
        self.isPar = None

        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        wx.CallLater(0, self.selecionaOpcao)

    def selecionaOpcao(self):
        dlg = OpcaoDialog(None)

        if dlg.ShowModal() == wx.ID_OK and dlg.escolha:
            self.isPar = True if dlg.escolha == "par" else False

            self.pararSom()
            self.tocarSom("trilha inicial.wav")

            wx.CallLater(0, self.solicitaJogada)

    def solicitaJogada(self):
        with wx.TextEntryDialog(None, "Escolha um número!", "Sua jogada") as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return

            entrada = dlg.GetValue()

            if not self.validarEntrada(entrada):
                wx.MessageBox("Digite uma opção válida (número)!")
                wx.CallAfter(self.solicitaJogada)
                return

            jogador = int(entrada)
            self.calculaResultado(jogador)

    def validarEntrada(self, entrada):
        return entrada.isdigit()

    def calculaResultado(self, jogador):
        soma = jogador + self.maquina

        self.pararSom()

        if (self.isPar and soma % 2 == 0) or (not self.isPar and soma % 2 != 0):
            self.tocarSom("voce ganhou.wav")
            mensagem = (
                f"Parabéns, você ganhou! "
                f"Jogador: {jogador}, Máquina: {self.maquina}"
            )
        else:
            self.tocarSom("voce perdeu.wav")
            mensagem = (
                f"Que pena, você perdeu! "
                f"Jogador: {jogador}, Máquina: {self.maquina}"
            )

        wx.CallLater(0, lambda: self.exibir_resultado(mensagem))

    def exibir_resultado(self, mensagem):
        dlg = ResultadoDialog(None, mensagem)

        if dlg.ShowModal() == wx.ID_OK:
            if dlg.result == "jogar_novamente":
                self.script_init()
            elif dlg.result == "voltar_menu":
                self.voltar_ao_menu()
            elif dlg.result == "sair":
                self.fechar_jogo()

    def voltar_ao_menu(self):
        self.pararSom()
        BlindGame.GlobalPlugin().mostrarMenu()

    def fechar_jogo(self):
        self.pararSom()

    def tocarSom(self, nomeSom):
        BlindGame.tocarTrilha(nomeSom)

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)
