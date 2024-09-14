import unittest
from time import sleep
from src.models.cache_handler import CacheHandler  

class TestCacheHandler(unittest.TestCase):
    def setUp(self):
        self.cache = CacheHandler()

    def test_insert_and_get(self):
        data = {'AAPL': 'Dados da Apple'}
        self.cache.insert(data)
        
        result = self.cache.get('AAPL')
        self.assertEqual(result, 'Dados da Apple')

    def test_delete(self):
        self.cache.delete('AAPL')
        result = self.cache.get('AAPL')
        self.assertNotIn('Dados da Apple', result)

    def test_insert_tmp(self):
        data = {'AAPL': 'Dados da Apple'}
        self.cache.insert_tmp(data=data, s=1)
        sleep(2)

        result = self.cache.get('AAPL')
        self.assertNotIn('Dados da Apple', result)

if __name__ == '__main__':
    unittest.main()