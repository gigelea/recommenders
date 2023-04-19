import psutil
import time

def mem_usage():
#     print(psutil.cpu_percent())
#     print(psutil.virtual_memory())  # physical memory usage
    print('memory % used:', psutil.virtual_memory()[2])

def main():
    for i in range(10):
        mem_usage()
        time.sleep(2)

if __name__ == "__main__":
    main()