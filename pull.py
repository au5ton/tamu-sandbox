#!/usr/bin/env python3
import os
import sys
from subprocess import run
import json

def prompt():
	choice = input('Add as submodule? [y/n] ')
	if choice.lower() == 'y':
		return True
	elif choice.lower() == 'c':
		exit(0)
	else:
		print('Won\'t add.')
		return False

# HOST = 'https://example.com'
HOST = sys.argv[1]
CWD = os.path.dirname(os.path.abspath(__file__))
print(f'Expecting .git repo in: {CWD}')

print('Fetching Gitlab API...')
response = run(['curl', f'{HOST}/gitlab/api/v4/projects'], capture_output=True, text=True)
out = response.stdout
data = json.loads(out)
print('Processed!')

# cwd=None

for elem in data:
	print('Repo data:')
	print('\t', elem['name'])
	print('\t', elem['http_url_to_repo'].replace('http://0.0.0.0', HOST))
	if(prompt() == False):
		continue
	print(f'Adding {elem["name"]}')
	run(['git', 'submodule', 'add', elem['http_url_to_repo'].replace('http://0.0.0.0', HOST)])
