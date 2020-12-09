import multiprocessing

def worker():
    """worker function"""
    print ('Worker')
    k = []

    # of course in an infinite loop
    while True:
        # lets use the cpu mathematical power, to increse its temp
        l = (2*33) >> 3 
        # it is also possible to consume memory..
        # but it will crash windows 8.1 after a while
        # k.append(l)
        pass
    return

if __name__ == '__main__':
    jobs = []

    cpu = multiprocessing.cpu_count()
    print("CPU count=" + str(cpu))
    for i in range(cpu):
        p = multiprocessing.Process(target=worker)
        jobs.append(p)
        p.start()