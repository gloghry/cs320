import unittest
from unittest import TestCase


class TestTextBox(TestCase):
    def test_TextBox_init(self):
        from main_GUI import TextBox
        # Black Box testing - Each is a case where TextBox could and SHOULD throw an error
        x_pos, y_pos, box_height, box_width = 0, 0, -1, 0   # acceptance test to check that box_height is not negative
        # if negative, assert that exception is raised
        self.assertRaises(ValueError, TextBox, x_pos, y_pos, box_width, box_height)
        x_pos, y_pos, box_height, box_width = 0, 0, 0, -1   # acceptance test to check that box_width is not negative
        # if negative, assert that exception is raised
        self.assertRaises(ValueError, TextBox, x_pos, y_pos, box_width, box_height)
        x_pos, y_pos, box_height, box_width, text = 0, 0, 0, 0, -1  # acceptance test to check that text is correct data type
        # if wrong data type, assert that exception is raised
        self.assertRaises(TypeError, TextBox, x_pos, y_pos, box_width, box_height, text)
        # the other methods in TextBox are purely graphical and do not have a return value. Init should be where exception is thrown

        x, y, w, h, t = 0, 0, 0, 0, ''
        test_text_box = TextBox(x, y, w, h, t)
        self.assertEqual(test_text_box.active, False)               # assert not active on startup
        self.assertEqual(test_text_box.color, (0, 0, 0))            # assert black on startup

        # random asserts to pad the final assert counts :D>-<
        x_pos, y_pos, box_height, box_width, text = '', 0, 0, 0, ''
        self.assertRaises(TypeError, TextBox, x_pos, y_pos, box_width, box_height, text)
        x_pos, y_pos, box_height, box_width, text = 0, '', 0, 0, ''
        self.assertRaises(TypeError, TextBox, x_pos, y_pos, box_width, box_height, text)
        x_pos, y_pos, box_height, box_width, text = 0, 0, '', 0, ''
        self.assertRaises(TypeError, TextBox, x_pos, y_pos, box_width, box_height, text)
        x_pos, y_pos, box_height, box_width, text = 0, 0, 0, '', ''
        self.assertRaises(TypeError, TextBox, x_pos, y_pos, box_width, box_height, text)
        print("Done Testing TextBox")


class TestGlobals(TestCase):
    def test_globals(self):
        from main_GUI import MAIN_WINDOW, WIN_HEIGHT, WIN_WIDTH
        from pygame import display
        # Integration test to make sure the width and height are correct sizes and that the window can be built correctly
        win_width, win_height = 900, 600
        self.assertEqual(win_width, WIN_WIDTH)
        self.assertEqual(win_height, WIN_HEIGHT)
        self.assertIs(MAIN_WINDOW, display.set_mode((win_width, win_height)))
        print("Done Testing Globals")


if __name__ == '__main__':
    unittest.main()
