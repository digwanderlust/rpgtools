#!/usr/bin/python
from __future__ import print_function
from __future__ import division

import random
from PIL import Image

class terrain():
    def __init__(self,height, width, water_extreme):
        self.height = height
        self.width = width
        
        self.water_char = '.'
        self.land_char = '%'
        
        self.terrain = [[self.land_char]*self.width for i in range(self.height)]
        water_extreme = min(water_extreme, 10)
        passes = int((water_extreme/10) * min(self.width, self.height))

	    #Initialize terrain
        self.terrain = [[self.land_char]*self.width for i in range(self.height)]
        self.terrain[0] = [self.water_char] * self.width 
        self.terrain[self.height - 1] = [self.water_char] * self.width
        
        #Add water on east and west edge
        for i in range(self.height):
            self.terrain[i][0] = self.water_char
            self.terrain[i][self.width - 1] = self.water_char
            
        for i in range(passes):
            self.terrain_pass(i)
            
    def alter(self, x, y, pass_num):
        water = 0
        #North
        if self.terrain[(y -1) % self.height][x % self.width] == self.water_char: 
            water += 1
        #South
        if self.terrain[(y +1) % self.height][x % self.width] == self.water_char:
            water += 1
        #East
        if self.terrain[y % self.height][(x + 1) % self.width] == self.water_char:
            water += 1
        #West
        if self.terrain[y % self.height][(x - 1) % self.width] == self.water_char:
            water += 1
                       
        if water >= random.randint(1, 4):
            self.terrain[y][x] = self.water_char
                        
        #provide a small chance for water to appear where it normally couldn't.
        #This allows for inland seas and greater chances of inlets.
        if (1 == random.randint(1, int((self.width*self.height)/1.5))) and \
           (pass_num == 1):
            self.terrain[y][x] = self.water_char
            
    def terrain_pass(self, pass_num):
        for x in range(self.width):
            for y in range(self.height):
                self.alter(x,y, pass_num)
                
    def __str__(self):
        for row in self.terrain:
		      print(' '.join(row))

if __name__ == "__main__":
    import argparse

    description = "Create a land mass for use with a square grid"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("width", default=46, type=int,
		                 help="Grid Width")
    parser.add_argument("height", default=32, type=int,
		                 help="Grid Height")
    parser.add_argument("water", default=2, type=int,
		                 help="1 - very little water, 10- lots of water")
    parser.add_argument("-i", "--gen-image", action="store_true",
                            help="create image file")

    args = parser.parse_args()
    random_terrain = terrain(args.width, args.height, args.water)
    print(random_terrain)
