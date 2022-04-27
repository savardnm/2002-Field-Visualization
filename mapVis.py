from copy import deepcopy
import tkinter as tk
import numpy
import argparse
import paho.mqtt.client as mqtt
from ast import literal_eval as make_tuple

TK_SILENCE_DEPRECATION = 1

verbose = False

class Map:
    def __init__(self, grid_size):
        self.canvas_size = [512, 512]
        self.grid_size = [grid_size, grid_size]
        self.grid = numpy.zeros(self.grid_size)
        self.last_grid = None
        self.unit_size = int(self.canvas_size[0] / self.grid_size[0])

        self.win = tk.Tk()
        self.canvas = tk.Canvas(
            self.win, bg="white", height=self.canvas_size[0], width=self.canvas_size[1])

        self.win.bind('<Escape>', lambda e: self.close_win(e))
        self.win.bind('r', lambda e: self.reset)

        self.canvas.pack()

        reset_btn = tk.Button(self.win, text='Reset', command=self.reset)

        reset_btn.pack()

        self.mqtt = MQTT(self)

    def close_win(self, e):
        # global win
        self.win.destroy()

    def update_canvas(self):
        global verbose
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x]:
                    self.canvas.create_rectangle(self.unit_size * x, self.unit_size * y, self.unit_size * (
                        x + 1), self.unit_size * (y + 1), outline="#000", fill="#000")
                else:
                    self.canvas.create_rectangle(self.unit_size * x, self.unit_size * y, self.unit_size * (
                        x + 1), self.unit_size * (y + 1), outline="#FFF", fill="#FFF")

        if verbose:
            if not numpy.array_equal(self.last_grid, self.grid):
                print(self.grid)

        self.last_grid = deepcopy(self.grid)

    def update(self):
        self.update_canvas()
        self.win.update_idletasks()
        self.win.update()

        self.mqtt.loop()

    def login(self):
        print("Please Enter Your Login Info:")
        username = input('Enter username: ')
        password = input('Enter password: ')

        self.mqtt.login(username, password)
        self.mqtt.connect()

    def reset(self):
        self.grid = numpy.zeros(self.grid_size)


class MQTT:
    def __init__(self, map):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.state = 1
        self.map = map

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        self.state = rc

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.client.subscribe(self.username + "/#")

        print("MQTT Subscribed! Now accepting messages on topics: " + self.username + "/#")
        print("To fill gridcells, send a value of [0,1] to the topic '%s/(x,y)' where 'x' and 'y' are integers from 0 to grid-size" % self.username)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        topic = msg.topic.split('/')[-1]
        val = msg.payload.decode()

        print(topic+" "+val)

        if self.is_coord(topic):
            coord = make_tuple(topic)
            try:
                self.map.grid[coord[1], coord[0]] = int(val)
            except:
                print("ERROR: Out of Bounds")
        elif (topic.lower() == "cmd"):
            if val == "reset":
                self.map.reset()

    def is_coord(self, msg):
        try:
            v = make_tuple(msg)
            return isinstance(v, tuple) and list(map(type, v)) == [int, int]
        except:
            return False

    def connect(self):
        self.client.connect("robomqtt.cs.wpi.edu", 1883, 60)

        pass

    def login(self, username, password):
        self.username = username
        print("Logging in as ", username, password)
        self.client.username_pw_set(username, password)

    def loop(self):
        self.client.loop(timeout=0.05)


def main():
    parser = argparse.ArgumentParser(description='Input Options')

    parser.add_argument('--gridsize', type=int, required=False, default=14)
    args = parser.parse_args()

    map = Map(args.gridsize)

    map.login()

    while 1:
        map.update()


if __name__ == "__main__":
    main()
