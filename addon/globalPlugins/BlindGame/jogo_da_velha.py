import ui
import globalPluginHandler
import wx
import winsound
import os
import random

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


class JogoDaVelha(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.tocarSom("trilha inicial.wav")
        self.tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
        self.rodada = 0
        self.jogador_atual = "X"  
        wx.CallLater(0, self.orientacoes)

    def orientacoes(self):
        frame = wx.Frame(None, title="Jogo da Velha", size=(500, 400))
        panel = wx.Panel(frame)

        conteudo = """ORIENTAÇÕES:

Coloque seu NVDA em modo grau de símbolos tudo, faça isso precionando Insert + P até ouvir grau de símbolos tudo.

Jogo da Velha - Você joga contra o computador!

Como jogar:
- Você é o X e o computador é o 0
- Digite a linha (1, 2 ou 3) e coluna (1, 2 ou 3) para fazer sua jogada
- O objetivo é formar uma linha, coluna ou diagonal com 3 símbolos iguais
- O jogo termina quando alguém vence ou quando todas as casas são preenchidas (empate)

Clique no botão Iniciar Jogo para começar.
"""

        text_ctrl = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        text_ctrl.SetFocus()

        btn_iniciar_jogo = wx.Button(panel, label="Iniciar Jogo")
        btn_menu = wx.Button(panel, label="Voltar ao Menu")
        btn_fechar = wx.Button(panel, label="Fechar")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(btn_iniciar_jogo, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_menu, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_fechar, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

        btn_iniciar_jogo.Bind(wx.EVT_BUTTON, lambda event: self.iniciar_jogo(frame))
        btn_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu(frame))
        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo(frame))

        frame.Show()

    def iniciar_jogo(self, frame_anterior=None):
        if frame_anterior:
            frame_anterior.Destroy()

        self.pararSom()
        self.tocarSom("trilha inicial.wav")

        self.tabuleiro = [[" " for _ in range(3)] for _ in range(3)]
        self.rodada = 0
        self.jogador_atual = "X"

        self.frame = wx.Frame(None, title="Jogo da Velha", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        titulo = wx.StaticText(self.panel, label="Jogo da Velha", pos=(150, 10))
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font)

        self.tabuleiro_text = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY, 
                                        size=(300, 150), pos=(50, 40))
        self.atualizar_tabuleiro()

        self.jogada_button = wx.Button(self.panel, label="Fazer Jogada", pos=(150, 200))
        self.jogada_button.Bind(wx.EVT_BUTTON, self.fazer_jogada)

        self.btn_voltar_menu = wx.Button(self.panel, label="Voltar ao Menu", pos=(50, 250))
        self.btn_sair = wx.Button(self.panel, label="Sair", pos=(250, 250))

        self.btn_voltar_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu(self.frame))
        self.btn_sair.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo(self.frame))

        self.frame.Show()

    def atualizar_tabuleiro(self):
        """Atualiza a exibição do tabuleiro na caixa de texto."""
        self.tabuleiro_text.Clear()
        for i, linha in enumerate(self.tabuleiro):
            linha_str = " | ".join(linha)
            self.tabuleiro_text.AppendText(f"{i+1}: {linha_str}\n")
            if i < 2:  
                self.tabuleiro_text.AppendText("  " + "-" * 9 + "\n")
        self.tabuleiro_text.AppendText("\nColunas: 1   2   3")

    def fazer_jogada(self, event):
        """Processa a jogada do jogador."""
        if self.jogador_atual == "X":
            self.jogada_humana()
        else:
            self.jogada_computador()

    def jogada_humana(self):
        """Permite que o jogador humano faça uma jogada."""
        with wx.TextEntryDialog(None, "Digite a linha (1, 2, 3):", "Sua jogada") as dlg_linha:
            if dlg_linha.ShowModal() == wx.ID_OK:
                try:
                    linha = int(dlg_linha.GetValue())
                    if linha not in [1, 2, 3]:
                        wx.MessageBox("Linha inválida! Digite 1, 2 ou 3.")
                        return
                except ValueError:
                    wx.MessageBox("Entrada inválida! Digite um número.")
                    return

        with wx.TextEntryDialog(None, "Digite a coluna (1, 2, 3):", "Sua jogada") as dlg_coluna:
            if dlg_coluna.ShowModal() == wx.ID_OK:
                try:
                    coluna = int(dlg_coluna.GetValue())
                    if coluna not in [1, 2, 3]:
                        wx.MessageBox("Coluna inválida! Digite 1, 2 ou 3.")
                        return
                except ValueError:
                    wx.MessageBox("Entrada inválida! Digite um número.")
                    return

        linha_interna = linha - 1
        coluna_interna = coluna - 1
        
        if self.tabuleiro[linha_interna][coluna_interna] != " ":
            wx.MessageBox("Posição já ocupada! Escolha outra posição.")
            return

        self.tabuleiro[linha_interna][coluna_interna] = "X"
        self.atualizar_tabuleiro()
        self.verificar_fim_jogo()

    def jogada_computador(self):
        """Computador joga em nível intermediário (meio inteligente, meio aleatório)."""

        import random

        # 50% chance de jogar de forma inteligente
        if random.random() < 0.5:
            # 1. Tentar vencer
            for i in range(3):
                for j in range(3):
                    if self.tabuleiro[i][j] == " ":
                        self.tabuleiro[i][j] = "0"
                        if self.verificar_vitoria("0"):
                            self.atualizar_tabuleiro()
                            self.verificar_fim_jogo()
                            return
                        self.tabuleiro[i][j] = " "  # desfaz

            # 2. Bloquear vitória do jogador
            for i in range(3):
                for j in range(3):
                    if self.tabuleiro[i][j] == " ":
                        self.tabuleiro[i][j] = "X"
                        if self.verificar_vitoria("X"):
                            self.tabuleiro[i][j] = "0"  
                            self.atualizar_tabuleiro()
                            self.verificar_fim_jogo()
                            return
                        self.tabuleiro[i][j] = " "  

        # 3. Jogada aleatória (ou sempre que não entrou acima)
        jogadas_disponiveis = [(i, j) for i in range(3) for j in range(3) if self.tabuleiro[i][j] == " "]
        if jogadas_disponiveis:
            linha, coluna = random.choice(jogadas_disponiveis)
            self.tabuleiro[linha][coluna] = "0"
            self.atualizar_tabuleiro()
        self.verificar_fim_jogo()

    def verificar_vitoria(self, jogador):
        """Verifica se um jogador venceu."""
        # Verifica linhas, colunas e diagonais
        for i in range(3):
            if all(self.tabuleiro[i][j] == jogador for j in range(3)):  
                return True
            if all(self.tabuleiro[j][i] == jogador for j in range(3)):  
                return True
        if all(self.tabuleiro[i][i] == jogador for i in range(3)):  
            return True
        if all(self.tabuleiro[i][2 - i] == jogador for i in range(3)):  
            return True
        return False

    def verificar_fim_jogo(self):
        """Verifica se o jogo terminou."""
        if self.verificar_vitoria("X"):
            self.pararSom()
            self.tocarSom("voce ganhou.wav")
            mensagem = "Parabéns! Você venceu! 🎉"
            self.frame.Close()
            self.exibir_resultado(mensagem)
        elif self.verificar_vitoria("0"):
            self.pararSom()
            self.tocarSom("voce perdeu.wav")
            mensagem = "O computador venceu! 😢"
            self.frame.Close()
            self.exibir_resultado(mensagem)
        elif all(self.tabuleiro[i][j] != " " for i in range(3) for j in range(3)):
            mensagem = "Deu velha! O jogo empatou. 🤝"
            self.frame.Close()
            self.exibir_resultado(mensagem)
        else:
            self.jogador_atual = "0" if self.jogador_atual == "X" else "X"
            if self.jogador_atual == "0":
                wx.CallLater(1000, self.jogada_computador)  

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

    def voltar_ao_menu(self, frame=None):
        try:
            if frame is not None:
                try:
                    frame.Destroy()
                except Exception:
                    pass
            self.tocarSom("trilha inicial.wav")
            menu = BlindGame.GlobalPlugin()
            menu.mostrarMenu()
        except Exception as e:
            print(f"Erro em voltar_ao_menu: {e}")

    def fechar_jogo(self, frame=None):
        try:
            self.pararSom()
            if frame is not None:
                try:
                    frame.Destroy()
                except Exception:
                    pass
        except Exception as e:
            print(f"Erro em fechar_jogo: {e}")

    def tocarSom(self, nomeSom):
        BlindGame.tocarTrilha(nomeSom)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    __gestures = {}
