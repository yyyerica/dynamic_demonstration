# coding:utf-8
import wx
import random
import sys

size = 20  # 随机数组长度
xPos = 50
BarData = []
delay = 100
type = '插入排序'


class AnimationPanel(wx.Panel): # 动画面板
    def __init__(self, parent, ID=-1, pos=(0, 0), size=(900, 500)):
        print "init"
        wx.Panel.__init__(self, parent, ID, pos, size)
        self.SetBackgroundColour("WHITE")
        self.GenerateBarData(xPos)  # 取随机数，设置随机数的区间
        self.Bind(wx.EVT_PAINT, self.OnPaint)

        self.font = wx.Font(8, wx.DEFAULT, wx.ITALIC, wx.NORMAL)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    # generate the original bars's data (x,y,w,h)
    def GenerateBarData(self, xPos):
        width = 900 / (size * 2)
        gap = 900 / (size * 4)
        print "GenerateBarData"
        del BarData[:]
        for num in range(size):
            xPos += (width + gap)  # 横坐标
            height = random.randrange(5, 300)
            barparameters = [xPos, 100, width, height]
            BarData.append(barparameters)  # append()方法向列表的尾部添加一个新的元素。只接受一个参数。
        self.RevertBarData()

    # revert the bars' yPos
    def RevertBarData(self):
        print "RevertBarData"
        maxH = self.maxHeight()
        for h in range(size):
            moveH = maxH - BarData[h][3]
            yPos = BarData[h][1]
            yPos += moveH
            BarData[h][1] = yPos

    # return the hightest height in bars
    def maxHeight(self):
        print "maxHeight"
        Height = []
        # store all the bar height in Height[]
        for h in range(size):
            Height.append(BarData[h][3])
        # find out the heightest bar and return
        maxH = max(Height)
        return maxH

    def OnPaint(self, event):
        # print "OnPaint"
        dc = wx.PaintDC(self)
        self.paintBox(dc)

    def paintBox(self, dc):
        # print "paintBox"
        dc.SetBrush(wx.Brush("gray"))
        dc.SetFont(self.font)
        dc.SetTextForeground("BLACK")
        for i in range(0, size):
            dc.DrawRectangle(*BarData[i])
            x = BarData[i][0]
            y = BarData[i][1] + BarData[i][3]
            h = str(BarData[i][3])
            dc.DrawText(h, x, y)

    # # bubble sort
    # def BubbleSort(self):
    #     print "BubbleSort"
    #     for i in range(len(BarData), 1, -1):
    #         for j in range(i - 1):
    #             if BarData[j][3] > BarData[j + 1][3]:
    #                 BarData[j][1], BarData[j + 1][1] = BarData[j + 1][1], BarData[j][1]
    #                 BarData[j][3], BarData[j + 1][3] = BarData[j + 1][3], BarData[j][3]
    #                 yield

    # select_sort
    def Selectsort(self):
        for i in range(0, len(BarData) - 1):
            index = i
            for j in range(i + 1, len(BarData)):
                if BarData[index][3] > BarData[j][3]:
                    index = j
            BarData[i][3], BarData[index][3] = BarData[index][3], BarData[i][3]
            BarData[i][1], BarData[index][1] = BarData[index][1], BarData[i][1]
            yield

    # 插入排序
    def insert_sort(self):
        for i in range(1, len(BarData)):
            key = BarData[i][3]
            key1 = BarData[i][1]
            j = i - 1
            while j >= 0:
                if BarData[j][3] > key:
                    BarData[j + 1][3] = BarData[j][3]
                    BarData[j + 1][1] = BarData[j][1]
                    BarData[j][3] = key
                    BarData[j][1] = key1
                    yield
                j -= 1

    def OnTimer(self, event):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # print "OnTimer"
        if not hasattr(self, 'g'):  # hasattr 检验 g 是否存在
            self.g = self.insert_sort()
            global type
            if type == '插入排序':
                self.g = self.insert_sort()
            elif type == '选择排序':
                self.g = self.Selectsort()
            elif type == '基数排序':
                self.g = self.insert_sort()
            elif type == '快速排序':
                self.g = self.Selectsort()
        try:
            next(self.g)
            self.Refresh()
        except StopIteration:
            del self.g
            self.timer.Stop()
            wx.MessageBox('Done!')


