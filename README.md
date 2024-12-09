## How to run

## Local execution
1. Create the virtual environment and activate it
```bash
python -m venv venv
```
Windows:
```bash
.\venv\Scripts\activate
```
MacOs / Linux:

```bash
source /venv/bin/activate
```

2. Install the requirements
```bash
pip install -r requirements.txt
```

3. Start the server
```bash
python main.py
```

## Docker execution

1. Up the service container

```bash
docker compose up --build
```

## Access

Go to http://0.0.0.0:8090/docs