# --------------------------
#  Project Variables
# --------------------------
PACKAGE=wigo
PYTHON=python
VERSION=$(shell $(PYTHON) -c "import $(PACKAGE); print($(PACKAGE).__version__)")
TAG=v$(VERSION)

# --------------------------
#  Build distribution files
# --------------------------
build:
	rm -rf dist
	$(PYTHON) -m build

# --------------------------
#  Publish to PyPI
# --------------------------
publish: build
	$(PYTHON) -m twine upload dist/*

# --------------------------
#  Git Tag version
# --------------------------
tag:
	git tag -a $(TAG) -m "Release $(TAG)"
	git push origin $(TAG)

# --------------------------
#  Create GitHub Release
# --------------------------
github-release: build
	gh release create $(TAG) dist/* \
		--title "Wigo $(TAG)" \
		--notes "Automated release for version $(TAG)"

# --------------------------
#  Full Release Pipeline
# --------------------------
release: tag github-release
	@echo "🚀 Published version $(TAG) to PyPI and GitHub Releases!"
