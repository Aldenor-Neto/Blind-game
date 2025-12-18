import ui
import globalPluginHandler
import wx
import random
import json
import os
import winsound

from .. import BlindGame


class Forca(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        wx.MessageBox(
            "Bem-vindo ao jogo da forca! Leia as informações na caixa de texto e precione o botão Palpite para fazer sua jogada.\n"
            "Coloque seu NVDA em modo grau de símbolos tudo, faça isso precionando Insert + P até ouvir grau de símbolos tudo."
        )

        addon_dir = os.path.dirname(__file__)
        dataset_path = os.path.join(addon_dir, "database/db_forca.json")
        self.dataset = self.load_dataset(dataset_path)

        if not self.dataset:
            wx.MessageBox("Não foi possível carregar o dataset. Jogo encerrado.")
            return

        self.category, self.word = self.choose_word_and_category(self.dataset)
        if not self.category or not self.word:
            wx.MessageBox("Não foi possível selecionar uma palavra ou categoria.")
            return

        self.word = self.word.lower()
        self.guessed_letters = set()
        self.attempts = 6

        self.frame = wx.Frame(None, title="Jogo da Forca", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        wx.StaticText(self.panel, label="Informações:", pos=(20, 10))

        self.progress_text = wx.TextCtrl(
            self.panel,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
            size=(350, 150),
            pos=(20, 30)
        )

        self.progress_text.AppendText(
            f"Dica: {self.category}\n"
            f"Tentativas restantes: {self.attempts}\n"
            f"Letras já jogadas: {', '.join(self.guessed_letters)}\n"
            f"Progresso: {self.get_progress()}\n"
        )

        self.new_guess_button = wx.Button(self.panel, label="Novo Palpite", pos=(150, 200))
        self.new_guess_button.Bind(wx.EVT_BUTTON, self.request_guess)

        self.voltar_button = wx.Button(self.panel, label="Voltar ao Menu", pos=(150, 200))
        self.voltar_button.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu())

        self.sair_button = wx.Button(self.panel, label="Sair", pos=(270, 200))
        self.sair_button.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo())

        self.frame.Show()

    def load_dataset(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                dataset = json.load(file)
                if "categorias" in dataset:
                    return dataset
        except Exception:
            pass
        return None

    def choose_word_and_category(self, dataset):
        category = random.choice(list(dataset["categorias"].keys()))
        word = random.choice(dataset["categorias"][category])
        return category, word

    def show_progress(self):
        self.progress_text.Clear()
        self.progress_text.AppendText(
            f"Dica: {self.category}\n"
            f"Tentativas restantes: {self.attempts}\n"
            f"Letras já jogadas: {', '.join(self.guessed_letters)}\n"
            f"Progresso: {self.get_progress()}\n"
        )

    def get_progress(self):
        return " ".join(
            letter if letter in self.guessed_letters else "_"
            for letter in self.word
        )

    def request_guess(self, event):
        with wx.TextEntryDialog(None, "Digite uma letra:", "Adivinhe a palavra") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                guess = dlg.GetValue().lower()

                if len(guess) != 1 or not guess.isalpha():
                    wx.MessageBox("Por favor, digite uma única letra válida.")
                    wx.CallLater(1000, self.request_guess, event)
                    return

                if guess in self.guessed_letters:
                    wx.MessageBox("Você já tentou essa letra.")
                    wx.CallLater(1000, self.request_guess, event)
                    return

                self.guessed_letters.add(guess)
                self.process_guess(guess)
                self.show_progress()

    def process_guess(self, guess):
        if guess in self.word:
            self.pararSom()
            self.tocarSom("acertou alegre.wav")
            wx.MessageBox("Boa! A letra está na palavra.")
        else:
            self.pararSom()
            self.tocarSom("errou alegre.wav")
            wx.MessageBox("Que pena! A letra não está na palavra.")
            self.attempts -= 1

        if self.attempts <= 0:
            mensagem = f"Você perdeu! A palavra era: {self.word}"
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            self.frame.Close()
            wx.CallLater(0, lambda: self.exibir_resultado(mensagem))

        elif all(letter in self.guessed_letters for letter in self.word):
            mensagem = f"Parabéns! Você adivinhou a palavra: {self.word}"
            self.pararSom()
            self.tocarSom("voce ganhou.wav")
            self.frame.Close()
            wx.CallLater(0, lambda: self.exibir_resultado(mensagem))

        else:
            wx.CallLater(2000, self.show_progress)

    def exibir_resultado(self, mensagem):
        dlg = ResultadoDialog(None, mensagem)

        if dlg.ShowModal() == wx.ID_OK:
            if dlg.result == "jogar_novamente":
                self.script_init(None)
            elif dlg.result == "voltar_menu":
                self.voltar_ao_menu()
            elif dlg.result == "sair":
                self.fechar_jogo()

    def voltar_ao_menu(self):
        self.pararSom()
        if hasattr(self, "frame") and self.frame:
            self.frame.Close()
        wx.CallAfter(lambda: BlindGame.GlobalPlugin().mostrarMenu())

    def fechar_jogo(self):
        self.pararSom()
        if hasattr(self, "frame") and self.frame:
            self.frame.Close()

    def tocarSom(self, nomeSom):
        BlindGame.tocarTrilha(nomeSom)

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)


class ResultadoDialog(wx.Dialog):
    def __init__(self, parent, mensagem):
        super(ResultadoDialog, self).__init__(parent, title="Resultado", size=(300, 200))
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
