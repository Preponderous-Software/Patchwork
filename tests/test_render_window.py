import unittest
from unittest.mock import MagicMock, patch


class TestRenderWindow(unittest.TestCase):
    def setUp(self):
        self.pygame_patcher = patch("render_window.pygame")
        self.mock_pygame = self.pygame_patcher.start()
        self.mock_pygame.QUIT = "QUIT_SENTINEL"
        self.addCleanup(self.pygame_patcher.stop)

        from render_window import RenderWindow
        self.RenderWindow = RenderWindow

    def test_init_sets_up_pygame_window(self):
        window = self.RenderWindow("Title", 640, 480)

        self.mock_pygame.init.assert_called_once()
        self.mock_pygame.display.set_mode.assert_called_once_with((640, 480))
        self.mock_pygame.display.set_caption.assert_called_once_with("Title")
        self.assertIs(window.get_surface(), self.mock_pygame.display.set_mode.return_value)

    def test_tick_delegates_to_clock(self):
        window = self.RenderWindow("Title", 640, 480)

        window.tick(30)

        self.mock_pygame.time.Clock.return_value.tick.assert_called_once_with(30)

    def test_should_continue_true_and_dispatches_non_quit_events(self):
        window = self.RenderWindow("Title", 640, 480)
        event = MagicMock(type="KEYDOWN_SENTINEL")
        self.mock_pygame.event.get.return_value = [event]
        handler = MagicMock()
        window.register_event_handler(handler)

        result = window.should_continue()

        self.assertTrue(result)
        handler.assert_called_once_with(event)

    def test_should_continue_false_after_quit_event(self):
        window = self.RenderWindow("Title", 640, 480)
        quit_event = MagicMock(type="QUIT_SENTINEL")
        self.mock_pygame.event.get.return_value = [quit_event]

        result = window.should_continue()

        self.assertFalse(result)

    def test_handlers_not_dispatched_for_quit_event(self):
        window = self.RenderWindow("Title", 640, 480)
        quit_event = MagicMock(type="QUIT_SENTINEL")
        self.mock_pygame.event.get.return_value = [quit_event]
        handler = MagicMock()
        window.register_event_handler(handler)

        window.should_continue()

        handler.assert_not_called()


if __name__ == "__main__":
    unittest.main()
