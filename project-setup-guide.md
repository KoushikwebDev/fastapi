# Setup Project by the uv

1. inatll uv => brew install uv

2. uv init fastapi-auth => create project

3. cd fastapi-auth

4. uv python pin 3.12 => select a python interpreter 3.12

5. Create and activate the virtual environment:
uv sync
source .venv/bin/activate

6. Install dependances:
uv add fastapi "uvicorn[standard]" sqlalchemy pymysql pydantic-settings "pwdlib[argon2]" PyJWT python-multipart


7. uv run uvicorn app.main:app --reload


