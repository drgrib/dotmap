import re

if __name__ == '__main__':
	setupFile = 'setup.py'
	outLines = []
	# read and update old version
	with open(setupFile, 'r') as f:
		for line in f:
			regex = r".+version.+'(.+)',"
			match = re.match(regex, line)
			if match != None:
				items = list(match.groups())
				version = items[0]
				major, middle, minor = [int(x) for x in version.split('.')]
				minor += 1
				newVersion = '{}.{}.{}'.format(major, middle, minor)
				print '{} -> {}'.format(version, newVersion)
				line = "\tversion = '{}',\n".format(newVersion)
			outLines.append(line)
	# write updated lines
	with open(setupFile, 'w') as f:
		s = ''.join(outLines)
		f.write(s)
