# must use personal access token for github password
# must use local su password for sudo
# must set up ~/.pypirc for pypi password

update:
	python update.py
	git commit -am "update version"
	git push origin master
	sudo python3 setup.py sdist bdist_wheel
	twine upload --skip-existing dist/*

test:
	python3 -m unittest