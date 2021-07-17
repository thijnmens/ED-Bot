import requests
import re

def commitCount(u, r):
	return re.search('\d+$', requests.get('https://api.github.com/repos/{}/{}/commits?per_page=1'.format(u, r)).links['last']['url']).group()

def latestCommitInfo(u, r):
	""" Get info about the latest commit of a GitHub repo """
	response = requests.get('https://api.github.com/repos/{}/{}/commits?per_page=1'.format(u, r))
	commit = response.json()[0]; commit['number'] = re.search('\d+$', response.links['last']['url']).group()
	return commit