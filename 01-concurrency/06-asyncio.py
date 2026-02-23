import asyncio
import random

# 1. We add 'async' to the definition
async def download_file(url):
    """Simulates downloading a file asynchronously."""
    
    # 2. CRITICAL: We use 'await asyncio.sleep' instead of 'time.sleep'
    # This tells the Event Loop: "I'm waiting, go do other tasks!"
    await asyncio.sleep(random.uniform(0.1, 0.5)) 
    
    return random.random() < 0.8 

# 3. We make our main function async too
async def main():
    urls = [f"https://example.com/data_{i}.csv" for i in range(1000)]
    
    # 4. We create the tasks (handing out the 1000 buzzers)
    # This doesn't run them yet, it just schedules them on the Event Loop
    tasks = [download_file(url) for url in urls]
    
    # 5. asyncio.gather runs them all concurrently and waits for the results
    results = await asyncio.gather(*tasks)
    
    # results is just a list of True/False values in the exact order we submitted them!
    success_count = sum(results) 
    print(f"Successfully downloaded {success_count} out of {len(urls)} files.")

if __name__ == "__main__":
    # 6. We start the Grandmaster (the Event Loop)
    asyncio.run(main())