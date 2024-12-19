"""
"""


##Consumer Producer Problem

import threading
import time
import random

BUFFER_SIZE = 10
buffer = []

mutex = threading.Semaphore(1)  # mutex for buffer
full = threading.Semaphore(0)  # full
empty = threading.Semaphore(BUFFER_SIZE)  # empty

productName = ["Apple", "Banana", "Orange", "Grape", "Strawberry", "Watermelon", "Pineapple", "Mango", "Peach", "Pear"]

def producer():
    while True:
        item = random.choice(productName)
        empty.acquire()  # wait for space in buffer
        mutex.acquire()  # wait for buffer to be available
        buffer.append(item)  # add item to buffer
        print(f"Producer produced: {item}. Buffer: {buffer}")
        mutex.release()  # release buffer
        full.release()  # signal that buffer is full
        time.sleep(random.uniform(0.5, 1.5))  # Sleep for 1 seconds

def consumer(consumer_id):
    while True:
        full.acquire()  # wait for buffer to be full
        mutex.acquire()  # wait for buffer to be available
        item = buffer.pop(0)  # remove item from buffer
        print(f"Consumer-{consumer_id} consumed: {item}. Buffer: {buffer}")
        mutex.release()  # release buffer
        empty.release()  # signal that buffer is empty
        time.sleep(random.uniform(0.5, 1.5))  # Sleep for 1 seconds

if __name__ == '__main__':
    # set up the threads
    print("*******Production and consumption started*******")
    thread_producer = threading.Thread(target=producer)
    thread_consumer = threading.Thread(target=consumer, args=(1,), name=f"Consumer-1")

    # start the threads
    thread_producer.start()
    thread_consumer.start()

    # wait for the threads to finish
    thread_producer.join()
    thread_consumer.join()

    #The program will never reach this point :(