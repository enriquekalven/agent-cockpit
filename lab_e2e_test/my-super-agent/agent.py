import os
from tenacity import retry

# PROBLEM: This agent lacks timeouts, caching, and literal types.
def fetch_data():
    # MISSING RETRY/TIMEOUT
    print('Fetching results from unsafe endpoint...')

if __name__ == '__main__':
    fetch_data()
