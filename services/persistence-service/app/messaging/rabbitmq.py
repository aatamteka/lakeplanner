import asyncio
import json
import logging
from typing import Callable, Dict
import aio_pika
from aio_pika import Message, ExchangeType

from app.core.config import settings

logger = logging.getLogger(__name__)


class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self.handlers: Dict[str, Callable] = {}

    async def connect(self):
        try:
            self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel()
            await self.channel.set_qos(prefetch_count=10)

            self.exchange = await self.channel.declare_exchange(
                "lake_platform_events",
                ExchangeType.TOPIC,
                durable=True
            )

            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            raise

    async def publish(self, routing_key: str, message: dict):
        if not self.channel or not self.exchange:
            raise RuntimeError("RabbitMQ not connected")

        try:
            await self.exchange.publish(
                Message(
                    body=json.dumps(message).encode(),
                    content_type="application/json",
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT
                ),
                routing_key=routing_key
            )
            logger.debug(f"Published message to {routing_key}: {message}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise

    async def subscribe(self, routing_key: str, queue_name: str, handler: Callable):
        if not self.channel or not self.exchange:
            raise RuntimeError("RabbitMQ not connected")

        try:
            queue = await self.channel.declare_queue(queue_name, durable=True)
            await queue.bind(self.exchange, routing_key)

            async def message_handler(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        data = json.loads(message.body.decode())
                        logger.debug(f"Received message from {routing_key}: {data}")
                        await handler(data)
                    except Exception as e:
                        logger.error(f"Error processing message: {e}")

            await queue.consume(message_handler)
            logger.info(f"Subscribed to {routing_key} on queue {queue_name}")
        except Exception as e:
            logger.error(f"Failed to subscribe to {routing_key}: {e}")
            raise

    async def close(self):
        if self.connection:
            await self.connection.close()
            logger.info("Closed RabbitMQ connection")


rabbitmq_client = RabbitMQClient()
