import ui
import globalPluginHandler
import wx
import winsound
import os
import random
import time

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


class Genio(globalPluginHandler.GlobalPlugin):
    def script_init(self, gesture):
        self.pararSom()  # Garante que não há trilha tocando
        self.sequencia = []
        self.rodada = 1
        self.posicao_atual = 0
        self.modo_treino = True
        wx.CallLater(0, self.orientacoes)

    def orientacoes(self):
        frame = wx.Frame(None, title="Gênio Sonoro", size=(500, 400))
        panel = wx.Panel(frame)

        self.tocarSom("trilha inicial.wav")
        
        conteudo = """ORIENTAÇÕES:
Gênio Sonoro - Teste sua memória auditiva!

Como jogar:
- O jogo reproduzirá uma sequência de sons
- Você deve repetir a sequência na ordem correta
- Use os botões 1, 2, 3 e 4 para reproduzir os sons
- A sequência aumenta a cada rodada
- O jogo termina quando você errar

Modo Treino:
- Use os botões para ouvir cada som
- Familiarize-se com os sons antes de começar

Clique no botão Iniciar Jogo para começar.
"""

        text_ctrl = wx.TextCtrl(panel, value=conteudo, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        text_ctrl.SetFocus()

        # Criar botões
        btn_iniciar_jogo = wx.Button(panel, label="Iniciar Jogo")
        btn_treino = wx.Button(panel, label="Modo Treino")
        btn_menu = wx.Button(panel, label="Voltar ao Menu")
        btn_fechar = wx.Button(panel, label="Fechar")

        # Organizar elementos
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        sizer.Add(btn_iniciar_jogo, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_treino, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_menu, flag=wx.EXPAND | wx.ALL, border=5)
        sizer.Add(btn_fechar, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(sizer)

        # Associar eventos aos botões
        btn_iniciar_jogo.Bind(wx.EVT_BUTTON, lambda event: self.iniciar_jogo(frame))
        btn_treino.Bind(wx.EVT_BUTTON, lambda event: self.modo_treino_interface(frame))
        btn_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu(frame))
        btn_fechar.Bind(wx.EVT_BUTTON, lambda event: self.fechar_jogo(frame))


        frame.Show()

    def iniciar_jogo(self, frame_anterior=None):
        if frame_anterior:
            frame_anterior.Destroy()

        self.pararSom()  # Para a trilha sonora no jogo principal

        # Reinicializa o jogo
        self.sequencia = []
        self.rodada = 1
        self.posicao_atual = 0
        self.modo_treino = False

        # Cria a interface do jogo
        self.frame = wx.Frame(None, title="Gênio Sonoro - Jogo", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        # Título
        titulo = wx.StaticText(self.panel, label="Gênio Sonoro", pos=(150, 10))
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font)

        # Status do jogo
        self.status_text = wx.StaticText(self.panel, label="Preparando...", pos=(20, 40))

        # Botões de som
        self.btn_som1 = wx.Button(self.panel, label="Som 1", pos=(50, 80), size=(60, 40))
        self.btn_som2 = wx.Button(self.panel, label="Som 2", pos=(120, 80), size=(60, 40))
        self.btn_som3 = wx.Button(self.panel, label="Som 3", pos=(190, 80), size=(60, 40))
        self.btn_som4 = wx.Button(self.panel, label="Som 4", pos=(260, 80), size=(60, 40))

        # Associar eventos aos botões
        self.btn_som1.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(1))
        self.btn_som2.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(2))
        self.btn_som3.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(3))
        self.btn_som4.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(4))

        # Botão para iniciar rodada
        #self.btn_iniciar_rodada = wx.Button(self.panel, label="Iniciar Rodada", pos=(150, 140))
        #self.btn_iniciar_rodada.Bind(wx.EVT_BUTTON, self.iniciar_rodada)

        self.frame.Show()
        self.frame.Bind(wx.EVT_CHAR_HOOK, self.on_tecla)

        wx.CallLater(1000, lambda: self.iniciar_rodada(None))

    def modo_treino_interface(self, frame_anterior=None):
        if frame_anterior:
            frame_anterior.Destroy()

        self.pararSom()  # Para a trilha sonora no modo treino
        self.modo_treino = True  # Define explicitamente como modo treino

        # Cria a interface do treino
        self.frame = wx.Frame(None, title="Gênio Sonoro - Treino", size=(400, 300))
        self.panel = wx.Panel(self.frame)

        # Título
        titulo = wx.StaticText(self.panel, label="Modo Treino", pos=(150, 10))
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        titulo.SetFont(font)

        # Instruções
        instrucoes = wx.StaticText(self.panel, label="Clique nos botões para ouvir os sons:", pos=(20, 40))

        # Botões de som
        self.btn_som1 = wx.Button(self.panel, label="Som 1", pos=(50, 80), size=(60, 40))
        self.btn_som2 = wx.Button(self.panel, label="Som 2", pos=(120, 80), size=(60, 40))
        self.btn_som3 = wx.Button(self.panel, label="Som 3", pos=(190, 80), size=(60, 40))
        self.btn_som4 = wx.Button(self.panel, label="Som 4", pos=(260, 80), size=(60, 40))

        # Associar eventos aos botões
        self.btn_som1.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(1))
        self.btn_som2.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(2))
        self.btn_som3.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(3))
        self.btn_som4.Bind(wx.EVT_BUTTON, lambda event: self.reproduzir_som(4))

        # Botões de controle
        btn_voltar = wx.Button(self.panel, label="Voltar", pos=(50, 140))
        btn_iniciar_jogo = wx.Button(self.panel, label="Iniciar Jogo", pos=(150, 140))
        btn_menu = wx.Button(self.panel, label="Menu Principal", pos=(250, 140))

        btn_voltar.Bind(wx.EVT_BUTTON, lambda event: (self.frame.Destroy(), self.orientacoes()))

        btn_iniciar_jogo.Bind(wx.EVT_BUTTON, lambda event: self.iniciar_jogo(self.frame))
        btn_menu.Bind(wx.EVT_BUTTON, lambda event: self.voltar_ao_menu(self.frame))

        self.frame.Show()
        self.frame.Bind(wx.EVT_CHAR_HOOK, self.on_tecla)


    def reproduzir_som(self, botao):
        """Reproduz o som do botão especificado."""
        # Define sons originais do Windows para cada botão
        sons_botoes = {
            1: "genio/som1.wav",  # chimes.wav
            2: "genio/som2.wav",  # ding.wav
            3: "genio/som3.wav",  # tada.wav
            4: "genio/som4.wav"   # notify.wav
        }
        
        som_botao = sons_botoes.get(botao, "genio/som1.wav")
        
        if self.modo_treino:
            self.tocarSomJogo(som_botao)  # Som específico do botão no treino
        else:
            # No jogo, verifica se é a jogada correta
            if self.posicao_atual < len(self.sequencia):
                if botao == self.sequencia[self.posicao_atual]:
                    # Apenas reproduz o som do botão, sem som de acerto
                    self.tocarSomJogo(som_botao)
                    self.posicao_atual += 1
                    self.atualizar_status()
                    
                    # Verifica se completou a sequência
                    if self.posicao_atual >= len(self.sequencia):
                        self.rodada_concluida()
                else:
                    self.tocarSomJogo("errou.wav")
                    self.fim_jogo()
            else:
                self.tocarSomJogo("errou.wav")

    def iniciar_rodada(self, event):
        """Inicia uma nova rodada do jogo."""
        # Adiciona um novo som à sequência
        self.sequencia.append(random.randint(1, 4))
        self.posicao_atual = 0
        
        self.status_text.SetLabel(f"Rodada {self.rodada} - Reproduzindo sequência...")
        #self.btn_iniciar_rodada.Enable(False)
        
        # Reproduz a sequência
        self.reproduzir_sequencia()

    def reproduzir_sequencia(self):
        """Reproduz a sequência atual."""
        if not self.sequencia:
            return
            
        self.indice_sequencia = 0
        self.reproduzir_proximo_som()

    def reproduzir_proximo_som(self):
        """Reproduz o próximo som da sequência."""
        if self.indice_sequencia < len(self.sequencia):
            botao = self.sequencia[self.indice_sequencia]
            # Define sons originais do Windows para cada botão na sequência
            sons_botoes = {
                1: "genio/som1.wav",
                2: "genio/som2.wav",
                3: "genio/som3.wav",
                4: "genio/som4.wav"
            }
            som_botao = sons_botoes.get(botao, "genio/som1.wav")
            self.tocarSomJogo(som_botao)  # Som específico do botão na sequência
            self.indice_sequencia += 1
            wx.CallLater(700, self.reproduzir_proximo_som)  # Intervalo de 0.7s
        else:
            # Sequência terminou, agora é a vez do jogador
            self.status_text.SetLabel(f"Rodada {self.rodada} - Sua vez! Repita a sequência:")

    def atualizar_status(self):
        """Atualiza o status do jogo."""
        if self.posicao_atual < len(self.sequencia):
            self.status_text.SetLabel(f"Rodada {self.rodada} - Posição {self.posicao_atual + 1} de {len(self.sequencia)}")
        else:
            self.status_text.SetLabel(f"Rodada {self.rodada} - Sequência completa!")

    def rodada_concluida(self):
        """Executa quando o jogador completa a rodada."""
        self.tocarSom("genio/acertou.wav")
        self.status_text.SetLabel(f"✅ Rodada {self.rodada} concluída!")
        self.rodada += 1

        # Espera 1 segundo e inicia a próxima rodada
        wx.CallLater(2000, lambda: self.iniciar_rodada(None))

    def fim_jogo(self):
        """Termina o jogo."""
        self.tocarSom("voce perdeu.wav")
        mensagem = f"❌ Errou! Fim de jogo.\nVocê chegou até a rodada {self.rodada}."
        self.frame.Close()
        self.exibir_resultado(mensagem)

    def exibir_resultado(self, mensagem):
        dlg = ResultadoDialog(None, mensagem)
        if dlg.ShowModal() == wx.ID_OK:
            escolha = dlg.result
            if escolha == "jogar_novamente":
                self.reiniciar_jogo()
            elif escolha == "voltar_menu":
                wx.CallAfter(self.voltar_ao_menu)
            elif escolha == "sair":
                self.fechar_jogo()

    def reiniciar_jogo(self):
        """Reinicia o jogo sem tocar a trilha sonora."""
        self.pararSom()
        self.sequencia = []
        self.rodada = 1
        self.posicao_atual = 0
        self.modo_treino = False
        wx.CallLater(0, self.iniciar_jogo)

    def voltar_ao_menu(self, frame_atual=None):
        if frame_atual:
            frame_atual.Destroy()
        self.tocarSom("trilha inicial.wav")
        menu = BlindGame.GlobalPlugin()
        menu.mostrarMenu()

    def fechar_jogo(self, frame_atual=None):
        self.pararSom()
        if frame_atual:
            frame_atual.Destroy()

    def tocarSom(self, nomeSom):
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)
        try:
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def tocarSomJogo(self, nomeSom):
        """Reproduz som do jogo com volume aumentado."""
        caminho_som = os.path.join(os.path.dirname(__file__), "sounds", nomeSom)
        try:
            # Usa SND_FILENAME | SND_ASYNC | SND_LOOP para melhor controle de volume
            winsound.PlaySound(caminho_som, winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Erro ao reproduzir o som: {e}")

    def pararSom(self):
        winsound.PlaySound(None, winsound.SND_ASYNC)

    def on_tecla(self, event):
        key_code = event.GetKeyCode()
        # Mapear teclas '1', '2', '3', '4' do teclado alfanumérico e numérico
        num_pad_map = {wx.WXK_NUMPAD1: 1, wx.WXK_NUMPAD2: 2, wx.WXK_NUMPAD3: 3, wx.WXK_NUMPAD4: 4}
        if key_code in [49, 50, 51, 52]:  # Teclado alfanumérico
            botao = key_code - 48
            self.reproduzir_som(botao)
        elif key_code in num_pad_map:  # Teclado numérico
            self.reproduzir_som(num_pad_map[key_code])
        else:
            event.Skip()

    __gestures = {}
