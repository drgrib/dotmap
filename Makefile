update:
	python update.py
	git commit -am "update version"
	git push origin master
	sudo python setup.py sdist upload -r pypi
