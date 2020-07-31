import os
import sys
import time
from os import path
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

MOVE_SHIP_INCREMENT = 1
MOVE_UFO_INCREMENT = 1
MOVE_FAST_UFO_INCREMENT = 1
SHIP_RECHARGE = 1  # 1 sec to recharge
GAME_SPEED = 1000 // 100  # each 0.1 sec update
BULLET_SPEED = 2

ALL_SHIP_DIRECTIONS = ("Left", "Right")


class SpaceInvaders(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.score = 0

        self.ship_position = (300, 595)
        self.ship_direction = ''
        self.ship_shoot = False
        self.ship_recharge_time = int(time.time())
        self.ufo_positions = [(300, 300), (200, 200)]
        self.ship_bullets = []
        self.ufo_bullets = []
        self.threshold = 580  # if space invader go down to this, fail

        self.bind_all("<KeyPress>", self.on_key_press)
        self.bind_all("<KeyRelease>", self.on_key_release)

        self.load_assets()
        self.create_objects()

        self.after(GAME_SPEED, self.perform_actions)

    def load_assets(self):
        try:
            #  in case one day I decide to make a bundle

            bundle_dir = getattr(
                sys,
                "_MEIPASS",
                path.abspath(path.join(path.dirname(__file__), '..'))
            )
            print('bundle_dir:', bundle_dir)
            path_to_ship = path.join(bundle_dir, "assets/imgs", "playership.gif")
            ship_image = Image.open(path_to_ship)
            self.ship = ImageTk.PhotoImage(ship_image)

            path_to_ship_shoot = path.join(bundle_dir, "assets/imgs", "shoot.gif")
            ship_shoot_image = Image.open(path_to_ship_shoot)
            self.ship_shoot_body = ImageTk.PhotoImage(ship_shoot_image)

            path_to_ship_exposion = path.join(bundle_dir, "assets/imgs", "explosion.gif")
            ship_explosion_image = Image.open(path_to_ship_exposion)
            self.ship_explosion = ImageTk.PhotoImage(ship_explosion_image)

            path_to_ufo = path.join(bundle_dir, "assets/imgs", "ufo.gif")
            ufo_image = Image.open(path_to_ufo)
            self.ufo = ImageTk.PhotoImage(ufo_image)

            path_to_fastinvader = path.join(bundle_dir, "assets/imgs", "fastinvader.gif")
            fastinvader_image = Image.open(path_to_fastinvader)
            self.fastinvader = ImageTk.PhotoImage(fastinvader_image)

            path_to_invader_killed = path.join(bundle_dir, "assets/imgs", "invaderkilled.gif")
            invader_killed_image = Image.open(path_to_invader_killed)
            self.invader_killed = ImageTk.PhotoImage(invader_killed_image)

            self.sound_explosion = path.join(bundle_dir, "assets/sounds", "explosion.wav")
            self.sound_fastinvader1 = path.join(bundle_dir, "assets/sounds", "fastinvader1.wav")
            self.sound_fastinvader2 = path.join(bundle_dir, "assets/sounds", "fastinvader2.wav")
            self.sound_fastinvader3 = path.join(bundle_dir, "assets/sounds", "fastinvader3.wav")
            self.sound_fastinvader4 = path.join(bundle_dir, "assets/sounds", "fastinvader4.wav")
            self.sound_invaderkilled = path.join(bundle_dir, "assets/sounds", "invaderkilled.wav")
            self.sound_shoot = path.join(bundle_dir, "assets/sounds", "shoot.wav")
            self.sound_spaceinvaders1 = path.join(bundle_dir, "assets/sounds", "spaceinvaders1.mpeg")
            self.sound_ufo_highpitch = path.join(bundle_dir, "assets/sounds", "ufo_highpitch.wav")
            self.sound_ufo_lowpitch = path.join(bundle_dir, "assets/sounds", "ufo_lowpitch.wav")

            # test play
            #os.system("afplay " + self.sound_ufo_lowpitch)

        except IOError as error:
            print(error)
            return

    def create_objects(self):
        self.create_text(
            100, 12, text=f"Score {self.score}", tag="score", fill="#fff",
            font=("TkDefaultFont", 14)
        )

        self.create_image(*self.ship_position, image=self.ship, tag="ship")

        for x_position, y_position in self.ufo_positions:
            self.create_image(x_position, y_position, image=self.ufo, tag="ufo")

        self.create_rectangle(7, 27, 593, 613, outline="#525d69")

    def on_key_press(self, e):
        new_direction = e.keysym

        if new_direction in ALL_SHIP_DIRECTIONS:
            self.ship_direction = new_direction

        self.ship_shoot = False
        if new_direction == "space":
            self.ship_shoot = True

    def on_key_release(self, e):
        released = e.keysym
        if released in ALL_SHIP_DIRECTIONS:
            self.ship_direction = ''
        elif released == "space":
            self.ship_shoot = False

    def move_ship(self):
        if self.ship_direction in ALL_SHIP_DIRECTIONS:
            ship_x_position, ship_y_position = self.ship_position

            if self.ship_direction == "Left":
                new_ship_position = (ship_x_position - MOVE_SHIP_INCREMENT, ship_y_position)
            elif self.ship_direction == "Right":
                new_ship_position = (ship_x_position + MOVE_SHIP_INCREMENT, ship_y_position)

            self.ship_position = new_ship_position
            self.coords(self.find_withtag("ship"), self.ship_position)

    def move_ufos(self):
        pass

    def move_bullets(self):
        if self.ship_bullets:
            new_positions = []
            for ship_bullet in self.ship_bullets:
                new_position = (
                    ship_bullet[0], ship_bullet[1] - BULLET_SPEED,
                    ship_bullet[2], ship_bullet[3] - BULLET_SPEED
                )
                new_positions.append(new_position)

            self.ship_bullets = new_positions
            for segment, position in zip(self.find_withtag("ship_bullet"), self.ship_bullets):
                self.coords(segment, position)

    def shoot(self):
        if self.ship_recharge_time > time.time():
            return

        if self.ship_shoot:
            ship_bullet_coord = (self.ship_position[0], self.ship_position[1] - 15, self.ship_position[0], self.ship_position[1] - 25)
            self.create_line(
                *ship_bullet_coord,
                tag="ship_bullet", fill="#476042",
                width=2, arrow=tk.LAST
            )
            self.ship_bullets.append(ship_bullet_coord)
            self.ship_recharge_time = int(time.time()) + SHIP_RECHARGE

    def check_collisions(self):
        return False

    def end_game(self):
        pass

    def check_ufo_collisions(self):
        pass


    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.check_ufo_collisions()
        self.move_ufos()
        self.move_bullets()
        self.move_ship()
        self.shoot()

        self.after(GAME_SPEED, self.perform_actions)