from datetime import timedelta
from temporalio import workflow

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import fetch_weather, send_email, store_data


@workflow.defn
class WeatherWorkflow:
    @workflow.run
    async def run(self, location: str, email: str):
        weather_data = await fetch_weather(location)
        await send_email(email, weather_data)
        await store_data(location, weather_data)
