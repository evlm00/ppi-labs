# Requirements
- httpx
- pyyaml
- pytest
- pydantic
- uvicorn

Install sqlalchemy and related:
```bash
pip install "sqlalchemy[asyncio,mypy]"
```
# Create DB
## Install Alembic
```bash
pip install alembic
alembic init alembic
```
Edit `alembic/env.py`: import add add base model metadata
## Initalize DB
```bash
alembic revision --autogenerate -m "initial migration"
alembic upgrade head
```
# Run
## Application
```bash
uvicorn app:app
```
## Tests
```
python -m pytest
```
