Resume Builder
==========

Open source software founded by [Marvin Mbatha][marvinmbatha], [Ronald Kimeli][ronaldkimeli] and [Robert Kimaiyo][robertkimaiyo] who are aspiring to bring a new phase of Resume builder techs into unlocking jobs with brilliant and ATS friendly Resumes. Your contribution is great inspiration and it is highly encouraged.

Frontend Git branches
-----------------

* AngularFrontend - Based on angular framework.
* ReactFrontend - Based on React framework.
* VueFrontend - Based on Vue framework.

Backend Git Branch
------------------

* FastApiBackend - Is the main high performing backend which is fully API driven.
* SocketServer - Small Node.js WebSocket server that pushes live resume updates to the browser.

Table of Contents
-----------------

* [Requirements](#requirements)
* [Usage](#usage)
* [Socket Server](#socket-server)

Requirements
------------

Resume Builder Frontend requirements based on React:

* [Node.js][node] 16+
* [Vite][vite]
* [React Bootrsap][react_bootstrap]
* [Docker][docker]
* [React Router][react_router_dom]
* [Axios][axios]
* [React Toastify][toastify]

[node]: https://nodejs.org
[vite]: https://vitejs.dev
[react_bootstrap]: https://react-bootstrap.netlify.app
[docker]: https://www.docker.com
[react_router_dom]: https://reactrouter.com
[axios]: https://axios-http.com/docs/intro
[toastify]: https://fkhadra.github.io/react-toastify/introduction
[ronaldkimeli]: https://github.com/ronald-kimeli
[marvinmbatha]: https://github.com/Mbatha-Marvin/
[robertkimaiyo]: https://github.com/robert5313


Usage
------------

Clone this repository then create .env for db connection creadentials by navigating to backend first


```bash
cd FastApiBackend
```

Make .env from copy of example.env


```bash
cp example.env .env
```

Replace the credentials of db on .env `DB_CONNECTION_STR` with your favorite naming to be generated with the postrgres 


```bash
DB_USER: DB UserName
DB_PASSWORD: DB Password
DB_NAME: DB Name
```

Install necessary dependencies and run the software servers on detached mode using command below.


```bash
docker compose build --no-cache && docker compose up -d
```
- Fill your data in to be reused on the resume preview e.g set Profile, Education,Certifications, Referees etc
- Preview your details as resume and generate pdf by clicking the pdf logo

* Now check your terminal if everything is already started - On your browser at the url `http://localhost:5173/` if frontend and `http://localhost:5000/` is backend


Socket Server
-------------

`SocketServer` is a small stateless Node.js service (`ws` + `amqplib`) that keeps open previews and forms in sync without polling.

How it works:

1. FastAPI publishes a `resume.updated` event to the RabbitMQ topic exchange `resume.events` with routing key `user.<id>` whenever a section of that user's resume changes.
2. Every socket server instance binds its own exclusive queue to `user.*`, so every instance sees every event.
3. The server forwards the message to the browsers connected to `/ws/user/<id>`. The Vue frontend uses the `useResumeSocket` composable to refetch data when an event arrives.

Because instances hold no shared state, you can run as many replicas as you like behind a load balancer.

### Configuration

| Variable | Default | Description |
| --- | --- | --- |
| `PORT` | `4000` | Port the server listens on |
| `RABBITMQ_URL` | `amqp://guest:guest@rabbitmq:5672/` | RabbitMQ connection string |
| `RABBITMQ_EXCHANGE` | `resume.events` | Topic exchange to consume from |

Root `.env` (see `example.env`):

```bash
RABBITMQ_USER=resume
RABBITMQ_PASSWORD=resume
RESUME_SOCKET_URL=ws://localhost:4000   # URL the browser uses to reach the socket server
```

### Endpoints

* `ws://localhost:4000/ws/user/<id>` - WebSocket for a user's events (messages are limited to 1 KB).
* `http://localhost:4000/health` - returns `{ "broker": true, "connections": 0 }`; responds `503` while RabbitMQ is unreachable.

The server answers an application-level `ping` text message with `{"event":"pong"}`, and drops dead connections with protocol pings every 30s. It reconnects to RabbitMQ with exponential backoff (max 15s) and closes sockets gracefully on `SIGTERM`.

### Running

It starts with the rest of the stack:

```bash
docker compose up -d
```

To run it on its own (Node 24+ and a reachable RabbitMQ):

```bash
cd SocketServer
pnpm install
RABBITMQ_URL=amqp://resume:resume@localhost:5672/ pnpm start
```

Quick check with [websocat](https://github.com/vi/websocat):

```bash
websocat ws://localhost:4000/ws/user/1
```
