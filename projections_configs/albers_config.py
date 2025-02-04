import math
import wx

class ConfigurationPanel(wx.Panel):
    
    def __init__(self, parent, window_id, cartographer):
        self.cartographer = cartographer

        sty = wx.SUNKEN_BORDER
        wx.Window.__init__(self, parent, window_id, style=sty, size=wx.Size(1, 1))

        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.panel = wx.Panel(self)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        fgs = wx.FlexGridSizer(2, 2, 10, 25)

        label_phi1 = wx.StaticText(self.panel, label="Std Parallel #1")
        label_phi2 = wx.StaticText(self.panel, label="Std Parallel #2")

        self.phi1_id = wx.NewId()
        self.phi2_id = wx.NewId()
        self.slider_phi1 = wx.Slider(self.panel, id=self.phi1_id, minValue=0, maxValue=88, value=30, style=wx.SL_HORIZONTAL)
        self.slider_phi2 = wx.Slider(self.panel, id=self.phi2_id, minValue=1, maxValue=89, value=60, style=wx.SL_HORIZONTAL)

        self.Bind(wx.EVT_SLIDER, self.on_update)

        fgs.AddMany([(label_phi1), (self.slider_phi1, 1, wx.EXPAND),
                     (label_phi2), (self.slider_phi2, 1, wx.EXPAND)])

        fgs.AddGrowableCol(1, 1)
        hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
        self.panel.SetSizer(hbox)
        self.Hide()

    def on_update(self, event):
        
        # if slider 1 is moving, adjust slider2
        if event.GetEventObject().GetId() == self.phi1_id:
            if self.slider_phi1.GetValue() >= self.slider_phi2.GetValue():
                self.slider_phi2.SetValue(self.slider_phi1.GetValue()+1)
                
        # if slider 2 is moving, adjust slider1
        elif event.GetEventObject().GetId() == self.phi2_id:
            if self.slider_phi2.GetValue() <= self.slider_phi1.GetValue():
                self.slider_phi1.SetValue(self.slider_phi2.GetValue()-1)

        self.cartographer.projection_panel.projection.set_standard_parallels(math.radians(self.slider_phi1.GetValue()), math.radians(self.slider_phi2.GetValue()))
        self.cartographer.earth_canvas.set_standard_parallels(self.slider_phi1.GetValue(), self.slider_phi2.GetValue())
        self.cartographer.projection_panel.Refresh()
        self.cartographer.earth_canvas.Refresh()
        
    def OnSize(self, event):
        self.panel.SetSize(self.GetSize())
        
