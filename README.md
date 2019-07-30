# Dockerized Flask Development Workflow in VSCode Example

This repository serves as an example on how I develop Flask based applications in Docker, while having full code hinting and debugging capabilities in Visual Studio Code. I use this workflow on an Ubuntu system, but this might not be required. It's just what I use.

I created this example to show others how you can achieve a development workflow that satisfies the following needs:

- Code-hinting (IntelliSense as Microsoft calls it) for both app and vendor code

- Debugging

- High Dev/Prod parity (https://12factor.net/dev-prod-parity) through Docker

- Ability for team members to run the entire stack with a simple `docker-compose up`

- ~~A 100% open-source stack~~ (Not sure if the VS Code Server that is temporarily installed to the container is open source)

- A simple developer experience (DX)

While creating this example I stumbled upon an incompatibility between Flask's auto-reload functionality and PTVSD (VSCode's Python debugger), see the [first point of Quirks/gotcha's](#quirksgotchas) to find out how I worked around that.

## Requirements

- Visual Studio Code (Insiders channel is required at this time of writing)

- Remote Development Extension ([https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack]())

- Docker CE

- Docker Compose

- A local working copy of this repository

## Endpoints

| What                                          | Port |
| --------------------------------------------- | ---- |
| Flask Application                             | 5000 |
| Flask Application while running in debug mode | 5001 |
| PTVSD (Debugger Remote Attach Port)           | 3000 |

## Running the stack

Just open your local clone of this repository in VSCode using 'Open Folder' and start the development container using 'Reopen Folder in Container' in the command palette (`ctrl+shift+p` / `command+shift+p`). VSCode will now start the Docker container and move it's context into the container as if you were developing on a native local filesystem. Any spawned terminals will also live within that context, so you can do pip installs directly into the container. (Don't forget to freeze your dependencies into requirements.txt so you can commit them to version control).

As soon as the container is running you can visit [http://localhost:5000]() for further instructions.

When you close VSCode the running container should automatically be stopped.

Container logs can be viewed by running `docker-compose logs -f` from a local (non-vscode) terminal.

## Running the stack (team members)

If you are working with team members that don't need to develop directly inside the container but just want to run it (for example to develop a frontend against an API you implemented in Flask)

```
# install backend dependencies (builds container and runs pip install. See Dockerfile)
docker-compose build
# start services
docker-compose up
```

## Adding more containers

### Sidecars and databases

Most applications these days consist of multiple containers. Even a simple blog application will probably contain at least a database. Whether you should containerize a database is a whole different topic by the way. But you shouldn't have to worry that much about it while still in the development lifecycle. Other possiblities could be a task queue in the form of [Celery](http://docs.celeryproject.org/en/latest/index.html) or a caching service like [Memcached](https://memcached.org/).

I have laid out some examples in `docker-compose.yml`. Feel free to add any container you need to that file and make sure you restart the whole stack afterwards. Again, using 'Reopen Folder in Container' in the command palette (`ctrl+shift+p` / `command+shift+p`). See the [third point of Quirks/gotcha's](#quirksgotchas) in case you can't find `docker-compose.yml` in VSCode's file manager.

### Application Code

Maybe your application consists of multiple containers in which your own code runs. You might for example have several Flask applications that, together, form a single logical application. In that case you also want VSCode to be able to switch it's context into those containers and have full code hinting and debugging capabilities within those containers.

Microsoft's Chuck Lantz has done a write up on that scenario [here](https://code.visualstudio.com/docs/remote/containers-advanced#_connecting-to-multiple-containers-at-once)

## Quirks/gotcha's

- We have to start a separate instance of flask when debugging because the default Flask development server configuration provides hot-reloading functionality, which is great when developing. Unfortunately PTVSD doesn't seem to be compatible with that feature at this moment and crashes with a `ValueError: signal only works in main thread` exception. So for now we just start another Flask process with auto-reloading disabled so we can attach a debugger. Debug that code, and move on. This brings us to the reason I created this repository: To make sure my colleagues and my future self have a workaround. If anyone has pointers on a better workaround, feel free to open a issue or make a PR.

- Any VSCode plugins that you wish to use while developing inside the container need to be designated for installation in the `.devcontainer` file. The Python support plugin is already defined there.

- When moving the VSCode context inside the container you can no longer edit files outside of the `flask-app` folder in that VSCode window. You would need to open an additional windows if you want to edit for example the `docker-compose.yml` file (Don't forget to restart the devcontainer).

- VSCode's remote development extension is still relatively new. While it works great right for a lot of people right now, it will probably be subject to change. In case the instructions in this repository are no longer up to date, feel free to open an issue or even better: make a pull request.
