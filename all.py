this is the board
import pygame

from const import *
from board_dim import BoardDim


class Board:

    def __init__(self, dims=None, linewidth=15, ultimate=False, max=False):
        self.squares = [[0, 0, 0] for row in range(DIM)]
        self.dims = dims

        if not dims:
            self.dims = BoardDim(WIDTH, 0, 0)

        self.linewidth = linewidth
        self.offset = self.dims.sqsize * 0.2
        self.radius = (self.dims.sqsize // 2) * 0.7
        self.max = max

        if ultimate:
            self.create_ultimate()

        self.active = True

    def __str__(self):
        s = ''
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]
                s += str(sqr)
        return s

    def create_ultimate(self):
        for row in range(DIM):
            for col in range(DIM):
                size = self.dims.sqsize
                xcor, ycor = self.dims.xcor + (col * self.dims.sqsize), self.dims.ycor + (row * self.dims.sqsize)
                dims = BoardDim(size=size, xcor=xcor, ycor=ycor)
                linewidth = self.linewidth - 7
                ultimate = self.max

                self.squares[row][col] = Board(dims=dims, linewidth=linewidth, ultimate=ultimate, max=False)

    def render(self, surface):
        for row in range(DIM):
            for col in range(DIM):
                sqr = self.squares[row][col]

                if isinstance(sqr, Board): sqr.render(surface)

        # vertical lines
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor + self.dims.sqsize, self.dims.ycor),
                         (self.dims.xcor + self.dims.sqsize, self.dims.ycor + self.dims.size), self.linewidth)
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor),
                         (self.dims.xcor + self.dims.size - self.dims.sqsize, self.dims.ycor + self.dims.size),
                         self.linewidth)

        # horizontal lines
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor, self.dims.ycor + self.dims.sqsize),
                         (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.sqsize), self.linewidth)
        pygame.draw.line(surface, LINE_COLOR, (self.dims.xcor, self.dims.ycor + self.dims.size - self.dims.sqsize),
                         (self.dims.xcor + self.dims.size, self.dims.ycor + self.dims.size - self.dims.sqsize),
                         self.linewidth)

    def valid_sqr(self, xclick, yclick):

        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        # base case
        if not isinstance(sqr, Board):
            return sqr == 0 and self.active

        # recursive step
        return sqr.valid_sqr(xclick, yclick)

    def mark_sqr(self, xclick, yclick, player):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        print('marking -> (', row, col, ')')

        # base case
        if not isinstance(sqr, Board):
            self.squares[row][col] = player
            return

        # recursive step
        sqr.mark_sqr(xclick, yclick, player)

    def draw_fig(self, surface, xclick, yclick):
        row = yclick // self.dims.sqsize
        col = xclick // self.dims.sqsize

        if row > 2: row %= DIM
        if col > 2: col %= DIM

        sqr = self.squares[row][col]

        # base case
        if not isinstance(sqr, Board):

            # cross
            if sqr == 1:
                # desc line
                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset,
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset,
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)

                # asc line
                ipos = (self.dims.xcor + (col * self.dims.sqsize) + self.offset,
                        self.dims.ycor + self.dims.sqsize * (1 + row) - self.offset)
                fpos = (self.dims.xcor + self.dims.sqsize * (1 + col) - self.offset,
                        self.dims.ycor + (row * self.dims.sqsize) + self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth)

            # circle
            elif sqr == 2:
                center = (self.dims.xcor + self.dims.sqsize * (0.5 + col),
                          self.dims.ycor + self.dims.sqsize * (0.5 + row))

                pygame.draw.circle(surface, CIRCLE_COLOR, center, self.radius, self.linewidth)

            return

        # recursive step
        sqr.draw_fig(surface, xclick, yclick)

    def manage_win(self, surface, winner, onmain=False):
        # transparent screen
        transparent = pygame.Surface((self.dims.size, self.dims.size))
        transparent.set_alpha(ALPHA)
        transparent.fill(FADE)
        if onmain:
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
            surface.blit(transparent, (self.dims.xcor, self.dims.ycor))
        surface.blit(transparent, (self.dims.xcor, self.dims.ycor))

        # draw win
        if not onmain:
            # cross
            if winner == 1:
                # desc line
                ipos = (self.dims.xcor + self.offset,
                        self.dims.ycor + self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset,
                        self.dims.ycor + self.dims.size - self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)

                # asc line
                ipos = (self.dims.xcor + self.offset,
                        self.dims.ycor + self.dims.size - self.offset)
                fpos = (self.dims.xcor + self.dims.size - self.offset,
                        self.dims.ycor + self.offset)
                pygame.draw.line(surface, CROSS_COLOR, ipos, fpos, self.linewidth + 7)

            # circle
            if winner == 2:
                center = (self.dims.xcor + self.dims.size * 0.5,
                          self.dims.ycor + self.dims.size * 0.5)

                pygame.draw.circle(surface, CIRCLE_COLOR, center, self.dims.size * 0.4, self.linewidth + 7)

        # inactive board
        self.active = False

    def check_draw_win(self, surface, ):

        isfull = True

        for row in range(DIM):
            for col in range(DIM):

                # base case sqr should have numbers
                sqr = self.squares[row][col]

                if isinstance(sqr, Board) and sqr.active:
                    # other board win
                    winner = sqr.check_draw_win(surface)
                    if winner:  # recursive step
                        self.squares[row][col] = winner
                        sqr.manage_win(surface, winner)

                # main
                #  vertical wins
                for c in range(DIM):
                    if self.squares[0][c] == self.squares[1][c] == self.squares[2][c] != 0:
                        color = CROSS_COLOR if self.squares[0][c] == 1 else CIRCLE_COLOR
                        # draw win
                        ipos = (self.dims.xcor + self.dims.sqsize * (0.5 + c),
                                self.dims.ycor + self.offset)
                        fpos = (self.dims.xcor + self.dims.sqsize * (0.5 + c),
                                self.dims.ycor + self.dims.size - self.offset)
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[0][c]

                # horizontal wins
                for r in range(DIM):
                    if self.squares[r][0] == self.squares[r][1] == self.squares[r][2] != 0:
                        color = CROSS_COLOR if self.squares[r][0] == 1 else CIRCLE_COLOR
                        # draw win
                        ipos = (self.dims.xcor + self.offset,
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        fpos = (self.dims.xcor + self.dims.size - self.offset,
                                self.dims.ycor + self.dims.sqsize * (r + 0.5))
                        pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                        return self.squares[r][0]

                # diagonal wins
                # desc
                if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR
                    # draw win
                    ipos = (self.dims.xcor + self.offset,
                            self.dims.ycor + self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset,
                            self.dims.ycor + self.dims.size - self.offset)
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]

                # asc
                if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
                    color = CROSS_COLOR if self.squares[1][1] == 1 else CIRCLE_COLOR
                    # draw win
                    ipos = (self.dims.xcor + self.offset,
                            self.dims.ycor + self.dims.size - self.offset)
                    fpos = (self.dims.xcor + self.dims.size - self.offset,
                            self.dims.ycor + self.offset)
                    pygame.draw.line(surface, color, ipos, fpos, self.linewidth)

                    return self.squares[1][1]
