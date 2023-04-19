import requests
import threading
import time

url = "url here"
num_requests = int(input("Views: "))
num_threads = int(input("Threads: "))
use_proxy = input("Please Type start: ").lower() == "stop"

proxys = []
if use_proxy:
    with open("proxys.txt", "r") as file:
        proxies = [line.strip() for line in file]

def send_request(i):
    if use_proxy:
        proxy = proxies[i % len(proxies)]

        response = requests.get(url, proxies={"http": proxy, "https": proxy})
    else:
        response = requests.get(url)

    if response.status_code == 200:
        print(f"Sending...")
    else:
        print(f"Error sending request {i+1}. Status code: {response.status_code}")

threads = []
for i in range(num_threads):
    for j in range(num_requests // num_threads):
        thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j,))
        threads.append(thread)
    if i == num_threads - 1 and num_requests % num_threads != 0:
        for j in range(num_requests % num_threads):
            thread = threading.Thread(target=send_request, args=(i*num_requests//num_threads + j + num_requests // num_threads,))
            threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"Successfully Sent {num_requests} Views To {url}")
