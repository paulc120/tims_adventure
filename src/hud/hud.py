from src.hud import hud_widgets

"""
hud.py

This file manages the
games heads-up display
"""


class HUD:

    def __init__(self, player, master):

        self.player = player
        self.master = master

        self.health_display = lambda: hud_widgets.HealthDisplay(self.player, self.master)
        self.bean_select = lambda: hud_widgets.BeanSelectPopup(self.player, self.master, 297, 452)
        self.save_select = lambda: hud_widgets.SaveSelect(self, 238, 178)

        self.defined_components = {
            "health_display": self.health_display,
            "bean_select": self.bean_select,
            "save_select": self.save_select
        }

        self.components = []

        self.hud_saves = {}
        self.hud_id = None

    def update(self):

        [component.update() for component in self.components]

    def load_saved_hud(self, hud_id):

        self.hud_id = hud_id
        self.components = [component() for component in self.hud_saves[self.hud_id]]

    def save_hud(self, hud_id, components, current=False):

        if not current:
            self.hud_saves[hud_id] = [self.defined_components[component] for component in components]
        else:
            self.hud_saves[hud_id] = self.components

    def open_widget(self, widget):

        self.components.append(widget)

        if self.hud_id is not None:
            self.save_hud(self.hud_id, None, True)

    def close_widget(self, widget):

        self.components.remove(widget)

        if self.hud_id is not None:
            self.save_hud(self.hud_id, None, True)

    def close_hud(self):

        self.components = []
        self.hud_id = None

    def draw(self, display):

        [component.draw(display) for component in self.components]
