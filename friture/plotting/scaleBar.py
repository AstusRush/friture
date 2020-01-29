from PyQt5 import QtGui, QtCore, QtWidgets
from friture.plotting.scaleDivision import numberPrecision
from friture.plotting import generated_cmrmap

# A widget canvas with a baseline, ticks and tick labels
# The logic of the placement of scale min/max and ticks belongs to another class.
# The title belongs to another class.
import math
class Note(float):
    def __init__(self,a,b):
        float.__init__(a)
        self.Name = b
    def __new__(self,a,b):
        return float.__new__(self, a)

Notes = {"C":16.35,"C#/Db":17.32,"D":18.35,"D#/Eb":19.45,"E":20.6,"F":21.83,"F#/Gb":23.12,"G":24.5,"G#/Ab":25.96,"A":27.5,"A#/B":29.14,"H":30.87}
AllNotes = {}
for i,v in Notes.items():
    c = 0
    while c <=11:
        AllNotes[i+" %d "%(c)] = v*2**c
        c+=1
FrequencyList = [Note(0.0," "),Note(100000000.0," ")]
for i,v in AllNotes.items():
    FrequencyList.append(Note(v,i))
FrequencyList.sort()

def tickFormatter(value, digits):
    #if value >= 1e3:
    #    label = "%gk" % (value / 1e3)
    #else:
    #    label = "%d" % (value)
    #Notes = {"C":16.35,"D":18.35,"E":20.6,"F":21.83,"G":24.5,"A":27.5,"H":30.87}
    for i,v in Notes.items():
        if value == v:
            return i+"0"
    n = int(round(value/Notes["C"]))
    if (n & (n-1) == 0) and n != 0:
        label = "C%d" % math.log(n, 2)
    else:
        n = int(round(value/Notes["F"]))
        if (n & (n-1) == 0) and n != 0:
            label = "F%d" % math.log(n, 2)
        else:
            label = " "
    return label

def TrackerFormatter(x,y):
    # Original: lambda x, y: "%d Hz, %.1f dB" % (x, y)
    Label = " %.2f Hz, %d dB" % (x, y)
    try:
        for i in range(1,len(FrequencyList)-2):
            lb = FrequencyList[i]-(FrequencyList[i]-FrequencyList[i-1])/2
            ub = FrequencyList[i]+(FrequencyList[i+1]-FrequencyList[i])/2
            if lb < x and x < ub :
                return Label+", "+FrequencyList[i].Name
    except:
        pass
    return Label

class VerticalScaleBar(QtWidgets.QWidget):

    def __init__(self, parent, division, transform):
        super(VerticalScaleBar, self).__init__()

        self.scaleDivision = division
        self.coordinateTransform = transform

        # should be based on font size
        self.tickLength = 8
        self.labelSpacing = 2
        self.borderOffset = 3

        self.tickFormatter = lambda tick, digits: '{0:.{1}f}'.format(tick, digits)

        # for vertical scale bar
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

    def setTickFormatter(self, formatter):
        self.tickFormatter = formatter

    def sizeHint(self):
        # for vertical scale bar
        majorTicks = self.scaleDivision.majorTicks()
        fm = QtGui.QFontMetrics(self.font())

        # label precision
        if len(majorTicks) < 2:
            maxLabelWidth = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
            prec = numberPrecision(interval)
            digits = max(0, int(-prec))
            maxLabelWidth = max([fm.width(self.tickFormatter(tick, digits)) for tick in majorTicks])

        return QtCore.QSize(maxLabelWidth + self.tickLength + self.borderOffset + self.labelSpacing, 10)

    def set_scale_properties(self, division, transform):
        self.scaleDivision = division
        self.coordinateTransform = transform

        self.update()
        # notify that sizeHint may have changed
        self.updateGeometry()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        fm = painter.fontMetrics()

        # Note: if anti-aliasing is enabled here, then coordinates need to be aligned to half-pixels
        # to get true pixel-aligned lines. Without anti-aliasing, integer coordinates are enough.
        # painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # base line
        #xb = self.width() - self.borderOffset
        #y0 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_min)
        #y1 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_max)
        #painter.drawLine(1, y0, 1, y1)

        # tick start
        xt = self.tickLength
        xtm = self.tickLength * 2 / 3

        # label end
        #le = xt - self.labelSpacing
        lh = fm.height()

        # label precision
        majorTicks = self.scaleDivision.majorTicks()
        if len(majorTicks) < 2:
            interval = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
        precision = numberPrecision(interval)
        digits = max(0, int(-precision))

        painter.setPen(QtGui.QPen(QtCore.Qt.white,3))
        for tick in self.scaleDivision.majorTicks():
            # for vertical scale we invert the coordinates
            y = self.height() - self.coordinateTransform.toScreen(tick)
            painter.drawLine(0, y, xt, y)
            tick_string = self.tickFormatter(tick, digits)
            #painter.drawText(le - fm.width(tick_string), y + lh / 2 - 2, tick_string)
            painter.drawText(xt+self.labelSpacing, y + lh / 2 - 2, " "+tick_string)

        for tick in self.scaleDivision.minorTicks():
            # for vertical scale we invert the coordinates
            y = self.height() - self.coordinateTransform.toScreen(tick)
            try:
                if len(tick.Name) > 5:
                    painter.setPen(QtGui.QPen(QtCore.Qt.black,3))
                else:
                    painter.setPen(QtGui.QPen(QtCore.Qt.white,3))
            except:
                painter.setPen(QtGui.QPen(QtCore.Qt.white,1))
            painter.drawLine(0, y, xtm, y)

    def spacingBorders(self):
        fm = QtGui.QFontMetrics(self.font())
        # for vertical scale bar
        return fm.height() // 2, fm.height() // 2


