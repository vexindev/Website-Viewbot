import requests
import threading
import time

url = "url here"
num_requests = int(input("Views: "))
num_threads = int(input("Threads: "))
use_proxy = input("Please Type start: ").lower() == "stop"

proxys = []
if use_proxy:
    # Read the list of proxies from the file
    with open("proxys.txt", "r") as file:
        proxies = [line.strip() for line in file]

def send_request(i):
    if use_proxy:
        # Choose a proxy from the list
        proxy = proxies[i % len(proxies)]

        # Make the request using the chosen proxy
        response = requests.get(url, proxies={"http": proxy, "https": proxy})
    else:
        # Make the request without a proxy
        response = requests.get(url)

    if response.status_code == 200:
        print(f"Sending...")
    else:
        print(f"Error sending request {i+1}. Status code: {response.status_code}")

# Create a list of threads
threads = []
for i in range(num_threads):
    for j in range(num_requests // num_threads):
        thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j,))
        threads.append(thread)
    if i == num_threads - 1 and num_requests % num_threads != 0:
        for j in range(num_requests % num_threads):
            thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j + num_requests // num_threads,))
            threads.append(thread)

# Start all the threads
for thread in threads:
    thread.start()

# Wait for all the threads to finish
for thread in threads:
    thread.join()

print(f"Successfully Sent {num_requests} Views To {url}")
