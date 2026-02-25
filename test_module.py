import unittest
from medical_data_visualizer import draw_cat_plot, draw_heat_map


class MedicalVisualizerTestCase(unittest.TestCase):

    def test_draw_cat_plot(self):
        fig = draw_cat_plot()
        self.assertIsNotNone(fig)

    def test_draw_heat_map(self):
        fig = draw_heat_map()
        self.assertIsNotNone(fig)


def test_draw_cat_plot():
    unittest.main(argv=[''], exit=False)


def test_draw_heat_map():
    unittest.main(argv=[''], exit=False)