import sys
import unittest
import tkinter as tk


from whisper.ui.custom import CustomWindowMixin, CustomWindowTitlebarMixin, CustomTkWindow


REASON_WIN32 = "for win32 platform only"
REASON_NON_WIN32 = "for platform other than win32"


class TestCustomWindowMixin(unittest.TestCase):
    """Test the customization working."""

    def get_window(self):
        class TestWindow(CustomWindowMixin, tk.Tk):
            def __init__(self):
                tk.Tk.__init__(self)
                CustomWindowMixin.__init__(self)
        return TestWindow()

    def setUp(self):
        self.window = self.get_window()

    def tearDown(self):
        self.window.destroy()
        self.window = None

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_customization_on_win32(self):
        self.window.remove_default()
        self.window.update_idletasks()
        self.assertTrue(self.window.is_customized)
        self.assertTrue(self.window.wm_overrideredirect(None))

    @unittest.skipIf(sys.platform == "win32", REASON_NON_WIN32)
    def test_customization_on_non_win32(self):
        with self.assertRaises(Exception):
            self.window.remove_default()
            self.window.update_idletasks()
        self.assertFalse(self.window.is_customized)
        self.assertFalse(self.window.wm_overrideredirect(None))


class TestCustomTitlebar(unittest.TestCase):
    """Test the working of custom titlebar."""

    def get_window(self):
        class TestWindow(CustomWindowTitlebarMixin, tk.Tk):
            def __init__(self):
                tk.Tk.__init__(self)
                CustomWindowTitlebarMixin.__init__(self)
        return TestWindow()

    def setUp(self):
        self.window = self.get_window()

    def tearDown(self):
        try:
            self.window.destroy()
        except tk.TclError:
            pass
        finally:
            self.window = None

    def test_should_have_root(self):
        self.window.update_idletasks()
        self.assertTrue(hasattr(self.window, "root"))

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_custom_titlebar_displayed_for_win32_only(self):
        self.window.update_idletasks()
        self.assertTrue(hasattr(self.window, "titlebar"))

    @unittest.skipIf(sys.platform == "win32", REASON_NON_WIN32)
    def test_custom_titlebar_not_displayed_for_non_win32(self):
        self.window.update_idletasks()
        self.assertFalse(hasattr(self.window, "titlebar"))

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_titlebar_has_required_widgets_in_win32(self):
        for widget_name in ("icon", "title", "minimize", "maximize", "close"):
            self.assertTrue(hasattr(self.window.titlebar, widget_name))

    @unittest.skipIf(sys.platform == "win32", REASON_NON_WIN32)
    def test_titlebar_dont_has_required_widgets_in_non_win32(self):
        self.assertFalse(hasattr(self.window, "titlebar"))

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_custom_titlebar_title_updates_in_win32(self):
        title = "TestWindowTitle"
        self.window.title(title)
        self.window.update_idletasks()
        self.assertEqual(self.window.title(), title)

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_titlebar_onclose_exists_in_win32(self):
        self.window.titlebar.close.invoke()
        self.window.update_idletasks()

        with self.assertRaises(tk.TclError) as error:
            self.window.destroy()
        self.assertTrue("destroy" in error.exception.args[0])

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def text_maximize_on_win32(self):
        self.assertFalse(self.window.is_maximized)

        self.window.titlebar.maximize.invoke()
        self.window.update_idletasks()
        self.assertTrue(self.window.is_maximized)

        self.window.titlebar.maximize.invoke()
        self.window.update_idletasks()
        self.assertFalse(self.window.is_maximized)

    @unittest.skipIf(sys.platform != "win32", REASON_WIN32)
    def test_minimize_on_win32(self):
        self.window.titlebar.minimize.invoke()
        self.window.update_idletasks()
        self.assertFalse(self.window.winfo_ismapped())

        self.window.event_generate("<Map>")
        self.window.update_idletasks()
        self.assertTrue(self.window.winfo_ismapped())


class TestCustomTkWindow(unittest.TestCase):

    def test_window_runs(self):
        window = CustomTkWindow()
        window.destroy()
        window.update_idletasks()