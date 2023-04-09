import requests
import bs4
from bs4 import BeautifulSoup
import multiprocessing as mp

from timer import timeit
from html_element import Tags


html_tags = [x for x in dir(Tags) if not x.startswith("__")]

class TupleClass(object):
    """
    This class convert tuple element in class attribute,
    which can be access with unique sequence identifier

    examples:

    t = TupleClass((1,2,3,4,5))

    t.a0    # print 1

    t.a1    # print 2
    """
    def __init__(self, *args, limit: int = 100, **kwargs) -> None:
        
        if args.__len__() > limit:
            raise RuntimeError("for safe memory usage limit is 100, but you can override with limit argument")
        
        for i, arg in enumerate(args):
            name = "a"+str(i)
            setattr(self, name, arg)


def req(url: str) -> str:
    """
    This function `requests` the content of url, and 
    return a str object, if response `status_code` in 200

    If no response in 10 seconds, then timeout

    :param url: takes the `URL` for request.
    :return: return the str

    Usage::

      >>> import scapper
      >>> res = req('GET', 'https://httpbin.org/get', timeout=10)
      >>> res
      <text string>
    """

    res: requests.Response = requests.get(url, timeout=10)
    if res.status_code == 200:
        return res.text
    return 


@timeit
def test_function(url: str, **kwargs) -> None:
    lock: mp.Lock = kwargs.get("lock")
    queue: mp.Queue = kwargs.get("queue")


    
    # 
    text: str = req(url)

    # 
    soup = BeautifulSoup(text, "html.parser")

    for tag in html_tags:
        try:
            found = soup.find_all(tag)
            print(found)
        except:
            print("[{tag}] not found")
        
        
            

def main():
    test_function()

if __name__ == "__main__":
    main()