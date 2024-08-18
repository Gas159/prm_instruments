import aio_pika
import aioredis
import asyncio



class RedisTools:
	redis = aioredis.from_url("redis://localhost")

# async def redis_and_rabbitmq():
# 	redis = aioredis.from_url("redis://localhost")
# 	connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
#
# 	channel = await connection.channel()
# 	queue = await channel.declare_queue("my_queue")
#
# 	# Use Redis to store some data
# 	await redis.set("my_key", "Hello, Redis!")
#
# 	# Use RabbitMQ to send a message
# 	await channel.default_exchange.publish(
# 		aio_pika.Message(body="Hello, RabbitMQ!".encode()), routing_key="my_queue"
# 	)
#
# 	# Consume the message from RabbitMQ
# 	message = await queue.get()
# 	print(message.body.decode())  # Output: Hello, RabbitMQ!
#
# 	# Use Redis to retrieve the stored data
# 	value = await redis.get("my_key", encoding="utf-8")
# 	print(value)  # Output: Hello, Redis!
#
# 	await connection.close()