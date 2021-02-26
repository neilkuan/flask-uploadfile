# flask-uploadfile
[![CodeFactor](https://www.codefactor.io/repository/github/guan840912/flask-uploadfile/badge/master)](https://www.codefactor.io/repository/github/guan840912/flask-uploadfile/overview/master)
[![codecov](https://codecov.io/gh/guan840912/flask-uploadfile/branch/master/graph/badge.svg)](https://codecov.io/gh/guan840912/flask-uploadfile)
![Publish Docker](https://github.com/guan840912/flask-uploadfile/workflows/Publish%20Docker/badge.svg)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)

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
docker run -d -p docker pull ghcr.io/guan840912/flask-uploadfile/flask-uploadfile:latest
```

### Usage Docker-compose 
```bash
docker-compose up -d
```



### Use curl and wget  , uploadfile and downloadfile and deletefile
```bash
$ touch aa.tar

$ curl -X POST -F file=@"aa.tar" http://localhost:8080/uploadfile

$ wget http://localhost:8080/downloadfile/aa.tar

$ curl -X DELETE http://localhost:8080/deletefile/aa.tar
```


## Note for run testing need to do first export ENV
```bash
export PASSWORD=admin
```
