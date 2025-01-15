# SuperFastPython.com
# example of calling map() and handling results
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# task function to be executed in the thread pool
def task(value):
    # sleep for a moment
    sleep(1)
    # return a message
    return f'Task: {value} done.'

# protect the entry point
if __name__ == '__main__':
    # start the thread pool
    with ThreadPoolExecutor(10) as exe:
        # execute tasks concurrently and process results in order
        for result in exe.map(task, range(10)):
            # report the result
            print(result)