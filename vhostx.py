#!/usr/bin/env python3

# vHostX by NoobsCode
# Author: Alexander A. Nordbo
# UR: https://github.com/noobscode

from functions import *
import time
import os

try:
    input = raw_input
except NameError:
    pass

def main():
	choice = '0'
	while choice =='0':
		os.system("clear")
		header()
		print("Action Menu:")
		print("1. Create a vHost")
		print("2. List all vHosts")
		print("3. Delete a vHost")
		print("4. Help")
		print("0. Exit")

		choice = input ("Please make a choice: ")

		if choice == "4":
			print("Help Section")
			help()
		elif choice == "3":
			rmsite()
		elif choice == "2":
			os.system("apache2ctl -S")
		elif choice == "1":
			gensite()
		elif choice == "0":
			print("Bye!")
			exit(1)
		else:
			print("I don't understand your choice.")
main()
