
### Vtiger 7 setup on Ubuntu 20.04

```
apt update -y && apt install -y php php-cli php-mysql php-common  php-zip php-mbstring php-xmlrpc php-curl php-soap php-gd php-xml php-intl php-ldap php-imap apache2 libapache2-mod-php mariadb-server mariadb-client

```

nano /etc/php/*/apache2/php.ini
```
date.timezone = UTC
memory_limit = 256M
upload_max_filesize = 64M
display_errors = Off
log_errors = Off
```

### mysql setup

mysql -u root -p
```
CREATE USER 'vtiger'@'localhost' IDENTIFIED BY 'configme';
CREATE DATABASE vtiger;
GRANT ALL PRIVILEGES ON vtiger.* TO 'vtiger'@'localhost';
FLUSH PRIVILEGES;
QUIT
```

nano /etc/mysql/mariadb.conf.d/50-server.cnf
```
[mysqld]
sql_mode = ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```
systemctl restart mariadb.service

mysql -u root -p
```
SHOW VARIABLES LIKE 'sql_mode';
QUIT
```


### download code
```
wget https://sourceforge.net/projects/vtigercrm/files/vtiger%20CRM%207.4.0/Core%20Product/vtigercrm7.4.0.tar.gz
tar xvf vtigercrm7.4.0.tar.gz && mv vtigercrm /srv/vtigercrm

```


### configure apache

```
a2enmod rewrite
systemctl restart apache2

chown -R www-data:www-data /srv/vtigercrm

```

##### replace domain.com with ip/domain
nano /etc/apache2/sites-enabled/vtigercrm.conf
```
<VirtualHost *:80>
     ServerAdmin admin@domain.com
     ServerName domain.com
     ServerAlias www.domain.com
     DocumentRoot /srv/vtigercrm/

     <Directory /srv/vtigercrm/>
        Options +FollowSymlinks
        AllowOverride All
        Require all granted
     </Directory>

     ErrorLog /var/log/apache2/vtigercrm_error.log
     CustomLog /var/log/apache2/vtigercrm_access.log combined
</VirtualHost>
```

```
apachectl -t
systemctl restart apache2
```

open url on browser
```
http://put-ip-here
```








