import tkinter as tk
from tkinter import messagebox
import pika
import json
import sys

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Unicap Jogo da Velha")
        self.root.configure(bg='red')  # Configura a cor de fundo para vermelho

        # Jogador atual (X ou O)
        self.current_player = "X"

        # Tabuleiro
        self.board = [["" for _ in range(3)] for _ in range(3)]

        # Botões do tabuleiro
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(root, text="", font=("Helvetica", 24), width=4, height=2,
                                               command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j, sticky='nsew')  # Centraliza os botões

        self.label_player = tk.Label(root, text=f"Jogador X", font=("Helvetica", 16))
        self.label_player.grid(row=3, column=0, columnspan=3, sticky='nsew')  # Centraliza a label

        # Configuração do peso das colunas e linhas para expansão
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

        self.root.geometry("400x450")  # Define a geometria da janela



    def on_button_click(self, row, col):
        
        self.Jogando (row, col)
        self.Esperando_Jogada()
        
       
        
    def Jogando (self, row, col):
        # Dados a serem enviados
        data = { 'row' : row, 'col' :col}

        # Envia os dados como uma mensagem serializada em JSON
        channel.basic_publish(exchange='',
                            routing_key='Tabuleiro_XO',
                            body=json.dumps(data))
        
        self.logica_de_jogo(row, col)
        
        
        
    def Esperando_Jogada(self):
        
                # Desabilita os botões durante a espera
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disable')

            # Aguarde até que uma mensagem seja recebida
        while True:
            method_frame, header_frame, body = channel.basic_get(queue='Tabuleiro_OX', auto_ack=True)
            if method_frame:
                    # Se uma mensagem foi recebida, chama o callback e sai do loop
                self.callback(None, method_frame, None, body)
                break
            self.root.update_idletasks()
            
                    # Habilita os botões após receber a mensagem
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='normal')

    
        
    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        row = data.get('row')
        col = data.get('col') 
        
        print (row, col)
        
        self.logica_de_jogo(row, col)
  
    
    
    
    def logica_de_jogo(self, row, col):
        if self.board[row][col] == "":
            # Atualiza o botão clicado com o jogador atual
            self.buttons[row][col].config(text=self.current_player)

            # Atualiza o tabuleiro
            self.board[row][col] = self.current_player
            self.root.update()

            # Verifica se há um vencedor
            if self.check_winner(row, col):
                messagebox.showinfo("Vitória!", f"Jogador {self.current_player} venceu!")
                self.reset_game()
            else:
                # Verifica se é um empate
                if all(all(cell != "" for cell in row) for row in self.board):
                    messagebox.showinfo("Empate!", "O jogo terminou em empate.")
                    self.reset_game()
                else:
                    # Alterna para o próximo jogador
                    if self.current_player == "X":
                        self.current_player = "O"
                    else:
                        self.current_player = "X"


    
    def check_winner(self, row, col):
        # Verifica a linha
        if all(self.board[row][c] == self.current_player for c in range(3)):
            return True
        # Verifica a coluna
        if all(self.board[r][col] == self.current_player for r in range(3)):
            return True
        # Verifica as diagonais
        if row == col and all(self.board[i][i] == self.current_player for i in range(3)):
            return True
        if row + col == 2 and all(self.board[i][2 - i] == self.current_player for i in range(3)):
            return True
        return False


    def reset_game(self):
        connection.close()
        self.root.destroy()
        
        
    def on_close(self):
        connection.close()
        self.root.destroy()



if __name__ == "__main__":
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
    except Exception as e:
        print(f"Erro ao criar conexão ou canal: {e}")
        sys.exit(1)
    channel.queue_delete(queue='Tabuleiro_OX')
    channel.queue_delete(queue='Tabuleiro_XO')
    channel.queue_declare(queue='Tabuleiro_OX')
    channel.queue_declare(queue='Tabuleiro_XO')
        
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
    
