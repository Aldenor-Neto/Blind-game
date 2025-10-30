import ui
import globalPluginHandler
import random

import wx
import winsound
import os

from .. import BlindGame

class NivelJogoDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Escolha o nível do jogo"):
        super(NivelJogoDialog, self).__init__(parent, id, title, size=(300, 200))
        self.escolha = None
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Escolha um nível")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        self.btnFacil = wx.Button(self, label="Fácil")
        vbox.Add(self.btnFacil, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnMedio = wx.Button(self, label="Médio")
        vbox.Add(self.btnMedio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnDificil = wx.Button(self, label="Difícil")
        vbox.Add(self.btnDificil, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.SetSizer(vbox)
        self.btnFacil.Bind(wx.EVT_BUTTON, self.on_facil)
        self.btnMedio.Bind(wx.EVT_BUTTON, self.on_medio)
        self.btnDificil.Bind(wx.EVT_BUTTON, self.on_dificil)

    def on_facil(self, event):
        self.escolha = "facil"
        self.EndModal(wx.ID_OK)

    def on_medio(self, event):
        self.escolha = "medio"
        self.EndModal(wx.ID_OK)

    def on_dificil(self, event):
        self.escolha = "dificil"
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

class AdivinheONumero(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.tocarSom("trilha inicial.wav")
        self.secreto = random.randint(0, 100)
        wx.CallLater(0, self.nivelJogo)

    def nivelJogo(self):
        dlg = NivelJogoDialog(None)
        if dlg.ShowModal() == wx.ID_OK and dlg.escolha is not None:
            self.escolha = dlg.escolha
            if self.escolha == "facil":
                self.pararSom()
                self.tocarSom("trilha inicial.wav")
                self.tentativas = 10
            elif self.escolha == "medio":
                self.pararSom()
                self.tocarSom("trilha inicial.wav")
                self.tentativas = 7
            elif self.escolha == "dificil":
                self.pararSom()
                self.tocarSom("trilha inicial.wav")
                self.tentativas = 5
            wx.CallLater(0, self.playGame)

    def playGame(self):
        self.pararSom()
        self.tocarSom("trilha inicial.wav")
        while self.tentativas > 0:
            with wx.TextEntryDialog(None, "Qual sua jogada!", "O número secreto está entre 0 e 100!") as dlg:
                if dlg.ShowModal() == wx.ID_OK:
                    try:
                        self.jogada = int(dlg.GetValue())
                        if self.secreto < self.jogada:
                            self.tentativas -= 1
                            if self.tentativas == 2:
                                self.pararSom()
                                self.tocarSom("acertou cuidado.wav")
                                wx.MessageBox("O número secreto é menor que seu palpite, Cuidado você só tem duas tentativas")
                                continue
                            elif self.tentativas == 1:
                                self.pararSom()
                                self.tocarSom("acertou cuidado.wav")
                                wx.MessageBox("O número secreto é menor que seu palpite, Cuidado você só tem uma tentativa!")
                                continue

                            self.pararSom()
                            self.tocarSom("acertou alegre.wav")
                            wx.MessageBox("O número secreto é menor que seu palpite!")
                            
                        elif self.secreto > self.jogada:
                            self.tentativas-=1
                            if self.tentativas == 2:
                                self.pararSom()
                                self.tocarSom("acertou cuidado.wav")
                                wx.MessageBox("O número secreto é maior que seu palpite, cuidado você só tem duas tentativas!")
                                continue
                            elif self.tentativas == 1:
                                self.pararSom()
                                self.tocarSom("acertou cuidado.wav")
                                wx.MessageBox("O número secreto é maior que seu palpite, cuidado você só tem uma tentativa!")
                                continue

                            self.pararSom()
                            self.tocarSom("acertou alegre.wav")
                            wx.MessageBox("O número secreto é maior que seu palpite!")

                        else:
                            break
                    except ValueError:
                        wx.MessageBox("Informe um valor válido! Apenas números.")
        if self.tentativas == 0:
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            wx.CallLater(6200, lambda: self.exibir_resultado(f"Que pena, você perdeu! O número secreto era: {self.secreto}"))
        else:
            self.pararSom()
            self.tocarSom("voce ganhou.wav")
            wx.CallLater(5000, lambda: self.exibir_resultado(f"Parabéns, você acertou o número secreto! Número Secreto: {self.secreto}"))

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
        self.tocarSom("trilha sem fala.wav")
        menu = BlindGame.GlobalPlugin()
        menu.mostrarMenu()

    def fechar_jogo(self):
        self.pararSom()

    def tocarSom(self, nomeSom):
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    __gestures = {}
