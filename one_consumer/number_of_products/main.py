import threading
import time
import random

BUFFER_SIZE = 10
NUMBER_OF_PRODUCTS = 20
buffer = []
stop_consuming = False  # Flag to stop the consumer

mutex = threading.Semaphore(1)  # mutex for buffer
full = threading.Semaphore(0)  # full semaphore
empty = threading.Semaphore(BUFFER_SIZE)  # empty semaphore

productName = ["Apple", "Banana", "Orange", "Grape", "Strawberry", "Watermelon", "Pineapple", "Mango", "Peach", "Pear"]

def producer():
    global stop_consuming
    for i in range(NUMBER_OF_PRODUCTS):
        item = random.choice(productName)
        empty.acquire()  # wait for space in buffer
        mutex.acquire()  # wait for buffer to be available
        buffer.append(item)  # add item to buffer
        print(f"Producer produced: {item}. Buffer: {buffer}")
        print(f"[-] { NUMBER_OF_PRODUCTS - i} products left")

        mutex.release()  # release buffer
        full.release()  # signal that buffer is full
        time.sleep(random.uniform(0.5, 1.5))  # simulate production time

    print("[+] Production finished")
    # Wait until all items in the buffer are consumed
    while buffer:
        time.sleep(0.1)
    stop_consuming = True  # Signal consumer to stop
    full.release()  # Release consumer if it's waiting



def consumer(consumer_id):
    global stop_consuming
    while not stop_consuming or buffer:
        full.acquire()  # wait for buffer to be full
        mutex.acquire()  # wait for buffer to be available
        if buffer:  # Check if there are items in the buffer
            item = buffer.pop(0)  # remove item from buffer
            print(f"Consumer-{consumer_id} consumed: {item}. Buffer: {buffer}")
        mutex.release()  # release buffer
        empty.release()  # signal that buffer has space
        time.sleep(random.uniform(0.5, 1.5))  # simulate consumption time



if __name__ == '__main__':
    # set up the threads
    print("*******Production and consumption started*******")
    thread_producer = threading.Thread(target=producer)
    thread_consumer = threading.Thread(target=consumer, args=(1,))

    # start the threads
    thread_producer.start()
    thread_consumer.start()

    # wait for the threads to finish
    thread_producer.join()
    thread_consumer.join()

    print("*******Production and consumption finished*******")
