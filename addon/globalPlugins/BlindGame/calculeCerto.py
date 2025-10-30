import ui
import globalPluginHandler
import wx
import winsound
import os
import random
import math

from .. import BlindGame


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


class CalculeCerto(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.tocarSom("trilha inicial.wav")
        self.mensagem = ""
        self.num1 = 0
        self.num2 = 0
        self.palpite = 0
        self.cont = 1
        self.operacao = 1
        wx.CallLater(0, self.orientacoes)

    def orientacoes(self):
        frame = wx.Frame(None, title="Seja bem-vindo ao Calcule certo!", size=(600, 400))
        panel = wx.Panel(frame)

        conteudo = """ORIENTAÇÕES:
        
        Coloque seu NVDA em modo grau de símbolos tudo, faça isso precionando Insert + P até ouvir grau de símbolos tudo.

Você deve realizar o calculo das operações básicas de matemática
Adição representada pelo símbolo de +,
Subtração representada pelo símbolo de -,
Multiplicação representada pelo símbolo de * e
Divisão representada pelo símbolo de /.

O jogo termina quando você errar o calculo.

Clique no botão Iniciar Jogo para começar.
"""

        text_ctrl = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        text_ctrl.SetFocus()

        # Criar botões
        btn_iniciar_jogo = wx.Button(panel, label="Iniciar Jogo")
        btn_menu = wx.Button(panel, label="Voltar ao Menu")
        btn_fechar = wx.Button(panel, label="Fechar")

        # Organizar elementos
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(btn_iniciar_jogo, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_menu, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_fechar, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

        # Associar eventos aos botões
        btn_iniciar_jogo.Bind(wx.EVT_BUTTON, lambda event: self.iniciarJogo(frame))
        btn_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu(frame))
        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo(frame))

        frame.Show()

    def iniciarJogo(self, frame_anterior = None):
        if  frame_anterior:
            frame_anterior.Destroy()  

        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        self.num1= random.randint(1, self.cont * 2);
        self.num2= random.randint(1, self.num1)

        if self.operacao % 4 == 0:
            aux = self.num1
            self.num1 *= self.num2
            self.mensagem = f"Quanto é {self.num1} / {self.num2}"
            self.jogada()
            if abs(aux - self.palpite) < 0.01:  # Comparação com tolerância para float
                wx.MessageBox(f"Parabéns! Você acertou, o valor é {self.palpite}")
                self.cont += 1
                self.operacao += 1
                wx.CallLater(0, self.iniciarJogo)
            else:
                self.pararSom()
                self.tocarSom("voce perdeu.wav")
                self.mensagem = f"""Que pena você perdeu! o valor era {aux}
Você teve {self.cont-1} acertos!
"""
                self.exibir_resultado(self.mensagem)

        elif self.operacao % 3 == 0:
            self.mensagem = f"Quanto é {self.num1} * {self.num2}"
            self.jogada()
            if self.num1* self.num2== self.palpite:
                wx.MessageBox(f"Parabéns! Você acertou, o valor é {self.palpite}")
                self.cont += 1
                self.operacao += 1
                wx.CallLater(0, self.iniciarJogo)
            else:
                self.pararSom()
                self.tocarSom("voce perdeu.wav")
                self.mensagem = f"""Que pena você perdeu! o valor era {self.num1* self.num2}
Você teve {self.cont-1} acertos!
"""
                self.exibir_resultado(self.mensagem)

        elif self.operacao % 2 == 0:
            self.mensagem = f"Quanto é {self.num1} - {self.num2}"
            self.jogada()
            if self.num1- self.num2== self.palpite:
                wx.MessageBox(f"Parabéns! Você acertou, o valor é {self.palpite}")
                self.cont += 1
                self.operacao += 1
                wx.CallLater(0, self.iniciarJogo)
            else:
                self.pararSom()
                self.tocarSom("voce perdeu.wav")
                self.mensagem = f"""Que pena você perdeu! o valor era {self.num1 - self.num2}
Você teve {self.cont-1} acertos
"""
                self.exibir_resultado(self.mensagem)

        else:
            self.mensagem = f"Quanto é {self.num1} + {self.num2}"
            self.jogada()
            if self.num1+ self.num2== self.palpite:
                wx.MessageBox(f"Parabéns! Você acertou, o valor é {self.palpite}")
                self.cont += 1
                self.operacao += 1
                wx.CallLater(0, self.iniciarJogo)
            else:
                self.pararSom()
                self.tocarSom("voce perdeu.wav")
                self.mensagem = f"""Que pena você perdeu! o valor era {self.num1 + self.num2}
Você teve {self.cont-1} acertos!
"""
                self.exibir_resultado(self.mensagem)

    def jogada(self):
        with wx.TextEntryDialog(None, "Calcule Certo!", self.mensagem) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                try:
                    # Para divisões, aceita float, para outras operações aceita int
                    if self.operacao % 4 == 0:  # Divisão
                        self.palpite = float(dlg.GetValue())
                    else:
                        self.palpite = int(dlg.GetValue())
                except ValueError:
                    wx.MessageBox("Entrada inválida! Digite um número válido.")
                    self.jogada()  # Chama novamente se entrada inválida

    def exibir_resultado(self, mensagem):
        dlg = ResultadoDialog(None, mensagem)
        if dlg.ShowModal() == wx.ID_OK:
            escolha = dlg.result
            if escolha == "jogar_novamente":
                self.script_init(None)
            elif escolha == "voltar_menu":
                wx.CallAfter(self.voltar_ao_menu, dlg)
            elif escolha == "sair":
                self.fechar_jogo()

    def voltar_ao_menu(self, frame_atual=None):
        if frame_atual is not None:
            try:
                frame_atual.Destroy()
            except:
                pass
        self.tocarSom("trilha inicial.wav")
        menu = BlindGame.GlobalPlugin()
        menu.mostrarMenu()

    def fechar_jogo(self, frame_atual):
        frame_atual.Destroy()  # Fecha a janela
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
