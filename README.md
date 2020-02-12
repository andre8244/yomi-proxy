# INTRO

YOMI PROXY it's a flask application server that, in combination with <a href="https://github.com/nethesis/yomi-rspamd">yomi-rspamd</a>, permit to get every mail attachment sent from rspamd lua plugin and send to <a href="https://yoroi.company">yoroi sandbox (YOMI)</a>.
Before install this package, you has to install <a href="https://github.com/nethesis/yomi-rspamd">yomi-rspamd</a>.

# PREREQUISITE

- python3
- pip3

# INSTALLATION

1 - Clone this repository on your $HOME local server.

```
git clone https://github.com/nethesis/yomi-proxy
yum install python3-pip
```

2 - Install all python package 
```
pip3 install -r dev.txt
```

3 - Execute server : 
```
YOROI_CLIENT_ID=<id> YOROI_CLIENT_SECRET=<secret> python3 app.py
```
