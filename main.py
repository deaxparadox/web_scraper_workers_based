import requests
import asyncio
import multiprocessing
import time 
import requests
from bs4 import BeautifulSoup
from queue import Queue
from multiprocessing import Process, Lock, Queue as mQueue

from rich import print as rprint
from rich.text import Text

from timer import timeit




@timeit
def callMe(q: Queue, l: Lock):
    count: int = 0

    while True:
        if count == 1:
            break
        l.acquire()
        try:
            # if queue in empty `continue`
            if q.empty():

                continue

            # get url from queue
            url = q.get()
            rprint(Text(f"{multiprocessing.current_process().name} => {url}", style="bold blue"))
        finally:
            l.release()

        res = requests.Response = requests.get(url, timeout=5)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            a_tags: list = soup.find_all("a")
            
            a_s: list[str] = []
            for a in a_tags:
                
                url: str = a.attrs.get('href', None)
                if not url: continue
                if url.startswith("https://"):
                    a_s.append(url) 
        
      
        l.acquire()
        try:
            for url in a_s:
                q.put(url)
        finally:
            l.release()
    
        # count += 1
    
    return 

class Workers:
    instance = 0
    def __init__(self) -> None:
        self.__l = Lock()
        self.__q = mQueue()
        self.__fq = mQueue()
        self.__target = None 
        self.__workers: list[Process] = []

        self.__urls: list[str] = [
            "https://docs.python.org/3/library/multiprocessing.html#exchanging-objects-between-processes",
            "https://docs.python.org/3/library/threading.html"
        ]

        for url in self.__urls:
            self.__q.put(url)

        
    
    @timeit
    def __createWorkers(self, workers: int):
        for i in range(3):
            self.__workers.append(
                Process(
                    target=callMe,
                    args=(self.__q, self.__l, ),
                )
            )
    @timeit
    def startWorkers(self, workers: int =1):
        """
        Create and start workers, default 1
        """

        # Create workers
        self.__createWorkers(workers)

        # start workers
        for p in self.__workers:
            rprint(Text(f"[Starting] {p.name}|{p.pid}", style='bold green'))
            p.start()
            rprint(Text(f"[Started] {p.name}|{p.pid}", style='bold green'))

        # join workers
        for p in self.__workers:
            rprint(Text(f"[Joining] {p.name}|{p.pid}", style='bold white'))
            p.join()
            rprint(Text(f"[Joined] {p.name}|{p.pid}", style='bold white'))

    @timeit
    def stopWorkers(self):
        """
        To stop the workers
        """
        for p in self.__workers:
            # if worker is alive
            # terminate it 
            if p.is_alive():
                rprint(Text(f"[Terminating] {p.name}|{p.pid}", style='bold red'))
                p.terminate()    
                rprint(Text(f"[Terminated] {p.name}|{p.pid}", style='bold red'))
@timeit
def main():
    try:
        w: Workers = Workers()
        w.startWorkers()
    except KeyboardInterrupt:
        w.stopWorkers()

if __name__ == "__main__":
    main()