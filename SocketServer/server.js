// Tiny WebSocket fan-out server.
// FastAPI publishes resume events to RabbitMQ (topic exchange, routing key `user.<id>`);
// every instance of this server consumes them and pushes to the browsers connected to
// /ws/user/<id>. Stateless, so run as many replicas as you like behind a load balancer.
import http from 'node:http';
import amqp from 'amqplib';
import { WebSocketServer } from 'ws';

const PORT = Number(process.env.PORT ?? 4000);
const AMQP_URL = process.env.RABBITMQ_URL ?? 'amqp://guest:guest@rabbitmq:5672/';
const EXCHANGE = process.env.RABBITMQ_EXCHANGE ?? 'resume.events';
const ROUTE = /^\/ws\/user\/(\d+)$/;

/** user id -> sockets */
const rooms = new Map();
let brokerUp = false;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(brokerUp ? 200 : 503, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ broker: brokerUp, connections: [...rooms.values()].reduce((n, s) => n + s.size, 0) }));
    return;
  }
  res.writeHead(404).end();
});

const wss = new WebSocketServer({ noServer: true, maxPayload: 1024 });

server.on('upgrade', (req, socket, head) => {
  const match = ROUTE.exec(new URL(req.url, 'http://x').pathname);
  if (!match) {
    socket.write('HTTP/1.1 404 Not Found\r\n\r\n');
    return socket.destroy();
  }
  wss.handleUpgrade(req, socket, head, (ws) => join(match[1], ws));
});

function join(userId, ws) {
  if (!rooms.has(userId)) rooms.set(userId, new Set());
  rooms.get(userId).add(ws);
  ws.isAlive = true;

  ws.on('pong', () => (ws.isAlive = true));
  // app-level ping from the browser composable (browsers can't send protocol pings)
  ws.on('message', (data) => {
    if (data.toString() === 'ping') ws.send('{"event":"pong"}');
  });
  ws.on('close', () => {
    const room = rooms.get(userId);
    room?.delete(ws);
    if (room?.size === 0) rooms.delete(userId);
  });
  ws.on('error', () => ws.terminate());
}

// drop half-open connections
setInterval(() => {
  for (const room of rooms.values()) {
    for (const ws of room) {
      if (!ws.isAlive) { ws.terminate(); continue; }
      ws.isAlive = false;
      ws.ping();
    }
  }
}, 30_000).unref();

async function consume() {
  for (let attempt = 0; ; attempt++) {
    try {
      const conn = await amqp.connect(AMQP_URL);
      const ch = await conn.createChannel();
      await ch.assertExchange(EXCHANGE, 'topic', { durable: false });
      // exclusive, auto-named queue per server instance: every instance sees every event
      const { queue } = await ch.assertQueue('', { exclusive: true, autoDelete: true });
      await ch.bindQueue(queue, EXCHANGE, 'user.*');
      await ch.consume(
        queue,
        (msg) => {
          if (!msg) return;
          const userId = msg.fields.routingKey.split('.')[1];
          const payload = msg.content.toString();
          for (const ws of rooms.get(userId) ?? []) {
            if (ws.readyState === ws.OPEN) ws.send(payload);
          }
        },
        { noAck: true },
      );
      brokerUp = true;
      attempt = 0;
      console.log(`consuming ${EXCHANGE} as ${queue}`);
      await new Promise((resolve) => {
        conn.on('close', resolve);
        conn.on('error', () => {});
      });
      console.warn('rabbitmq connection closed, reconnecting');
    } catch (err) {
      console.warn(`rabbitmq unavailable (${err.message}), retrying`);
    }
    brokerUp = false;
    await new Promise((r) => setTimeout(r, Math.min(1000 * 2 ** Math.min(attempt, 4), 15_000)));
  }
}

server.listen(PORT, '0.0.0.0', () => console.log(`socket server on :${PORT}`));
consume();

for (const sig of ['SIGINT', 'SIGTERM']) {
  process.on(sig, () => {
    wss.clients.forEach((ws) => ws.close(1001));
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 2000).unref();
  });
}
