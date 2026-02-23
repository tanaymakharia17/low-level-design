import asyncio
import random

async def download_file(url, semaphore):
    """Simulates downloading a file, limited by a semaphore."""
    async with semaphore:
        await asyncio.sleep(random.uniform(0.1, 0.5)) 
        return random.random() < 0.8
async def main():
    urls = [f"https://example.com/data_{i}.csv" for i in range(1000)]
    
    # We create the bucket with 50 permits
    semaphore = asyncio.Semaphore(50)
    
    # We hand the exact same bucket to all 1000 tasks
    tasks = [download_file(url, semaphore) for url in urls]
    
    print("Starting 1000 downloads with a limit of 50 at a time...")
    results = await asyncio.gather(*tasks)
    
    success_count = sum(results) 
    print(f"Successfully downloaded {success_count} out of {len(urls)} files.")

if __name__ == "__main__":
    asyncio.run(main())