class SidePanel(wx.Panel):
    def __init__(self, parent, aPanel, ID=-1, pos=(750, 0), size=(250, 500)):

        wx.Panel.__init__(self, parent, ID, pos, size)
        self.SetBackgroundColour("WHITE")
        self._aPanel = aPanel

        # ---------------------------------------------
        # create Button_Panel on Side_Panel
        self.Button_Panel = wx.Panel(self, -1, pos=(750, 0), size=(250, 100))

        # create ButtonSizer for button_panel
        # buttonSizer = wx.GridSizer(rows=2, cols=2)
        buttonSizer = wx.GridSizer(1, 2, 5, 5)

        # create 4 buttons label, add them to Button_Panel
        # and binding them with corresponding event

        # button = wx.Button(self.Button_Panel, -1, eachLabel)
        bmp = wx.Bitmap("start.jpg", wx.BITMAP_TYPE_PNG)
        button = wx.BitmapButton(self.Button_Panel, -1, bmp, size=(bmp.GetWidth()+10, bmp.GetHeight()+10))
        button.Bind(wx.EVT_BUTTON, self.OnStart)
        buttonSizer.Add(button, 0,  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)

        bmp = wx.Bitmap("stop.jpg", wx.BITMAP_TYPE_PNG)
        button = wx.BitmapButton(self.Button_Panel, -1, bmp, size=(bmp.GetWidth()+10, bmp.GetHeight()+10))
        button.Bind(wx.EVT_BUTTON, self.OnPause)
        buttonSizer.Add(button, 0,  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.Button_Panel.SetSizer(buttonSizer)

        # self.Button_Panel.Fit()
        # ---------------------------------------------

        # ---------------------------------------------
        # Create ChoiceList_Panel for 2 choice dropdown list
        # Sort_List: provide choice of sorting algorithm
        # Graph_List: provide choice of graph algorithm
        self.ChoiceList_Panel = wx.Panel(self, -1, pos=(750, 150), size=(250, 50))

        SortList = [ '插入排序', '快速排序', '选择排序', '基数排序']

        self.SortChoice = wx.Choice(self.ChoiceList_Panel, -1, choices=SortList)
        self.SortChoice.SetStringSelection('插入排序')
        al_tex = wx.StaticText(self.ChoiceList_Panel, -1, '选择排序算法 :')
        ChoiceSizer = wx.BoxSizer(wx.VERTICAL)
        ChoiceSizer.Add(al_tex, 1, wx.EXPAND | wx.ALL)
        ChoiceSizer.Add(self.SortChoice, 1, wx.EXPAND | wx.ALL)
        self.SortChoice.Bind(wx.EVT_CHOICE, self.sortChange)
        self.ChoiceList_Panel.SetSizer(ChoiceSizer)
        # ---------------------------------------------

        # ---------------------------------------------
        # create Size_Panel
        # Provide a set of size RadioBox
        self.Size_Panel = wx.Panel(self, -1, pos=(750, 300), size=(250, 100))
        SizeList = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50']
        self.Size_RadioBox = wx.RadioBox(self.Size_Panel, -1, "选择数组长度", wx.DefaultPosition, wx.DefaultSize, SizeList, 5,
                                    wx.RA_SPECIFY_COLS)
        self.Size_RadioBox.Bind(wx.EVT_RADIOBOX, self.sizeChange)
        # SizeSizer = wx.BoxSizer(wx.VERTICAL)
        # SizeSizer.Add(Size_RadioBox, 1, wx.EXPAND | wx.ALL)
        # self.Size_Panel.SetSizer(SizeSizer)

        # ---------------------------------------------

        # ---------------------------------------------
        # create a Speed_Panel
        # Speed_Panel contains a slider used for control the speed of animation
        self.Speed_Panel = wx.Panel(self, -1, pos=(750, 400), size=(250, 100))
        self.Speed_Slider = wx.Slider(self.Speed_Panel, -1, 25, 1, 50, wx.DefaultPosition, (250, -1),
                                 wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS, name="Speed")

        # Speed_Slider.SetTickFreq(5, 1)
        self.Speed_Slider.SetTickFreq(1)
        self.Bind(wx.EVT_SCROLL_THUMBRELEASE, self.sliderSubThumbMoveFunc, self.Speed_Slider)
        Speed_tex = wx.StaticText(self.Speed_Panel, -1, "Change animation's speed")
        Speed_Sizer = wx.BoxSizer(wx.VERTICAL)
        Speed_Sizer.Add(Speed_tex, 0, wx.EXPAND | wx.ALL)
        Speed_Sizer.Add(self.Speed_Slider, 0, wx.EXPAND | wx.ALL)
        self.Speed_Panel.SetSizer(Speed_Sizer)
        # ---------------------------------------------

        Side_PanelSizer = wx.BoxSizer(wx.VERTICAL)
        Side_PanelSizer.Add(self.Button_Panel, 0, wx.EXPAND)
        Side_PanelSizer.Add((-1, 40))
        Side_PanelSizer.Add(self.ChoiceList_Panel, 0, wx.EXPAND)
        Side_PanelSizer.Add((-1, 40))
        Side_PanelSizer.Add(self.Size_Panel, 0, wx.EXPAND)
        Side_PanelSizer.Add((-1, 40))
        Side_PanelSizer.Add(self.Speed_Panel, 0, wx.EXPAND)
        self.SetSizer(Side_PanelSizer)
        self.Center()

    def OnStart(self, event):
        self._aPanel.timer.Start(delay)
        pass

    def OnPause(self, event):
        self._aPanel.timer.Stop()
        pass

    def sizeChange(self, event):
        global size
        size = int(self.Size_RadioBox.GetStringSelection())
        print size, \
            ' is clicked from Radio Box'
        self._aPanel.GenerateBarData(xPos)
        self._aPanel.Refresh(True, None)
        pass

    def sortChange(self, event):
        global type
        type = self.SortChoice.GetStringSelection()
        # self.SortChoice.GetStringSelection()
        pass

    def sliderSubThumbMoveFunc(self, event):
        obj = event.GetEventObject()
        # objID = obj.GetId()
        global delay
        delay = obj.GetValue()*4
        print delay
        pass

class MainFrame(wx.Frame):
    def __init__(self):  # 初始化实例的值
        wx.Frame.__init__(self, None, title="Sort Algorithm", size=(1000, 500))

        # ---------------------------------------------
        # create 2 panels
        # Animation_Panel---display the sorting animation
        # Side_panels---display the buttons, comboBox, slider
        self.Animation_Panel = AnimationPanel(self)
        self.Side_Panel = SidePanel(self, self.Animation_Panel)
        # self.Side_Panel = SidePanel(self)

        # ---------------------------------------------
        # arrange the two main panels in the main sizer for the MainFrame
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        # mainSizer.Add(self.Side_Panel, 1, wx.EXPAND | wx.ALL, 30)
        mainSizer.Add(self.Side_Panel, 1, wx.LEFT | wx.TOP, 30)
        mainSizer.Add(self.Animation_Panel, 2, wx.RIGHT | wx.TOP, 30)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        self.Center()

        # ---------------------------------------------


if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame()  # 幀是一個窗口
    frame.Center()
    frame.SetBackgroundColour("white")
    frame.Show()
    app.MainLoop()
