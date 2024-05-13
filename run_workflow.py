import asyncio
from temporalio.client import Client
from workflows import WeatherWorkflow

async def main():
    # Connect to the Temporal server (replace with your actual server address)
    client = await Client.connect("localhost:7233")

    try:
        # Start the WeatherWorkflow
        workflow = await client.start_workflow(
            WeatherWorkflow,
            id="weather_workflow",
            args=("New York", "user@example.com"),
        )

        # Wait for the workflow to complete and print the result
        result = await workflow.result()
        print(result)

    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())