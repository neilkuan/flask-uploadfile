# flask-uploadfile
[![CodeFactor](https://www.codefactor.io/repository/github/guan840912/flask-uploadfile/badge/master)](https://www.codefactor.io/repository/github/guan840912/flask-uploadfile/overview/master)
[![codecov](https://codecov.io/gh/guan840912/flask-uploadfile/branch/master/graph/badge.svg)](https://codecov.io/gh/guan840912/flask-uploadfile)
![Publish Docker](https://github.com/guan840912/flask-uploadfile/workflows/Publish%20Docker/badge.svg)

### This for easy upload file via python flask . 
- enable login page 
- uploadfile 
- downloadfile
- docker image   
### you can run in docker .

### also can run in local 
```bash
$ git clone https://github.com/guan840912/flask-uploadfile.git

$ cd flask-uploadfile/

$ export URL='0.0.0.0'

$ python app.py

open your browser http://localhost:8080

# default login admin/admin
```

### Usage Docker  
```bash
docker run -d -p 8080:8080 guanyebo/flask-uploadfile
```

### Usage Docker-compose 
```bash
docker-compose up -d
```



### Use curl and wget  , uploadfile and downloadfile 
```bash
$ touch aa.tar

$ curl -X POST -F file=@"aa.tar" http://localhost:8080/uploadfile

$ wget http://localhost:8080/downloadfile/aa.tar
```
