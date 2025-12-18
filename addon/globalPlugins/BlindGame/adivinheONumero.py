import ui
import random
import wx
import winsound
import os

from .. import BlindGame


class NivelJogoDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Escolha o nível do jogo"):
        super().__init__(parent, id, title, size=(300, 200))
        self.escolha = None
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="Escolha um nível")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.btnFacil = wx.Button(self, label="Fácil (10 Tentativas)")
        self.btnMedio = wx.Button(self, label="Médio (7 Tentativas)")
        self.btnDificil = wx.Button(self, label="Difícil (5 Tentativas)")

        for btn in (self.btnFacil, self.btnMedio, self.btnDificil):
            vbox.Add(btn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

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


class AdivinheONumero:

    def script_init(self, gesture=None):
        self.secreto = random.randint(0, 100)
        self.tocarSom("trilha inicial.wav")
        wx.CallLater(0, self.nivelJogo)

    def nivelJogo(self):
        dlg = NivelJogoDialog(None)

        if dlg.ShowModal() == wx.ID_OK and dlg.escolha:
            self.escolha = dlg.escolha

            if self.escolha == "facil":
                self.tentativas = 10
            elif self.escolha == "medio":
                self.tentativas = 7
            else:
                self.tentativas = 5

            self.pararSom()
            self.tocarSom("trilha inicial.wav")
            wx.CallLater(0, self.playGame)

    def playGame(self):
        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        while self.tentativas > 0:
            with wx.TextEntryDialog(
                None,
                "Qual sua jogada!",
                "O número secreto está entre 0 e 100!"
            ) as dlg:

                if dlg.ShowModal() != wx.ID_OK:
                    return

                try:
                    jogada = int(dlg.GetValue())
                except ValueError:
                    wx.MessageBox("Informe um valor válido! Apenas números.")
                    continue

                self.tentativas -= 1

                if jogada == self.secreto:
                    break

                aviso = "menor" if jogada > self.secreto else "maior"

                if self.tentativas <= 2:
                    self.pararSom()
                    self.tocarSom("acertou cuidado.wav")
                    wx.MessageBox(
                        f"O número secreto é {aviso} que seu palpite. "
                        f"Cuidado, você só tem {self.tentativas} tentativa(s)!"
                    )
                else:
                    self.pararSom()
                    self.tocarSom("acertou alegre.wav")
                    wx.MessageBox(f"O número secreto é {aviso} que seu palpite!")

        self.pararSom()

        if self.tentativas == 0:
            self.tocarSom("voce perdeu.wav")
            wx.CallLater(
                0,
                lambda: self.exibir_resultado(
                    f"Que pena, você perdeu! O número secreto era: {self.secreto}"
                )
            )
        else:
            self.tocarSom("voce ganhou.wav")
            wx.CallLater(
                0,
                lambda: self.exibir_resultado(
                    f"Parabéns, você acertou o número secreto! Número: {self.secreto}"
                )
            )

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
        BlindGame.tocarTrilha("trilha sem fala.wav")
        BlindGame.GlobalPlugin().mostrarMenu()

    def fechar_jogo(self):
        self.pararSom()

    def tocarSom(self, nomeSom):
        BlindGame.tocarTrilha(nomeSom)

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)
