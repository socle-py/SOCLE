cd /opt
sudo curl -L "https://github.com/socle-py/socle/releases/download/$(basename $(curl -fsSLI -o /dev/null -w %{url_effective} https://github.com/socle-py/socle/releases/latest))/socle.tar.gz" | sudo tar -xz 
sudo ln -f -s /opt/socle/socle /usr/local/bin/socle.py

sudo mkdir -p  /usr/local/share/socle
sudo curl -Lo /usr/local/share/socle/socle.yml https://raw.githubusercontent.com/socle-py/SOCLE/main/socle.yml