this is the board_dim
from const import *

class BoardDim:

    def __init__(self, size, xcor, ycor):
        self.size = size
        self.sqsize = size // DIM
        self.xcor = xcor
        self.ycor = ycor

this i the client
import pygame
import socket
import pickle
import sys
from const import *
from game import Game


class GameClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('127.0.0.1', 3000)

        print("Client initialized. Ready to connect to the server.")
        self.game = Game(ultimate=True, max=True)

    def send_action(self, xclick, yclick, player):
        action = {
            'position': (xclick, yclick),
            'player': player
        }
        try:
            self.client.sendto(pickle.dumps(action), self.server_address)
            print(f"Sent action: {action}")
        except Exception as e:
            print(f"Error sending action: {e}")

    def receive_response(self):
        try:
            data, _ = self.client.recvfrom(4096)
            response = pickle.loads(data)
            print(f"Received response: {response}")
            return response
        except (EOFError, pickle.UnpicklingError) as e:
            print(f"Error receiving response: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def mainloop(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('ULTIMATE TIC TAC TOE')

        self.game.render_board(screen)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    xclick, yclick = event.pos
                    if self.game.board.valid_sqr(xclick, yclick):
                        self.send_action(xclick, yclick, self.game.player)
                        response = self.receive_response()

                        if response:
                            # Update the game board with the server's response
                            self.game.board.update_state(response['board'])
                            self.game.board.draw_fig(screen, xclick, yclick)

                            if response['winner']:
                                self.game.board.manage_win(screen, response['winner'])
                                pygame.display.update()
                                pygame.time.wait(2000)  # Wait before restarting or quitting

                            self.game.next_turn()
                        else:
                            print("No response from server")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game.restart()
                        screen.fill(BG_COLOR)
                        self.game.render_board(screen)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == '__main__':
    client = GameClient()
    client.mainloop()
this is the const
WIDTH = 729 # 3^6
HEIGHT = 729

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CROSS_COLOR = (66, 66, 66)
CIRCLE_COLOR = (239, 231, 200)
FADE = (28, 170, 156)

ALPHA = 100

DIM = 3

this is the game
import pygame

from const import *
from board import Board


class Game:

    def __init__(self, ultimate=False, max=False):
        self.ultimate = ultimate
        self.max = max
        self.board = Board(ultimate=ultimate, max=max)
        self.player = 1
        self.playing = True
        pygame.font.init()

    def render_board(self, surface):
        self.board.render(surface)

    def next_turn(self):
        self.player = 2 if self.player == 1 else 1

    def ultimate_winner(self, surface, winner):
        print('ULTIMATE WINNER! ->', winner)

        if winner == 1:
            color = CROSS_COLOR
            # desc
            iDesc = (WIDTH // 2 - 110, HEIGHT // 2 - 110)
            fDesc = (WIDTH // 2 + 110, HEIGHT // 2 + 110)
            # asc
            iAsc = (WIDTH // 2 - 110, HEIGHT // 2 + 110)
            fAsc = (WIDTH // 2 + 110, HEIGHT // 2 - 110)
            # draw
            pygame.draw.line(surface, color, iDesc, fDesc, 22)
            pygame.draw.line(surface, color, iAsc, fAsc, 22)

        else:
            color = CIRCLE_COLOR
            # center
            center = (WIDTH // 2, HEIGHT // 2)
            pygame.draw.circle(surface, color, center, WIDTH // 4, 22)

        font = pygame.font.SysFont('monospace', 64)
        lbl = font.render('ULTIMATE WINNER!', 1, color)
        surface.blit(lbl, (WIDTH // 2 - lbl.get_rect().width // 2, HEIGHT // 2 + 220))

        self.playing = False

    def restart(self):
        self.__init__(self.ultimate, self.max)

this is the server
import socket

# Server configuration
SERVER_IP = '127.0.0.1'
SERVER_PORT = 3000

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print(f"Server started on {SERVER_IP}:{SERVER_PORT}, waiting for clients to connect...")

    clients = []  # To store connected clients' addresses
    while True:
        try:
            # Receive data from any client
            data, addr = server_socket.recvfrom(1024)
            print(f"Received data: {data.decode()} from {addr}")

            # Add new clients to the list
            if addr not in clients:
                clients.append(addr)
                print(f"New client connected: {addr}")

            # Broadcast the data to all clients
            for client in clients:
                if client != addr:  # Avoid sending data back to the sender
                    server_socket.sendto(data, client)
                    print(f"Sent data to {client}")

        except Exception as e:
            print(f"Server error: {e}")
            break

if __name__ == "__main__":
    main()
