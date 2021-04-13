import urwid

class FancyListBox(urwid.ListBox):
    def keypress(self, size, key):
        if key in ("j", "down"):
            return super().keypress(size, "down")
        if key in ("k", "up"):
            return super().keypress(size, "up")
        else:
            return super().keypress(size, key)


class FancyLineBox(urwid.LineBox):
    def __init__(self, original_widget, title=""):

        original_widget = urwid.Padding(original_widget, left=1, right=1)

        super().__init__(
            original_widget,
            title,
            title_align="left",
            tline="─",
            trcorner="╮",
            tlcorner="╭",
            bline="─",
            blcorner="╰",
            brcorner="╯",
            lline="│",
            rline="│",
        )


class SelectableColumns(urwid.Columns):
    def selectable(self):
        return True

    def keypress(self, size, key):
        return super().keypress(size, key)
