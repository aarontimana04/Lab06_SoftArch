# Papers Search & Subscription PoC (Django + DRF)
Monolito DRF que emula microservicios de la arquitectura (auth, subscription, search/TF-IDF mock, ranking, logging, scraping mock, paper upload, paging/overview, authors, download).
## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd papers_api
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 9000
```
