# Install
* Install pip virtualenv & virtualenvwrapper
* Install Let's Encrypt certbot-nginx
```bash
sudo apt install python3-dev
mkvirtualenv -p /usr/bin/python3 felix_web
sudo cp extra/etc/nginx/sites-available/felixnomada.duckdns.org /etc/nginx/sites-available/
sudo cp extra/systemd/system/felixweb.service /etc/systemd/system
```