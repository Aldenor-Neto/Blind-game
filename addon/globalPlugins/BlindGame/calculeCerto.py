import ui
import wx
import winsound
import random
import math

from .. import BlindGame


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


class CalculeCerto:

    def script_init(self, gesture=None):
        self.cont = 1
        self.operacao = 1
        self.pararSom()
        self.tocarSom("trilha inicial.wav")
        wx.CallLater(0, self.orientacoes)

    def orientacoes(self):
        frame = wx.Frame(None, title="Seja bem-vindo ao Calcule Certo!", size=(600, 400))
        panel = wx.Panel(frame)

        conteudo = (
            "ORIENTAÇÕES:\n\n"
            "Coloque o NVDA em grau de símbolos tudo.\n\n"
            "Você deve resolver operações matemáticas básicas:\n"
            "+ Adição\n"
            "- Subtração\n"
            "* Multiplicação\n"
            "/ Divisão\n\n"
            "O jogo termina ao errar um cálculo.\n\n"
            "Clique em 'Iniciar Jogo' para começar."
        )

        text_ctrl = wx.TextCtrl(
            panel,
            value=conteudo,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        )
        text_ctrl.SetFocus()

        btn_iniciar = wx.Button(panel, label="Iniciar Jogo")
        btn_menu = wx.Button(panel, label="Voltar ao Menu")
        btn_fechar = wx.Button(panel, label="Fechar")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(btn_iniciar, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_menu, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(btn_fechar, 0, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(sizer)

        btn_iniciar.Bind(wx.EVT_BUTTON, lambda e: self.iniciarJogo(frame))
        btn_menu.Bind(wx.EVT_BUTTON, lambda e: self.voltar_ao_menu(frame))
        btn_fechar.Bind(wx.EVT_BUTTON, lambda e: self.fechar_jogo(frame))

        frame.Show()

    def iniciarJogo(self, frame_anterior=None):
        if frame_anterior:
            frame_anterior.Destroy()

        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        num1 = random.randint(1, self.cont * 2)
        num2 = random.randint(1, num1)

        if self.operacao % 4 == 0:
            resultado = num1
            pergunta = f"Quanto é {num1 * num2} / {num2}"
            correto = float(resultado)

        elif self.operacao % 3 == 0:
            pergunta = f"Quanto é {num1} * {num2}"
            correto = num1 * num2

        elif self.operacao % 2 == 0:
            pergunta = f"Quanto é {num1} - {num2}"
            correto = num1 - num2

        else:
            pergunta = f"Quanto é {num1} + {num2}"
            correto = num1 + num2

        palpite = self.jogada(pergunta)

        if palpite is None:
            return

        if abs(palpite - correto) < 0.01:
            wx.MessageBox("Parabéns! Você acertou!")
            self.cont += 1
            self.operacao += 1
            wx.CallLater(0, self.iniciarJogo)
        else:
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            wx.CallLater(
                0,
                lambda: self.exibir_resultado(
                    f"Que pena! O valor correto era {correto}\n"
                    f"Você teve {self.cont - 1} acertos."
                )
            )

    def jogada(self, mensagem):
        with wx.TextEntryDialog(None, "Calcule Certo!", mensagem) as dlg:
            if dlg.ShowModal() != wx.ID_OK:
                return None
            try:
                return float(dlg.GetValue())
            except ValueError:
                wx.MessageBox("Digite um número válido.")
                return self.jogada(mensagem)

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
