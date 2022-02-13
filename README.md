# firebase-data
[![pypi](https://img.shields.io/pypi/v/firebase-data.svg)](https://pypi.python.org/pypi/firebase-data)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/louis030195/firebase-data/blob/master/notebook/firebase_data_getting_started.ipynb)
[![Try it on gitpod](https://img.shields.io/badge/try-on%20gitpod-brightgreen.svg)](https://gitpod.io/#https://github.com/louis030195/firebase-data)

Easily transfer data between firebase projects.

⚠️ This package is still in early development. Read the code before running (especially on production environments).

## Why another Firebase data management tool

- Existing ones don't provide features to handle inter-project data management.
- Official solution does not allow eu/us data movement

## Install

`pip install firebase-data`

## Usage

### Export collection

```bash
fdata export --service_account_path=./svc.dev.json --collection=foos --output_path=./data
```

### Import collection

```bash
fdata import --service_account_path=./svc.prod.json --collection=foos --input_path=./data
```

### Export authentication

```bash
fdata auth:export --service_account_path=./svc.dev.json --output_path=./data
```

### Delete

No need to reinvent the wheel here, use firebase-cli.

```bash
export GOOGLE_APPLICATION_CREDENTIALS=./svc.dev.json
firebase use my-project
firebase firestore:delete foos --recursive
```

## Warning

- Not optimized for large collections (your PC will explose)
- Only one collection depth, i.e. foos/{fooId}/bars/{barId}


## TODOS

- [x] import/export Firestore (depth one)
- [x] export Firebase authentication
- [x] delete Firebase collection
- [ ] import Firebase authentication
- [ ] use transactions
- [ ] parallelize/optimize
- [ ] import+export as single call
- [ ] other firebase data

## Development

### Install

```bash
firebase login
firebase init
```

### How to release

1. Update version in `setup.py`
2. `git add .`
3. `git commit -m "my message"`
4. `git push`
5. `git tag v1.0.0`
6. `git push origin v1.0.0`
