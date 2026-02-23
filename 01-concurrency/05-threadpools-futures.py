import concurrent.futures
import time
import random

def download_file(url):
    """Simulates downloading a file. Returns True if successful, False if it fails."""
    time.sleep(3) # Simulating I/O network wait
    
    # 80% chance to succeed, 20% chance to fail
    return random.random() < 0.8 

if __name__ == "__main__":
    urls = [f"https://example.com/data_{i}.csv" for i in range(200)]
    success_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        # Map hands the items to the pool and returns the results IN ORDER
        # results = executor.map(process_data, items)
        
        # for result in results:
        #     print(result)
        #--------------------------------------------------------------
        # submit returns a future object for each task, and we can process them as they complete, regardless of the order they were submitted in
        futures = [executor.submit(download_file, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            if future.result():
                success_count += 1

    print(f"Successfully downloaded {success_count} out of {len(urls)} files.")