class HorizontalScaleBar(QtWidgets.QWidget):

    def __init__(self, parent, division, transform):
        super(HorizontalScaleBar, self).__init__()

        self.scaleDivision = division
        self.coordinateTransform = transform

        # should be based on font size
        self.tickLength = 8
        self.labelSpacing = 2
        self.borderOffset = 3

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))

    def sizeHint(self):
        # for vertical scale bar
        majorTicks = self.scaleDivision.majorTicks()
        fm = QtGui.QFontMetrics(self.font())

        # label precision
        if len(majorTicks) < 2:
            maxLabelWidth = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
            prec = numberPrecision(interval)
            digits = max(0, int(-prec))
            maxLabelWidth = max([fm.width('{0:.{1}f}'.format(tick, digits)) for tick in majorTicks])

        return QtCore.QSize(10, fm.height() + self.tickLength + self.borderOffset + self.labelSpacing)
        # return QtCore.QSize(maxLabelWidth + self.tickLength + self.borderOffset + self.labelSpacing, 10)

    def set_scale_properties(self, division, transform):
        self.scaleDivision = division
        self.coordinateTransform = transform

        self.update()
        # notify that sizeHint may have changed
        self.updateGeometry()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        fm = painter.fontMetrics()

        # Note: if anti-aliasing is enabled here, then coordinates need to be aligned to half-pixels
        # to get true pixel-aligned lines. Without anti-aliasing, integer coordinates are enough.
        # painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # base line
        yb = self.borderOffset
        x0 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_min)
        x1 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_max)
        painter.drawLine(x0, yb, x1, yb)

        # tick start
        yt = yb + self.tickLength
        ytm = yb + self.tickLength / 2

        # label end
        le = yt + self.labelSpacing

        # label precision
        majorTicks = self.scaleDivision.majorTicks()
        if len(majorTicks) < 2:
            interval = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
        precision = numberPrecision(interval)
        digits = max(0, int(-precision))

        #for tick in self.scaleDivision.majorTicks():
        #    # for vertical scale we invert the coordinates
        #    x = self.coordinateTransform.toScreen(tick)
        #    painter.drawLine(x, yt, x, yb)
        #    tick_string = '{0:.{1}f}'.format(tick, digits)
        #    painter.drawText(x - fm.width(tick_string) / 2, le + fm.height(), tick_string)
        #
        #for tick in self.scaleDivision.minorTicks():
        #    # for vertical scale we invert the coordinates
        #    x = self.coordinateTransform.toScreen(tick)
        #    painter.drawLine(x, ytm, x, yb)
        
        painter.setPen(QtGui.QPen(QtCore.Qt.white,3))
        KeyboardTicks = True
        for tick in self.scaleDivision.majorTicks():
            # for vertical scale we invert the coordinates
            x = self.coordinateTransform.toScreen(tick)
            painter.drawLine(x, yt, x, yb)
            try:
                if KeyboardTicks and tick > 20:
                    tick_string = tickFormatter(tick, digits)
                else:
                    KeyboardTicks = False
                    tick_string = '{0:.{1}f}'.format(tick, digits)
            except:
                tick_string = '{0:.{1}f}'.format(tick, digits)
            painter.drawText(x - fm.width(tick_string) / 2, le + fm.height(), tick_string)

        for tick in self.scaleDivision.minorTicks():
            # for vertical scale we invert the coordinates
            x = self.coordinateTransform.toScreen(tick)
            try:
                if len(tick.Name) > 5:
                    painter.setPen(QtGui.QPen(QtCore.Qt.black,3))
                else:
                    painter.setPen(QtGui.QPen(QtCore.Qt.white,3))
            except:
                painter.setPen(QtGui.QPen(QtCore.Qt.white,1))
            painter.drawLine(x, ytm, x, yb)

    def spacingBorders(self):
        fm = QtGui.QFontMetrics(self.font())
        # for vertical scale bar
        return fm.height() // 2, fm.height() // 2


