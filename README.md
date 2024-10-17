# Innovation Lab Practice

> This proyect use python 3.10

## If *pipenv* is used

Install and create environment
```bash
pipenv sync --dev
```

Run migrations
```bash
pipenv run ./manage.py migrate # or
pipenv shell
./manage.py migrate
```

Run the service
```bash
pipenv run ./manage.py runserver # or
pipenv shell
./manage.py runserver
```

Exit from environment
```bash
exit
```

## If *venv* is used

Create environment
```bash
python -m venv {env_name}
```

Activate environment
** LINUX
```bash
source {env_name}/bin/activate
```
** WINDOWS
```bash
.\{env_name}\Scripts\activate
```

Install dependecies
```bash
pip install -r requirements.txt
```

Exit from environment
```bash
deactivate
```

#### SUPER USER LOGIN:
- email: admin@example.com
- pass: 123

#### STAFF USER LOGIN:
- email: staff@example.com
- pass: 123

## ROUTES

**GET** LIST USERS
> http://{host}:{port}/user

**GET** RETRIEVE USERS PDF
> http://{host}:{port}/user/pdf

**POST** CREATE USER
> http://{host}:{port}/user/
