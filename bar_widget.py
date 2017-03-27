
from PySide import QtGui


class BarWidget(QtGui.QWidget):
    def __init__(self):
        super(BarWidget, self).__init__()

        self.bars_number = 16
        self.bars = [1] * self.bars_number
        self.padding = 2
        self.resolution = 255

        self.setMinimumSize(240, 320)

    def setBars(self, bars):
        self.bars_number = len(bars)
        for index, value in enumerate(bars):
            if value > self.resolution:
                bars[index] = self.resolution
        self.bars = bars
        self.update()

    def paintEvent(self, e):

        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawBars(painter)
        painter.end()

    def drawBars(self, painter):
        size = self.size()
        width = size.width()
        height = size.height()

        bar_width = float(width - self.padding) / self.bars_number

        color = QtGui.QColor(0, 0, 0)
        painter.setPen(color)
        painter.setBrush(color)
        painter.drawRect(0, 0, width, height)
        for bar, value in enumerate(self.bars):
            bar_height = (height - self.padding) * value / self.resolution
            if not bar_height:
                bar_height = 1
            painter.setBrush(self.barColor(bar))
            painter.drawRect(
                bar * bar_width + self.padding,
                height - bar_height,
                bar_width - self.padding,
                bar_height - self.padding)

    def barColor(self, bar):
        position = int((bar + 0.5) * 255 / self.bars_number)
        return self.palette(position)

    def blue2red(self, position):
        position &= 0xFF
        if position < 128:
            return QtGui.QColor(0, position * 2, 255 - position * 2)
        else:
            position -= 128
            return QtGui.QColor(position * 2, 255 - position * 2, 0)

    palette = blue2red


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    BarWidget().show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
