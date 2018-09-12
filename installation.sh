# Kjørt skript ved å gi kommando "bash installation"

python3 -m venv ncvenv

source ncvenv/bin/activate

# Nødvendig for Scrapy. Se https://docs.scrapy.org/en/latest/intro/install.html for info.
xcode-select --install

pip install -r requirements.txt
