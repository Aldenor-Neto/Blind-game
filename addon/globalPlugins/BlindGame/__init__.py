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

TRILHA_PAUSADA = False

def tocarTrilha(nomeSom):
    """
    Reproduz uma trilha sonora respeitando o estado global
    de pausa (Shift+P).
    """
    global TRILHA_PAUSADA

    if TRILHA_PAUSADA:
        return

    caminho = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)

    try:
        winsound.PlaySound(
            caminho,
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )
    except Exception as e:
        print(f"Erro ao reproduzir o som: {e}")


def pararTrilha():
    winsound.PlaySound(None, winsound.SND_ASYNC)

class GameMenuDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title="Menu de Jogos"):
        super().__init__(parent, id, title, size=(300, 200))
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        title = wx.StaticText(self, label="Selecione um jogo")
        vbox.Add(title, flag=wx.ALIGN_CENTER | wx.TOP, border=10)

        self.btnParImpar = wx.Button(self, label="Par ou Ímpar")
        self.btnAdivinheNumero = wx.Button(self, label="Adivinhe o Número")
        self.btnForca = wx.Button(self, label="Forca")
        self.btnCalculeCerto = wx.Button(self, label="Calcúle Certo")
        self.btnJogoDaVelha = wx.Button(self, label="Jogo da Velha")
        self.btnGenio = wx.Button(self, label="Gênio Sonoro")
        self.btnClose = wx.Button(self, label="Fechar")

        for btn in (
            self.btnParImpar,
            self.btnAdivinheNumero,
            self.btnForca,
            self.btnCalculeCerto,
            self.btnJogoDaVelha,
            self.btnGenio,
            self.btnClose,
        ):
            vbox.Add(btn, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.SetSizer(vbox)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    scriptCategory = "Blind Game"

    __gestures = {
        "kb:NVDA+shift+J": "init",
        "kb:NVDA+shift+p": "toggle_trilha",
    }

    def script_init(self, gesture):
        tocarTrilha("bem vindo ao blind game.wav")
        wx.CallLater(0, self.mostrarMenu)

    def mostrarMenu(self):
        tocarTrilha("bem vindo ao blind game.wav")
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
        pararTrilha()
        self.dialog.Destroy()
        parOrImpar.ParOrImpar().script_init(None)

    def iniciar_jogo_adivinhe_o_numero(self, event):
        pararTrilha()
        self.dialog.Destroy()
        adivinheONumero.AdivinheONumero().script_init(None)

    def iniciar_jogo_forca(self, event):
        pararTrilha()
        self.dialog.Destroy()
        forca.Forca().script_init(None)

    def iniciar_jogo_calcule_certo(self, event):
        pararTrilha()
        self.dialog.Destroy()
        calculeCerto.CalculeCerto().script_init(None)

    def iniciar_jogo_da_velha(self, event):
        pararTrilha()
        self.dialog.Destroy()
        jogo_da_velha.JogoDaVelha().script_init(None)

    def iniciar_jogo_genio(self, event):
        pararTrilha()
        self.dialog.Destroy()
        genio.Genio().script_init(None)

    def fechar_menu(self, event):
        pararTrilha()
        self.dialog.Destroy()

    def script_toggle_trilha(self, gesture):
        global TRILHA_PAUSADA

        if not TRILHA_PAUSADA:
            TRILHA_PAUSADA = True
            pararTrilha()
            ui.message("Trilha sonora pausada")
        else:
            TRILHA_PAUSADA = False
            ui.message("A trilha sonora será retomada na próxima janela")
