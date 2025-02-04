import asyncio
import aiohttp
import json

API_ENDPOINTS = [
    "https://api.example.com/data1",
    "https://api.example.com/data2",
    "https://api.example.com/data3"
]

TIMEOUT = 5  # Timeout in seconds

async def fetch_data(session, url):
    """Fetch data from an API with error handling and timeout."""
    try:
        async with session.get(url, timeout=TIMEOUT) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            return await response.json()
    except asyncio.TimeoutError:
        return {"error": f"Timeout occurred for {url}"}
    except aiohttp.ClientError as e:
        return {"error": f"Request failed for {url}: {str(e)}"}

async def fetch_all_data():
    """Fetch data concurrently from multiple APIs."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_data(session, url) for url in API_ENDPOINTS]
        return await asyncio.gather(*tasks)

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # If running in an environment where event loop is already running
        data = asyncio.run(fetch_all_data())
    else:
        data = loop.run_until_complete(fetch_all_data())

    return {
        "statusCode": 200,
        "body": json.dumps(data)
    }

if __name__ == "__main__":
    # For local testing
    print(asyncio.run(fetch_all_data()))
