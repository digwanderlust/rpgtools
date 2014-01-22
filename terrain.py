#!/usr/bin/python
from __future__ import print_function
from __future__ import division

import random

def gen_terrain(width, height, water_extreme, compensate):
	def terrain_pass(terrain, num):
		for x in range(width):
			for y in range(height):
				water = 0
				#North
				if terrain[(y -1) % height][x % width] == water_char: 
					water += 1
				#South
				if terrain[(y +1) % height][x % width] == water_char:
					water += 1
				#East
				if terrain[y % height][(x + 1) % width] == water_char:
					water += 1
				#West
				if terrain[y % height][(x - 1) % width] == water_char:
					water += 1

				if water >= random.randint(1, 4):
					terrain[y][x] = water_char

				#provide a small chance for water to appear where it normally couldn't.
				#This allows for inland seas and greater chances of inlets.
				if (1 == random.randint(1, int((width*height)/1.5))) and \
				   (num == 1):
					terrain[y][x] = water_char

	#Cap user input
	water_extreme = min(water_extreme, 10)
	if compensate:
		water_char = chr(178)
		land_char = chr(219)
	else:
		water_char = '.'
		land_char = '%'
	passes = int((water_extreme/10) * min(width, height))

	#Initialize terrain
	terrain = [[land_char]*width for i in range(height)]
	terrain[0] = [water_char] * width 
	terrain[height - 1] = [water_char] * width

	#Add water on east and west edge
	for i in range(height):
		terrain[i][0] = water_char
		terrain[i][width - 1] = water_char

	for i in range(passes):
	 	terrain_pass(terrain, i)

	for row in terrain:
		if compensate:
			for out_char in row:
				print("{0}{0}".format(out_char), end="")
			print("")
		else: 
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

	parser.add_argument("-c", "--compensate", action='store_true',
		                help="Compensate for the fact that terminals draw chars roughly twice the height as width.")

	args = parser.parse_args()
	gen_terrain(args.width, args.height, args.water, args.compensate)