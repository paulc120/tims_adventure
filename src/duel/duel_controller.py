import pygame
from pygame.locals import *

from src.duel.duel_gui import load_images
from src.etc import gui_components, constants
from src.duel.duel_players import DuelPlayer
from src.duel.moves import moves

import math
import random

"""
duel.py

This deals with the game mechanics and GUI of duelling
"""


class DuelController:

    particle_engine = None
    controller = None

    def __init__(self, master):

        self.master = master

        self.images = load_images()

        self.background = self.images["background"]

        self.attack_main_button = gui_components.Button(self.images["attack_main_button"], 508, 584,
                                                        lambda: self.callback(0))
        self.attack_alt_button = gui_components.Button(self.images["attack_alt_button"], 730, 584,
                                                       lambda: self.callback(1))
        self.item_button = gui_components.Button(self.images["item_button"], 508, 645,
                                                 lambda: self.callback(2))
        self.retreat_button = gui_components.Button(self.images["retreat_button"], 730, 645,
                                                    lambda: self.callback(3))

        self.buttons = [
            self.attack_main_button,
            self.attack_alt_button,
            self.item_button,
            self.retreat_button
        ]

        self.player = None
        self.enemy = None

        self.player_hp_bar = gui_components.ProgressBar(563, 379, 232, 30, [constants.HEALTH_BAR_RED,
                                                                            constants.HEALTH_BAR_GREEN])
        self.enemy_hp_bar = gui_components.ProgressBar(81, 38, 232, 30, [constants.HEALTH_BAR_RED,
                                                                         constants.HEALTH_BAR_GREEN])

        self.player_xp_bar = gui_components.ProgressBar(563, 519, 232, 30, [constants.XP_BAR_BLUE,
                                                                            constants.XP_BAR_CYAN])
        self.enemy_xp_bar = gui_components.ProgressBar(81, 108, 232, 30, [constants.XP_BAR_BLUE,
                                                                          constants.XP_BAR_CYAN])

        self.player_energy_bar = gui_components.ProgressBar(563, 449, 232, 30, [constants.ENERGY_BAR_ORANGE,
                                                                                constants.ENERGY_BAR_YELLOW])

        self.progress_bars = [
            self.player_hp_bar,
            self.enemy_hp_bar,
            self.player_xp_bar,
            self.enemy_xp_bar,
            self.player_energy_bar
        ]

        self.player_hp_label = gui_components.Label(807, 359, "")
        self.enemy_hp_label = gui_components.Label(323, 18, "")

        self.player_xp_label = gui_components.Label(807, 500, "")
        self.enemy_xp_label = gui_components.Label(323, 89, "")
        self.player_energy_label = gui_components.Label(807, 429, "")

        self.player_level_label = gui_components.Label(624, 499, "")
        self.enemy_level_label = gui_components.Label(135, 88, "")

        self.attack_main_label = None
        self.attack_alt_label = None

        self.winner_label = None

        self.text = [
            self.player_hp_label,
            self.enemy_hp_label,
            self.player_xp_label,
            self.enemy_xp_label,
            self.player_energy_label,
            self.player_level_label,
            self.enemy_level_label
        ]

        self.turn = 0
        self.turn_cool_down = 50

        self.game_won = False
        self.game_won_counter = 0
        self.winner = ""
        self.shown_win = False

    def reset(self):

        self.turn = 0
        self.turn_cool_down = 50

        self.game_won = False
        self.game_won_counter = 0
        self.winner = ""
        self.shown_win = False

        try:
            self.text.remove(self.winner_label)
        except ValueError:
            pass

    def begin_duel(self, player, enemy):

        self.player = DuelPlayer(player)
        self.enemy = DuelPlayer(enemy)

        self.attack_main_label = gui_components.Label(607, 603, moves[self.player.meta.moves[0]]["name"], True)
        self.attack_alt_label = gui_components.Label(831, 603, moves[self.player.meta.moves[1]]["name"], True)

        self.text.append(self.attack_main_label)
        self.text.append(self.attack_alt_label)

        self.reset()

    def update(self):

        for event in pygame.event.get():
            if event.type == QUIT:
                self.master.game_exit = True

        if self.game_won:
            if self.game_won_counter > 0:
                self.game_won_counter -= 1
            else:
                if not self.shown_win:

                    self.shown_win = True
                    self.game_won_counter = 120

                    self.winner_label = gui_components.Label(480, 280, "{} won!".format(self.winner),
                                                             True, 128, constants.BLACK)
                    self.text.append(self.winner_label)
                else:
                    self.master.game_mode = 0

        if self.p_energy - moves[self.player.moves[0]]["energy"] < 0:
            self.attack_main_button.set_off()
        else:
            self.attack_main_button.set_on()
        if self.p_energy - moves[self.player.moves[1]]["energy"] < 0:
            self.attack_alt_button.set_off()
        else:
            self.attack_alt_button.set_on()

        [button.update(not self.turn and not self.turn_cool_down) for button in self.buttons]

        if self.turn_cool_down > 0:
            self.turn_cool_down -= 1

        if self.turn == 1 and not self.turn_cool_down and not self.game_won:

            possible_moves = [0, 1, 2, 3]

            if self.e_energy - moves[self.enemy.moves[0]]["energy"] < 0:
                possible_moves.remove(0)
            if self.e_energy - moves[self.enemy.moves[1]]["energy"] < 0:
                possible_moves.remove(1)

            move_no = possible_moves[random.randint(0, len(possible_moves)-1)]

            if move_no < 2:
                self.player.hp -= int(self.enemy.attack * moves[self.enemy.moves[move_no]]["str_mod"])
                if self.player.hp <= 0:
                    self.player.hp = 0

                    self.game_won = True
                    self.game_won_counter = 120

                    self.winner = "Opponent"

                self.e_energy -= moves[self.enemy.moves[move_no]]["energy"]

                self.enemy.xp += moves[self.enemy.moves[move_no]]["xp"]
                if self.enemy.xp >= int((constants.level_up_base *
                                        (constants.level_up_multiplier ** self.enemy.level))):
                    self.enemy.xp = self.enemy.xp % int((constants.level_up_base *
                                                        (constants.level_up_multiplier ** self.enemy.level)))
                    self.enemy.level += 1

                self.turn = 0
                self.turn_cool_down = constants.turn_cool_down

                move = moves[self.enemy.moves[move_no]]["effects"]

                if moves[self.enemy.moves[move_no]]["name"] in constants.shake_moves:
                    move = move.format("enemy", "-")
                elif moves[self.enemy.moves[move_no]]["name"] in constants.positional_moves:
                    move = move.format(220, 520)
                exec(move)

        self.shake_players()

        self.player.shadow.update()
        self.enemy.shadow.update()

        self.update_gui_components()

    def callback(self, button_id):

        if self.turn == 1 or self.turn_cool_down:
            return

        if self.game_won:
            return

        if button_id < 2:

            self.enemy.hp -= int(self.player.attack * moves[self.player.moves[button_id]]["str_mod"])
            if self.enemy.hp <= 0:
                self.enemy.hp = 0

                self.game_won = True
                self.game_won_counter = 120

                self.winner = "Player"

            self.p_energy -= moves[self.player.moves[button_id]]["energy"]

            self.player.xp += moves[self.player.moves[button_id]]["xp"]
            if self.player.xp >= int((constants.level_up_base *
                                     (constants.level_up_multiplier ** self.player.level))):
                self.player.xp = self.player.xp % int((constants.level_up_base *
                                                      (constants.level_up_multiplier ** self.player.level)))
                self.player.level += 1

            self.turn = 1
            self.turn_cool_down = constants.turn_cool_down

            move = moves[self.player.moves[button_id]]["effects"]

            if moves[self.player.moves[button_id]]["name"] in constants.shake_moves:
                move = move.format("player", "")
            elif moves[self.player.moves[button_id]]["name"] in constants.positional_moves:
                move = move.format(750, 170)
            exec(move)

    def update_gui_components(self):

        self.player_hp_bar.update(self.player.hp / self.player.max_hp)
        self.player_xp_bar.update(self.player.xp / (constants.level_up_base *
                                                    (constants.level_up_multiplier ** self.player.level)))

        self.enemy_hp_bar.update(self.enemy.hp / self.enemy.max_hp)
        self.enemy_xp_bar.update(self.enemy.xp / (constants.level_up_base *
                                                  (constants.level_up_multiplier ** self.enemy.level)))

        self.player_energy_bar.update(self.p_energy / self.player.energy)

        self.player_hp_label.update("{}/{}".format(self.player.hp, self.player.max_hp))
        self.enemy_hp_label.update("{}/{}".format(self.enemy.hp, self.enemy.max_hp))

        self.player_xp_label.update("{}/{}".format(self.player.xp,
                                                   int((constants.level_up_base *
                                                        (constants.level_up_multiplier **
                                                         self.player.level)))))
        self.enemy_xp_label.update("{}/{}".format(self.enemy.xp,
                                                  int((constants.level_up_base *
                                                       (constants.level_up_multiplier **
                                                        self.enemy.level)))))

        self.player_energy_label.update("{}/{}".format(self.p_energy, self.player.energy))

        self.player_level_label.update("Level {}".format(self.player.level))
        self.enemy_level_label.update("Level {}".format(self.enemy.level))

    def draw(self, display):

        display.blit(self.background, (0, 0))

        self.player.shadow.draw(display)
        self.enemy.shadow.draw(display)

        display.blit(self.player.image, (self.player.rect.x, 368))
        display.blit(self.enemy.image, (self.enemy.rect.x, 53))

        [button.draw(display) for button in self.buttons]
        [bar.draw(display) for bar in self.progress_bars]
        [label.draw(display) for label in self.text]

    def start_shake_player(self, duration, dx, w, direction):

        self.player.shake = duration
        self.player.shake_distance = dx
        self.player.shake_w = w
        self.player.shake_timer = 0
        self.player.shake_direction = direction

    def start_shake_enemy(self, duration, dx, w, direction):
        self.enemy.shake = duration
        self.enemy.shake_distance = dx
        self.enemy.shake_w = w
        self.enemy.shake_timer = 0
        self.enemy.shake_direction = direction

    def shake_players(self):

        if self.player.shake_timer < self.player.shake:
            c = self.player.shake_distance
            self.player.rect.x += (c-(c/math.pow(self.player.shake_w, 2))*math.pow(
                self.player.shake_timer
                , 2)) * self.player.shake_direction
            self.player.shake_timer += 1
        else:
            self.player.rect.x = 75

        if self.enemy.shake_timer < self.enemy.shake:
            c = self.enemy.shake_distance
            self.enemy.rect.x += (c-(c/math.pow(self.enemy.shake_w, 2))*math.pow(
                self.enemy.shake_timer
                , 2)) * self.enemy.shake_direction
            self.enemy.shake_timer += 1
        else:
            self.enemy.rect.x = 640
