package:
	python setup.py sdist bdist_wheel

VERSION = 0.1
upload:
	python -m twine upload  dist/antiocr-$(VERSION)* --verbose

# Streamlit Demo
demo:
	streamlit run antiocr/app.py

.PHONY: package upload demo
