import unittest
from src.controllers.predictor_controller import PredictorController
from src.views.window import Window


class TestPredictorController(unittest.TestCase):
    def setUp(self):
        self.app = PredictorController()

    def test_create_main_window(self):
        window = self.app.create_main_window()
        self.assertTrue(isinstance(window, Window))



if __name__ == '__main__':
    unittest.main()