import threading  # generate thread
import time  # sleep function
import queue  # block buffer data structure
import random  # random number generator

NUMBER_OF_CONSUMERS = 5
BUFFER_SIZE = 10
NUMBER_OF_PRODUCTS = 20
buffer = []  # shared buffer

mutex = threading.Semaphore(1)  # mutex for buffer
full = threading.Semaphore(0)  # full semaphore
empty = threading.Semaphore(BUFFER_SIZE)  # empty semaphore
production_finished = threading.Event()  # Event to signal production completion

productName = ["Apple", "Banana", "Orange", "Grape", "Strawberry", "Watermelon", "Pineapple", "Mango", "Peach", "Pear"]

produced_count = 0  # Track the number of produced items

def producer():
    global produced_count
    while produced_count < NUMBER_OF_PRODUCTS:
        item = random.choice(productName)
        empty.acquire()  # wait for space in buffer
        mutex.acquire()  # wait for buffer to be available
        buffer.append(item)  # add item to buffer
        produced_count += 1
        print(f"Producer produced: {item}. Buffer: {buffer}")
        mutex.release()  # release buffer
        full.release()  # signal that buffer has at least one item
        time.sleep(random.uniform(0.5, 1.5))  # Sleep for 0.5 to 1.5 seconds

    # Signal that production is finished
    production_finished.set()
    print("Producer finished production.")

    # Release all the full semaphores to ensure consumers can exit
    for _ in range(NUMBER_OF_CONSUMERS):
        full.release()

def consumer(consumer_id):
    while True:
        full.acquire()  # wait for buffer to be full
        mutex.acquire()  # wait for buffer to be available
        if production_finished.is_set() and not buffer:  # Check if production is finished and buffer is empty
            mutex.release()
            break  # Exit loop if no more products to consume
        if buffer:  # Double-check in case buffer was emptied in between
            item = buffer.pop(0)  # remove item from buffer
            print(f"Consumer-{consumer_id} consumed: {item}. Buffer: {buffer}")
        mutex.release()  # release buffer
        empty.release()  # signal that buffer has at least one empty slot
        time.sleep(random.uniform(0.5, 1.5))  # Sleep for 0.5 to 1.5 seconds

    print(f"Consumer-{consumer_id} finished consuming.")

if __name__ == '__main__':
    # Set up the threads
    thread_producer = threading.Thread(target=producer)
    consumer_threads = [
        threading.Thread(target=consumer, args=(i,), name=f"Consumer-{i}")
        for i in range(NUMBER_OF_CONSUMERS)
    ]

    # Start the threads
    thread_producer.start()
    for thread in consumer_threads:
        thread.start()

    # Wait for the producer thread to finish
    thread_producer.join()

    # Wait for all consumer threads to finish
    for thread in consumer_threads:
        thread.join()

    print("Production and consumption finished.")
