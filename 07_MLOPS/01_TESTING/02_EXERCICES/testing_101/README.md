# Getting started

1. Run Docker :
```shell
docker run -it -v "$(pwd):/home" jedha/pytest-environment bash
```

2. Run specific test (Docker) :
```shell
pytest tests/test_basic_operations.py
```

3. (optional) Change PYTHONPATH (Docker) :
```shell
# In the /home folder, if error on step 1
export PYTHONPATH=$(pwd)
```

4. Run all tests (Docker) :
```shell
pytest
```