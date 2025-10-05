import unittest
from app.services import baidu_search, bing_search
from app.services.searchEngines import search_engines


class TestSearchEngines(unittest.TestCase):
    def test_baidu_search(self):
        urls = baidu_search("hbpu.edu.cn")
        print("result:", len(urls))
        for x in urls:
            print(x)

    def test_bing_search(self):
        urls = bing_search("hbpu.edu.cn")
        print("result:", len(urls))
        for x in urls:
            print(x)

    def test_search_engines(self):
        urls = search_engines("hbpu.edu.cn")
        print("result:", len(urls))
        for x in urls:
            print(x)


if __name__ == '__main__':
    unittest.main()
