# firebase-data
[![pypi](https://img.shields.io/pypi/v/firebase-data.svg)](https://pypi.python.org/pypi/firebase-data)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/louis030195/firebase-data/blob/master/notebook/firebase_data_getting_started.ipynb)
[![Try it on gitpod](https://img.shields.io/badge/try-on%20gitpod-brightgreen.svg)](https://gitpod.io/#https://github.com/louis030195/firebase-data)

Easily transfer data between firebase projects.

## Why another Firebase data management tool

- Existing ones don't provide features to handle inter-project data management.

## Install

pip install firebase-data

## Usage

### Export

```bash
fdata export_data --service_account_path=./svc.dev.json --collection=foos
```

### Import

```
fdata import_data --service_account_path=./svc.prod.json --collection=foos
```

## Warning

- Not optimized for large collections (your PC will explose)
- Only one collection depth, i.e. foos{fooId}/bars/{barId}


## TODOS

- [x] import/export (depth one)
- [ ] import+export as single call
- [ ] clean/delete
- [ ] other firebase data