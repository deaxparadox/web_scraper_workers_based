import multiprocessing as mp
import typing
from rich import print as rprint
from rich.text import Text
from time import sleep

from timer import timeit
from scraper import test_function



# @timeit
# def test_function(**kwargs) -> None:
#     lock: mp.Lock = kwargs.get("lock")
#     queue: mp.Queue = kwargs.get("queue")
    
#     for i in range(10):
#         lock.acquire()
#         try:
#             print(f"{mp.current_process().name} => {i}")
#         finally:
#             lock.release()    
#         sleep(0.1)

class Workers(object):
    def __init__(self, workers: int =3, **kwargs):
        self.__lock: mp.Lock = mp.Lock()
        self.__queue: mp.Queue = mp.Queue()
        self.__processes: int = workers
        self.__processes_list: list[mp.Process] = []

        # 
        self.__processes_active_count: int = 0
        
    
    def workers_create(self, func: typing.Any | None, **kwargs) -> None:
        # add lock and queue to kwargs
        kwargs.update({
            "lock": self.__lock,
            "queue": self.__queue
        })

        for i in range(self.__processes):
            name: str = f"Process {i}"

            # create process
            p: mp.Process = mp.Process(
                target=func,
                kwargs=kwargs,
                name=name,
            )

            # add process to `__processes_list`
            self.__processes_list.append(p)

    def workers_start(self, *args, **kwargs) -> None:
        """
        Start the workers in `__processes_list`
        and increase the `__processes_active_count`
        """

        # starting workers in `__processes_list`
        for p in self.__processes_list:
            p.start()
            self.__processes_active_count+=1

    def workers_join(self, *args, **kwargs) -> None:
        """
        Join the processes in `__processes_list` and decrease the `__processes_active_count`
        """
        for p in self.__processes_list:
            p.join()
            self.__processes_active_count -= 1

    def workers_stop(self, *args, **kwargs) -> None:
        for p in self.__processes_list:
            if p.is_alive():
                p.terminate()


def main():
    workers = Workers(workers=36)
    try:
        workers.workers_create(test_function)
        workers.workers_start()
        workers.workers_join()
    except KeyboardInterrupt:
        workers.workers_stop()


if __name__ == "__main__":
    main()