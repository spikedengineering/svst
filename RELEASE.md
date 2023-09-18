# How to release a new version of `svst`.

> This is a temporary documentation file until we have a proper CI/CD pipeline in place.

## Docs
```bash
cd docs/
make html
```

## Git
```bash
pip freeze > requirements.txt

git add .
git commit -m "release-x.x.x"
git push 
```

## Pypi
```bash
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --skip-existing dist/*
```
