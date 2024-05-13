import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker
from activities import fetch_weather, send_email, store_data
from workflows import WeatherWorkflow

async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    # Run the worker
    worker = Worker(
        client=client,
        task_queue="weather_queue",
        workflows=[WeatherWorkflow],
        activities=[fetch_weather, send_email, store_data],
    )
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
