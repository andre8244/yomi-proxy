#INTRO
YOMI PROXY it's a flask application server that, in combination with <a href="https://github.com/nethesis/yomi-rspamd">yomi-rspamd</a>, permit to get every mail attachment sent from rspamd lua plugin and send to <a href="https://yoroi.company">yoroi sandbox (YOMI)</a>.
Before install this package, you has to install <a href="https://github.com/nethesis/yomi-rspamd">yomi-rspamd</a>.

#PREREQUISITE

- python3
- pip3
- MySQL/MariaDB

#INSTALLATION

1 - Clone this repository on your $HOME local server.

>git clone https://github.com/nethesis/yomi-proxy

2 - Install all python package 

>pip3 install -r dev.txt

3 - Create user yomi_user 

> CREATE USER 'yomi_user'@'%' IDENTIFIED BY 'yomi_password';

4 - Create MySQL/MariaDB database :

> CREATE DATABASE nethesis_sandbox

5 - Grant privileges :

> GRANT ALL PRIVILEGES ON nethesis_sandbox.* TO 'yomi_user'@'%';

6 - Load database :

> mysql -u yomi_user -pyomi_password nethesis_sandbox < nethesis_sandbox.sql

7 - Execute server : 

> python3 app.py