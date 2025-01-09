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
