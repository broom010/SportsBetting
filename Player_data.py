import numpy as np

class Player (object):
    """
    Defines a player class that has attributes that can be queried.
    """

    def __init__(self, name, data):
        self.df = data[data['Player'] == name]
        self.position = self.df.Pos
        self.receptions = self.df.Rec
        self.yards = self.df.Yds
        self.touchDowns = self.df.TD
        self.fumbles = self.df.FUM