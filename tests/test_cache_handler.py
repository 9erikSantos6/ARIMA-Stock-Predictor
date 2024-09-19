import unittest
from time import sleep
from src.models.cache_handler import CacheHandler  

class TestCacheHandler(unittest.TestCase):
    def setUp(self):
        self.cache = CacheHandler()

    def test_insert_and_get(self):
        data1 = {'my_dict': (4, 3, 1)}
        data2 = {'second_dict': 'Ação'}
        self.cache.insert(data1) 
        self.cache.insert(data2) 
        
        result1 = self.cache.get('my_dict')
        result2 = self.cache.get('second_dict')
        self.assertEqual(result1, (4, 3, 1))
        self.assertEqual(result2, 'Ação')

    def test_insert_tmp(self):
        data = {'AAPL': 'Dados da Apple'}
        self.cache.insert_tmp(data=data, s=1)
        sleep(2)

        result = self.cache.get('AAPL')
        self.assertIsNone(result)

    def test_delete(self):
        self.cache.delete('AAPL')
        result = self.cache.get('AAPL')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
