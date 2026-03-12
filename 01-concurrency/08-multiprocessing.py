import concurrent.futures
import time

def is_prime(n):
    """A heavy CPU-bound mathematical operation."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def count_primes(start, end):
    """Counts primes in a given range."""
    count = 0
    for i in range(start, end):
        if is_prime(i):
            count += 1
    return count

# =====================================================================
# THE SHIELD: Prevents imported child processes from running this block
# =====================================================================
if __name__ == "__main__":
    ranges = [
        (1, 1_000_000),
        (1_000_000, 2_000_000),
        (2_000_000, 3_000_000),
        (3_000_000, 4_000_000)
    ]
    
    start_time = time.time()
    
    # 1. Boot up 4 entirely separate Python processes (Cloning the factory)
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        
        # 2. Submit the tasks. The OS safely passes the start/end arguments
        #    to the new processes using serialization (pickling).
        futures = [executor.submit(count_primes, r[0], r[1]) for r in ranges]
        
        total_primes = 0
        
        # 3. as_completed yields the results as soon as any process finishes.
        #    Because this loop runs in the MAIN process, we can safely
        #    increment total_primes without needing any Mutex Locks!
        for future in concurrent.futures.as_completed(futures):
            total_primes += future.result()
            
    print(f"Found {total_primes} primes in {time.time() - start_time:.2f} seconds.")