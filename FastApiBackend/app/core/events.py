"""Publishes resume events to RabbitMQ; the Node socket server fans them out to browsers.

Topic exchange `resume.events`, routing key `user.<id>`. Publishing never blocks or
fails an API request: if the broker is down the event is dropped with a warning and
the connection is retried on the next event.
"""
import asyncio
import json
import logging

import aio_pika

from app import settings

logger = logging.getLogger(__name__)


class EventPublisher:
    def __init__(self) -> None:
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None
        self._lock = asyncio.Lock()

    async def _ensure(self) -> aio_pika.abc.AbstractExchange:
        async with self._lock:
            if self._exchange is None or (self._connection and self._connection.is_closed):
                # connect_robust re-establishes the connection on its own after drops
                self._connection = await aio_pika.connect_robust(
                    settings.rabbitmq_url, timeout=5
                )
                channel = await self._connection.channel()
                self._exchange = await channel.declare_exchange(
                    settings.rabbitmq_exchange, aio_pika.ExchangeType.TOPIC, durable=False
                )
            return self._exchange

    async def publish(self, user_id: int, message: dict) -> None:
        try:
            exchange = await self._ensure()
            await exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.NOT_PERSISTENT,
                ),
                routing_key=f"user.{user_id}",
            )
        except Exception as exc:  # broker problems must not affect the API
            logger.warning("Could not publish resume event: %s", exc)

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()


publisher = EventPublisher()
