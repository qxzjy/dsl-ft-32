# Getting started

1. Build Docker :
```shell
docker build . -t sample-ml-project
```

2. Run Docker :
```shell
docker run -it -v "$(pwd):/home" sample-ml-project bash
```

3. Run specific test (Docker) :
```shell
pytest tests/test_data_preprocessing.py
```

4. (optional) Change PYTHONPATH (Docker) :
```shell
# In the /home folder, if error on step 3
export PYTHONPATH=$(pwd)
```

5. Run all tests (Docker) :
```shell
pytest
```