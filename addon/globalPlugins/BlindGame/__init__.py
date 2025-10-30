import ui
import wx
import globalPluginHandler
import winsound
import os

from . import parOrImpar
from . import adivinheONumero
from . import forca
from . import calculeCerto
from . import jogo_da_velha
from . import genio

class GameMenuDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Menu de Jogos"):
        super(GameMenuDialog, self).__init__(parent, id, title, size=(300, 200))
        self.InitUI()
    
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        title = wx.StaticText(self, label="Selecione um jogo")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)
        self.btnParImpar = wx.Button(self, label="Par ou Ímpar")
        vbox.Add(self.btnParImpar, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnAdivinheNumero = wx.Button(self, label="Adivinhe o Número")
        vbox.Add(self.btnAdivinheNumero, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnForca= wx.Button(self, label="Forca")
        vbox.Add(self.btnForca, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnCalculeCerto= wx.Button(self, label="Calcúle Certo")
        vbox.Add(self.btnCalculeCerto, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnJogoDaVelha = wx.Button(self, label="Jogo da Velha")
        vbox.Add(self.btnJogoDaVelha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        self.btnGenio = wx.Button(self, label="Gênio Sonoro")
        vbox.Add(self.btnGenio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.btnClose = wx.Button(self, label="Fechar")
        vbox.Add(self.btnClose, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)
        self.SetSizer(vbox)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.tocarSom("bem vindo ao blind game.wav")
        wx.CallLater(0, lambda: self.mostrarMenu())

    def mostrarMenu(self):
        self.dialog = GameMenuDialog(None)
        self.dialog.btnParImpar.Bind(wx.EVT_BUTTON, self.iniciar_jogo_par_ou_impar)
        self.dialog.btnAdivinheNumero.Bind(wx.EVT_BUTTON, self.iniciar_jogo_adivinhe_o_numero)
        self.dialog.btnForca.Bind(wx.EVT_BUTTON, self.iniciar_jogo_forca)
        self.dialog.btnCalculeCerto.Bind(wx.EVT_BUTTON, self.iniciar_jogo_calcule_certo)
        self.dialog.btnJogoDaVelha.Bind(wx.EVT_BUTTON, self.iniciar_jogo_da_velha)
        self.dialog.btnGenio.Bind(wx.EVT_BUTTON, self.iniciar_jogo_genio)
        self.dialog.btnClose.Bind(wx.EVT_BUTTON, self.fechar_menu)
        self.dialog.ShowModal()

    def iniciar_jogo_par_ou_impar(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = parOrImpar.ParOrImpar()
        jogo.script_init(None)

    def iniciar_jogo_adivinhe_o_numero(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = adivinheONumero.AdivinheONumero()
        jogo.script_init(None)

    def iniciar_jogo_forca(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = forca.Forca()
        jogo.script_init(None)

    def iniciar_jogo_calcule_certo(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = calculeCerto.CalculeCerto()
        jogo.script_init(None)

    def iniciar_jogo_da_velha(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = jogo_da_velha.JogoDaVelha()
        jogo.script_init(None)

    def iniciar_jogo_genio(self, event):
        self.pararSom()
        self.dialog.Destroy()
        jogo = genio.Genio()
        jogo.script_init(None)

    def fechar_menu(self, event):
        self.pararSom()
        self.dialog.Destroy()

    def tocarSom(self, caminho):
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", caminho)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    __gestures = {
        "kb:NVDA+shift+J": "init"
    }