class ColorScaleBar(QtWidgets.QWidget):

    def __init__(self, parent, division, transform):
        super(ColorScaleBar, self).__init__()

        self.scaleDivision = division
        self.coordinateTransform = transform

        # should be based on font size
        self.tickLength = 8
        self.labelSpacing = 2
        self.borderOffset = 3
        self.barSpacing = 1
        self.colorBarWidth = self.tickLength * 2

        # should be shared with spectrogram_image in a dedicated class
        cmap = generated_cmrmap.CMAP
        self.colors = [QtGui.QColor(cmap[i, 0] * 255, cmap[i, 1] * 255, cmap[i, 2] * 255) for i in range(cmap.shape[0])]

        # for vertical scale bar
        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

    def sizeHint(self):
        # for vertical scale bar
        majorTicks = self.scaleDivision.majorTicks()
        fm = QtGui.QFontMetrics(self.font())

        # label precision
        if len(majorTicks) < 2:
            maxLabelWidth = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
            prec = numberPrecision(interval)
            digits = max(0, int(-prec))
            maxLabelWidth = max([fm.width('{0:.{1}f}'.format(tick, digits)) for tick in majorTicks])

        return QtCore.QSize(self.borderOffset + self.colorBarWidth + self.barSpacing + self.tickLength + self.labelSpacing + maxLabelWidth, 10)

    def set_scale_properties(self, division, transform):
        self.scaleDivision = division
        self.coordinateTransform = transform

        self.update()
        # notify that sizeHint may have changed
        self.updateGeometry()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)

        fm = painter.fontMetrics()

        # Note: if anti-aliasing is enabled here, then coordinates need to be aligned to half-pixels
        # to get true pixel-aligned lines. Without anti-aliasing, integer coordinates are enough.
        # painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # color bar
        by = self.spacingBorders()[0]
        for y in range(0, self.height() - 2 * by):
            yNorm = float(y) / (self.height() - 2 * by)
            color = self.colors[int(yNorm * (len(self.colors) - 1))]
            rect = QtCore.QRect(self.borderOffset, self.height() - by - y, self.colorBarWidth, 1)
            painter.fillRect(rect, color)

        # base line
        xb = self.borderOffset + self.colorBarWidth + self.barSpacing
        y0 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_min)
        y1 = self.coordinateTransform.toScreen(self.coordinateTransform.coord_max)
        painter.drawLine(xb, y0, xb, y1)

        # tick start
        xt = xb + self.tickLength
        xtm = xb + self.tickLength / 2

        # label start
        ls = xt + self.labelSpacing
        lh = fm.height()

        # label precision
        majorTicks = self.scaleDivision.majorTicks()
        if len(majorTicks) < 2:
            interval = 0
        else:
            interval = majorTicks[1] - majorTicks[0]
        precision = numberPrecision(interval)
        digits = max(0, int(-precision))

        for tick in self.scaleDivision.majorTicks():
            # for vertical scale we invert the coordinates
            y = self.height() - self.coordinateTransform.toScreen(tick)
            painter.drawLine(xt, y, xb, y)
            tick_string = '{0:.{1}f}'.format(tick, digits)
            painter.drawText(ls, y + lh / 2 - 2, tick_string)

        for tick in self.scaleDivision.minorTicks():
            # for vertical scale we invert the coordinates
            y = self.height() - self.coordinateTransform.toScreen(tick)
            painter.drawLine(xtm, y, xb, y)

    def spacingBorders(self):
        fm = QtGui.QFontMetrics(self.font())
        # for vertical scale bar
        return fm.height() // 2, fm.height() // 2
