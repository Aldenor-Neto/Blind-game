# 🎮 Blind Game

**Blind Game** é um complemento (add-on) desenvolvido para o leitor de telas [NVDA (NonVisual Desktop Access)](https://nvaccess.org/), que reúne uma **central de jogos clássicos e educativos totalmente acessíveis** para pessoas com deficiência visual.

Atualmente, o complemento conta com **6 jogos**, criados para oferecer diversão, aprendizado e desafios cognitivos de forma inclusiva e acessível.

---

## 🧩 Jogos disponíveis

### 1. Par ou Ímpar
Um jogo clássico de sorte!  
O usuário escolhe entre **Par** ou **Ímpar**, e o computador realiza uma jogada aleatória.  
O resultado é anunciado com base na soma das jogadas.

---

### 2. Adivinhe o Número
Desafie sua intuição!  
O computador escolhe um número secreto entre **0 e 100**, e o jogador deve adivinhar.  
O jogo possui **3 níveis de dificuldade**:
- **Fácil:** 10 tentativas disponíveis.  
- **Médio:** 7 tentativas.  
- **Difícil:** 5 Tentativas.

A cada palpite, o jogo informa se o número digitado é **maior** ou **menor** que o número secreto.

---

### 3. Calcule Certo
Teste seus conhecimentos básicos de matemática!  
O jogo apresenta operações de **adição**, **subtração**, **multiplicação** e **divisão**, sempre com dois operandos gerados aleatoriamente.  

A dificuldade aumenta progressivamente:
- A cada **8 rodadas**, os números ganham um novo dígito (por exemplo, de 1–9, depois 1–99, e assim por diante).  
O jogo termina quando o usuário erra uma operação.

---

### 4. Jogo da Forca
O tradicional **Jogo da Forca**, agora acessível no NVDA!  
O usuário deve adivinhar a palavra correta com base em uma dica fornecida.  
A cada erro, uma tentativa é perdida até que o boneco da forca esteja completo.

---

### 5. Jogo da Velha
Desafie o computador no clássico tabuleiro 3x3!  
O jogador joga com o **X** e o computador com o **0**.  
O objetivo é formar uma sequência de três símbolos — na **vertical**, **horizontal** ou **diagonal**.  
O primeiro a completar a sequência vence!

---

### 6. Gênio Sonoro
Um jogo de memória auditiva inspirado no famoso *Genius*!  
Cada número (1, 2, 3, e 4) representa um som distinto.  
O computador reproduz uma sequência de sons, e o jogador deve repeti-la corretamente.  
A cada rodada, a sequência aumenta — e o jogo termina quando o usuário erra.

---

## 🖥️ Estrutura e Desenvolvimento

O complemento foi desenvolvido em **Python**, seguindo o **template oficial de add-ons do NVDA**, respeitando a estrutura modular recomendada pela NV Access.

Cada jogo é implementado com **diálogos interativos e sonorizados**, garantindo acessibilidade total por meio do leitor de telas.

---

## ⌨️ Atalhos de Teclado

- **NVDA + Shift + J** → Abre o menu principal do **Blind Game**.

A partir desse menu, o usuário pode escolher o jogo desejado e iniciar a diversão.

- **NVDA + Shift + P** → Para e retoma a trilha sonora.

---

## 💡 Observações

- Compatível com o **NVDA 2022.4 ou superior**.  
- Todos os sons utilizados estão localizados na pasta `sounds` dentro do diretório do projeto.  
- Todos os jogos incluem efeitos sonoros para aprimorar a experiência de imersão.

---

## 🧑‍💻 Autor

**Aldenor Neto**  
Desenvolvedor e pesquisador em acessibilidade digital e usabilidade com foco em deficiência visual.

---

## 📄 Licença

Este projeto é distribuído sob a **Licença GPL v2**, a mesma utilizada pelo NVDA.  

---

## ❤️ Agradecimentos

Agradecimentos especiais à comunidade de usuários do NVDA e aos testadores com deficiência visual, cujo feedback foi essencial para aprimorar a jogabilidade e a acessibilidade de todos os jogos incluídos.

---

> *"Acessibilidade é mais do que inclusão — é liberdade para jogar, aprender e se divertir."*
