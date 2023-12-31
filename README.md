# FastAPI App Example (Deprecated)

## 1. Requirements

- Python 3.10+

    This example uses `|` operator on type annotations (PEP 604).

- Python 3.8+

    This example uses `:=` (Walrus) operator on file chunked reading (PEP 572).

## 2. Setup Environment

1. Create Python virtual environment.

    ```bash
    python -m venv py310venv
    ```

2. Activate the Python virtual environment.

    ```bash
    source py310venv/bin/activate
    ```

3. Upgrade `pip` and install dependencies.

    ```bash
    python -m pip install --no-cache-dir --upgrade pip
    python -m pip install --no-cache-dir --upgrade -r requirements.txt
    ```

## 3. Usage

Get into `src/fastapi_app` folder and run `python main.py`.

### 3.1 Development mode

To run in development mode, set `MODE` environment variable to `dev` and run
app:

```bash
MODE="dev" python main.py
```

In this mode, it will reload automatically if you save the changes to files in
`src/fastapi_app` folder.

### 3.2 File logger

To enable file logger, change `logger.enable` to `true` in
`src/fastapi_app/configs/settings.json` file.

The log files will be put in `src/fastapi_app/logs` folder.
To change the location to place log files, change `logger.path` in
`src/fastapi_app/configs/settings.json` file.

### 3.3 Default console logger

To change the log level of default console logger, set `LOGURU_LEVEL`
environment variable, e.g. set it to `INFO`:

```bash
LOGURU_LEVEL="INFO" python main.py
```

To disable the default console logger, change the following lines in
`src/fastapi_app/main.py` file:

```py
if settings.logger is not None:
    logger_util.setup_logger(settings.logger, True)
```

### 3.4 Docker

The examples below use `example-fastapi-static` as the image name.

#### 3.4.1 Static Client

To build a Docker image:

```bash
docker build -t example-fastapi-static .
```

Run a container (the default port is `3001`):

```bash
docker run -p 3001:3001 -d example-fastapi-static
```

#### 3.4.2 Environment Only

To build a Docker image that only contains environment:

```bash
docker build -t example-fastapi:env-only -f Dockerfile.env_only .
```

Run a container:

```bash
docker run -p 3001:3001 -v ./src:/ws/src -d example-fastapi:env-only
```

### 3.5 Tailwind CSS

Get into `src/static_client_tailwindcss` folder and install dependencies:

```bash
npm install
```

Run the following command in `src/static_client_tailwindcss` folder to generate
Tailwind CSS file:

```bash
npx tailwindcss -i tailwind_input.css -o css/tailwind.css
```

Afterwards, get into `src/fastapi_app` folder and run `python main.py`. Open
browser and enter `http://localhost:3001/tailwindcss/`.

### 3.6 React

Get into `src/react_client` folder and install dependencies:

```bash
npm install
```

#### 3.6.1 Development mode

First, add `proxy` option into `src/react_client/package.json` file:

```jsonc
{
  // ...
  "proxy": "http://localhost:3001"
}
```

And start React app by running the following command in `src/react_client/`
folder:

```bash
npm start
```

(If you encount any problem with command above, check [docs/react.md](./docs/react.md)
for more information.)

This proxy the request from the React app to FastAPI backend.

Then get into `src/fastapi_app/` folder and start FastAPI backend:

```bash
MODE="dev" python main.py
```

Afterwards, open browser and enter `http://localhost:3000`.

Run the following code in the browser console:

```js
fetch("/hello").then((res) => res.json()).then((data) => console.log(data));
```

It should receive `world` from the backend.

#### 3.6.2 Build React app

Since we mount the React app under `/react-client` path in `src/main.py`:

```python
app.mount(
    "/react-client",
    StaticFiles(directory=REACT_BUILD_DIR, html=True),
    name="react_client",
)
```

We need to add `homepage` option into `src/react_client/package.json` file:

```jsonc
{
  // ...
  "homepage": "/react-client"
}
```

To build React app, run the following command in `src/react_client/` folder:

```bash
npm run build
```

Then run the following command in `src/fastapi_app/` folder:

```bash
python main.py
```

Now, the React app web page should be under
`http://localhost:3001/react-client/` URL.

## Todo List

- [x] Docker
- [x] Static client with Tailwind CSS
- [ ] React client
- [ ] React client with Headless UI
- [ ] Angular client

## Troubleshooting

- **isort sorts imports in wrong order.**

    Refer to [Wrong order in import when using sort imports in vscode #14254](https://github.com/microsoft/vscode-python/issues/14254)

    **Solution:** Add `.vscode/settings.json` to your workspace:

    ```json
    {
      "isort.args": [
        "--src=${workspaceFolder}/src/fastapi_app"
      ]
    }
    ```

- **Browser doesn't reflect changes made in the files in `client` folder.**

  Browser might cache the content before changes made.

  To disable browser caching, open the developer tools (press the `F12` key
  generally) and get into **Network** tab then check **Disable cache** checkbox.

  Now refresh the website, it should reflect changes.
