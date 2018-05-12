# Deploying on EC2

- after ssh into the amazon box update packages and install docker

`sudo yum update -y`

`sudo yum install -y docker`

- start docker service
`sudo service docker start`

- Run the docker container

`sudo docker run -p 8000:8000 pavankm/repository:magicktable3`

- install and start nginx

`sudo yum install nginx`

`sudo service nginx start`

- edit the nginx configs

`sudo vi /etc/nginx/conf.d/virtual.conf`

content:

```
server {
     listen  80;
     server_name    ec2-34-238-239-179.compute-1.amazonaws.com;
    location / {
         proxy_pass http://127.0.0.1:8000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
         proxy_connect_timeout       600;
         proxy_send_timeout          600;
         proxy_read_timeout          600;
         send_timeout                600;
    }
}
```

`sudo vi /etc/nginx/nginx.conf`

add the line
`client_max_body_size 200M;`

inside the `http` object


- restart nginx to reflect new changes

`sudo service nginx restart`