#!/bin/sh

mkdir -p /tmp/wordpress-app
cat << EOF > /tmp/wordpress-app/docker-compose.yaml
version: '3'
services:
   mysql:
     image: mysql:5.7.9
     volumes:
       - mysql-data:/var/lib/mysql
     restart: always
     environment:
       MYSQL_ROOT_PASSWORD: himitsupass
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD: wordpress

   wordpress:
     depends_on:
       - mysql
     image: wordpress:latest
     ports:
       - "80:80"
     restart: always
     environment:
       WORDPRESS_DB_HOST: mysql:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD: wordpress
volumes:
    mysql-data:
EOF
