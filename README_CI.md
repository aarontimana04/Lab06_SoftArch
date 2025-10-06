# CI para Django (GitHub Actions)
1) Copia `.github/workflows/ci.yml`, `requirements-dev.txt`, `pytest.ini` y la carpeta `tests/` a la raíz de tu repo.
2) Cambia `myproject.settings` por el nombre real de tu proyecto Django.
3) Asegúrate de que `requirements.txt` instala Django/DRF/etc. y que `requirements-dev.txt` se versiona.
4) Sube a GitHub: el pipeline correrá Flake8 y Pytest en cada push o PR contra `main`.
