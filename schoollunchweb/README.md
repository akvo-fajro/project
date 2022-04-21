# schoollunchweb manual

### environment
`ubuntu 20.04 LTS`<br>
`python 3.8.10`<br>
`pip 22.0.4`<br>
`django 4.0.3`<br>
`docker 20.10.7`<br>
`docker-compose 1.29.2`<br>
`nginx 1.18.0`<br>

### setup schoollunchweb and it's uwsgi
`$ pip3 install django`<br>
`$ pip3 install django-crontab`<br>
`$ pip3 install cryptography`<br>
`$ pip3 install PyMySQL`<br>
`$ pip3 install uwsgi`<br>
`$ tar zxvf schoollunchweb_all.tar.gz`<br>
`$ mv schoollunchweb_all site`<br>
`$ cd site`<br>
`$ docker-compose -f mysqldb_docker.yml up -d`<br>
`$ ./schoollunchweb_init`<br>
> check is the web working

### shutdown the web
`$ uwsgi --stop /tmp/schoollunchweb-master.pid`<br>

### start the web (not initialize)
`$ ./schoollunchweb_start`

### stop the mysql
`$ docker-compose -f mysqldb_docker.yml down`<br>
> the data in mysql will not disappeare

### start the mysql
`$ docker-compose -f mysqldb_docker.yml up -d`<br>

### website
[django-contrib](https://www.gushiciku.cn/pl/238K/zh-tw)<br>
[install docker on ubuntu](https://docs.docker.com/engine/install/ubuntu/)<br>
[install docker-compose on ubuntu](https://docs.docker.com/compose/install/)<br>
[set up nginx](https://orcahmlee.github.io/devops/nginx-uwsgi-django-root/)<br>
[no-ip web](https://www.noip.com/)<br>
[certbot reference](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)<br>
