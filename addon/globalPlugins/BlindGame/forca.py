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
        self.tocarSom("trilha inicial.wav")
        wx.MessageBox("Bem-vindo ao jogo da forca! Leia as informações na caixa de texto e precione o botão Palpite para fazer sua jogada. \n Coloque seu NVDA em modo grau de símbolos tudo, faça isso precionando Insert + P até ouvir grau de símbolos tudo.")

        addon_dir = os.path.dirname(__file__)
        dataset_path = os.path.join(addon_dir, "database/db_forca.json")
        self.dataset = self.load_dataset(dataset_path)
        if not self.dataset:
            wx.MessageBox("Não foi possível carregar o dataset. Jogo encerrado.")
            return

        # Escolhe uma categoria e uma palavra
        self.category, self.word = self.choose_word_and_category(self.dataset)
        if not self.category or not self.word:
            wx.MessageBox("Não foi possível selecionar uma palavra ou categoria. Verifique o dataset.")
            return

        # Converte a palavra para minúsculas para facilitar a comparação
        self.word = self.word.lower()

        # Inicializa variáveis do jogo
        self.guessed_letters = set()
        self.attempts = 6

        # Cria a interface gráfica
        self.frame = wx.Frame(None, title="Jogo da Forca", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        # Adiciona o título "Informações"
        informacoes_label = wx.StaticText(self.panel, label="Informações:", pos=(20, 10))

        # Criação de uma caixa de texto não editável
        self.progress_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(350, 150), pos=(20, 30))
        self.progress_text.AppendText(f"Dica: {self.category}\nTentativas restantes: {self.attempts}\nLetras já jogadas: {', '.join(self.guessed_letters)}\nProgresso: {self.get_progress()}\n")

        # Botão para fazer um novo palpite
        self.new_guess_button = wx.Button(self.panel, label="Novo Palpite", pos=(150, 200))
        self.new_guess_button.Bind(wx.EVT_BUTTON, self.request_guess)

        # Botão Voltar ao Menu
        self.voltar_button = wx.Button(self.panel, label="Voltar ao Menu", pos=(150, 200))
        self.voltar_button.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu())

        # Botão Sair
        self.sair_button = wx.Button(self.panel, label="Sair", pos=(270, 200))
        self.sair_button.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo())

        # Exibe a janela
        self.frame.Show()

    def load_dataset(self, file_path):
        """Carrega o dataset JSON."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                dataset = json.load(file)
                if "categorias" in dataset and isinstance(dataset["categorias"], dict):
                    return dataset
                else:
                    wx.MessageBox("Erro no formato do dataset.json. Verifique as categorias.")
                    return None
        except FileNotFoundError:
            wx.MessageBox("O arquivo dataset.json não foi encontrado.")
            return None
        except json.JSONDecodeError:
            wx.MessageBox("Erro ao decodificar o arquivo JSON. Verifique o formato do arquivo.")
            return None

    def choose_word_and_category(self, dataset):
        """Escolhe uma categoria e uma palavra aleatória."""
        if dataset and "categorias" in dataset:
            category = random.choice(list(dataset["categorias"].keys()))
            word = random.choice(dataset["categorias"][category])

            return category, word
        return None, None

    def show_progress(self):
        """Exibe o progresso atual do jogador."""
        self.progress_text.Clear()  # Limpa o conteúdo da caixa de texto
        self.progress_text.AppendText(f"Dica: {self.category}\nTentativas restantes: {self.attempts}\nLetras já jogadas: {', '.join(self.guessed_letters)}\nProgresso: {self.get_progress()}\n")

    def get_progress(self):
        """Retorna o progresso atual como uma string formatada."""
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)

    def request_guess(self, event):
        """Solicita uma letra ao jogador e atualiza a caixa de texto."""
        with wx.TextEntryDialog(None, "Digite uma letra:", "Adivinhe a palavra") as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                guess = dlg.GetValue().lower()  # Converte para minúsculas

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

                # Atualiza o progresso após o palpite
                self.show_progress()

    def process_guess(self, guess):
        """Processa a letra fornecida pelo jogador e atualiza o número de tentativas."""
        if guess in self.word:
            self.pararSom()
            self.tocarSom("acertou alegre.wav")
            wx.MessageBox("Boa! A letra está na palavra.")
        else:
            self.pararSom()
            self.tocarSom("errou alegre.wav")
            wx.MessageBox("Que pena! A letra não está na palavra.")
            self.attempts -= 1

        # Verifica se o jogo terminou
        if self.attempts <= 0:
            mensagem = f"Você perdeu! A palavra era: {self.word}"
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            self.frame.Close()  # Fecha a janela do jogo
        elif all(letter in self.guessed_letters for letter in self.word):
            mensagem = f"Parabéns! Você adivinhou a palavra: {self.word}"
            self.pararSom()
            self.tocarSom("voce ganhou.wav")
            self.frame.Close()  # Fecha a janela do jogo
        else:
            wx.CallLater(2000, self.show_progress)
        wx.CallLater(3000, lambda: self.exibir_resultado(mensagem))
    
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
        self.pararSom()
        if hasattr(self, "frame") and self.frame:
            self.frame.Destroy()
        self.tocarSom("trilha inicial.wav")
        wx.CallLater(500, lambda: BlindGame.GlobalPlugin().mostrarMenu())

    def fechar_jogo(self):
        self.pararSom()
        if hasattr(self, "frame") and self.frame:
            self.frame.Destroy()

    def tocarSom(self, nomeSom):
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)



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

