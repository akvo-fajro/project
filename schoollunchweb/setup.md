# schoollunchweb manual

## environment
`ubuntu 20.04 LTS` : use `/bin/bash` as default terminal<br>
`python 3.8.10` : this is install by default on ubuntu 20.04<br>


## set up environment
### install pip3 and some 3rd-party package of python
`$ sudo apt install python3-pip -y`<br>
`$ pip3 install django`<br>
`$ pip3 install cryptography`<br>
`$ pip3 install PyMySQL`<br>
`$ pip3 install uwsgi`<br>
`$ pip3 install schedule`<br>

### install docker and docker-compose
`$ sudo apt remove docker docker-engine docker.io containerd runc`<br>
`$ sudo apt update`<br>
`$ sudo apt install ca-certificates curl gnupg lsb-release`<br>
`$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`<br>
`$ echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`<br>
`$ sudo apt update`<br>
`$ sudo apt install docker-ce docker-ce-cli containerd.io`<br>
> try `sudo docker run hello-world` to check if the docker install is all right <br>

`$ sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`<br>
`$ sudo chmod +x /usr/local/bin/docker-compose`<br>
> try `docker-compose --version` to check if the docker-compose install is all right<br>

`$ sudo groupadd docker`<br>
`$ sudo usermod -aG docker {username}`<br>

### install nginx
`$ sudo apt install nginx -y`<br>


## setup schoollunchweb and uwsgi
`$ tar zxvf schoollunchweb_all.tar.gz`<br>
`$ mv schoollunchweb_all site`<br>
> set up the environment viariable<br>
> add the under block in the ~/.bashrc file<br>
> change the value of every {.*}<br>
``` bash=
export DJANGO_SECRET_KEY={your_django_secret_key};
export DJANGO_DATABASE_NAME={database_name_on_docker};
export DJANGO_DATABASE_USER={database_user_on_docker};
export DJANGO_DATABASE_PASSWD={database_password_on_docker};
export DJANGO_DATABASE_HOST='127.0.0.1'
export DJANGO_DATABASE_PORT={ports_open_on_docker(default is 8080)}
```
`$ cd site`<br>
`$ docker pull mysql`<br>
`$ docker-compose -f mysqldb_docker.yml up -d`<br>
> wait for 1 minute let docker-compose to start up the mysql server

`$ ./schoollunhcweb_init`<br>


## setup nginx
> change /etc/nginx/nginx.conf
> comment out the conf.d/*.conf
```
...
# include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;
...
```

`$ cd /etc/nginx/sites-available`<br>
`$ sudo vim deploy-at-root-proxy-pass.conf`<br>
```
server {
    listen 80;
    server_name _;
    charset utf-8;

    client_max_body_size 75M;

    location / {
        proxy_pass http://127.0.0.1:8003/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header  X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias {your_static_dir_path};
    }
}
```
`$ ln -s /etc/nginx/sites-available/deploy-at-root-proxy-pass.conf /etc/nginx/sites-enabled/`<br>
`$ sudo rm /etc/nginx/sites-enabled/default`<br>
> try `nginx -t` to check if everything is right

`$ sudo systemctl restart nginx`<br>


## get a domain name
[no-ip website](https://www.noip.com/)<br>
[freenom website](https://www.freenom.com/en/index.html?lang=en)<br>


## get a ssl cert
[cerboot reference](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)<br>


## other
### start the mysql
`$ docker-compose -f mysqldb_docker.yml up -d`<br>

### stop the mysql
`$ docker-compose -f mysqldb_docker.yml down`<br>

### start the web (not initialize)
`$ uwsgi -d --ini uwsgi.ini`<br>

### shutdown the web
`$ uwsgi --stop /tmp/schoollunchewb-master.pid`<br>
