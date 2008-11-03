import wx
import wx.aui
import sys
    
def drawFlowBox(dc,name,rgb=[200,50,50],pos=[0,0]):
    font = dc.GetFont()
    font.SetPointSize(24)
    r, g, b = rgb

    #get size based on text
    dc.SetFont(font)
    w,h = dc.GetFullTextExtent(name)[0:2]
    #draw box
    rect = wx.Rect(pos[0], pos[1], w,h)
    rect.Inflate(20,10)    
    #the edge should match the text
    dc.SetPen(wx.Pen(wx.Colour(r, g, b, wx.ALPHA_OPAQUE)))
    #for the fill, draw once in white near-opaque, then in transp colour
    dc.SetBrush(wx.Brush(wx.Colour(255,255,255, 250)))
    dc.DrawRoundedRectangleRect(rect, 8)   
    dc.SetBrush(wx.Brush(wx.Colour(r,g,b,50)))
    dc.DrawRoundedRectangleRect(rect, 8)   
    #draw text        
    dc.SetTextForeground(rgb) 
    dc.DrawText(name, pos[0], pos[1])
def drawFlowLoop(dc,name,startX,endX,base,height,rgb=[200,50,50]):
    xx = [endX,  endX,   endX,   endX-5, endX-10, startX+10,startX+5, startX, startX, startX]
    yy = [base,height+10,height+5,height, height, height,  height,  height+5, height+10, base]
    pts=[]
    for n in range(len(xx)):
        pts.append([xx[n],yy[n]])
    dc.DrawSpline(pts)
class FlowPanel(wx.ScrolledWindow):
    def __init__(self, parent, id=-1,size = wx.DefaultSize):
        """A panel that shows how the procedures will fit together
        """
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        self.parent=parent    
        self.addProcBtn = wx.Button(self,-1,'AddProc')              
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        
    def OnPaint(self, evt):
        #create a drawing context for our lines/boxes
        pdc = wx.PaintDC(self)
        try:
            self.dc = wx.GCDC(pdc)
        except:
            self.dc = pdc
            
        self.dc.Clear()
        
        self.dc.DrawLine(x1=10,y1=80,x2=500,y2=80)
        drawFlowLoop(self.dc,'Flow1',startX=100,endX=450,base=80,height=20)
        drawFlowBox(self.dc, name='Proc1', pos=[150,40])
        drawFlowBox(self.dc, name='Proc2', pos=[350,40])
                  
class Procedure(wx.Panel):
    """A frame to represent a single procedure
    """
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self,parent)
        self.parent=parent            
class ProceduresPanel(wx.aui.AuiNotebook):
    """A notebook that stores one or more procedures
    """
    def __init__(self, parent, id=-1):
        self.parent=parent
        wx.aui.AuiNotebook.__init__(self, parent, id,)
        self.addProcedure('first')
    def addProcedure(self, procName):
        text1 = Procedure(parent=self)
        self.AddPage(text1, procName)
    
class ProcButtonsPanel(wx.Panel):
    def __init__(self, parent, id=-1):
        """A panel that shows how the procedures will fit together
        """
        wx.Panel.__init__(self,parent,size=(100,600))
        self.parent=parent    
        self.sizer=wx.BoxSizer(wx.VERTICAL)
        
        textImg = wx.Bitmap("res//text.png")
        self.textBtn = wx.BitmapButton(self, -1, textImg, (20, 20),
                       (textImg.GetWidth()+10, textImg.GetHeight()+10),style=wx.NO_BORDER)
                       
        patchImg= wx.Bitmap("res//patch.png")
        self.patchBtn = wx.BitmapButton(self, -1, patchImg, (20, 20),
                       (patchImg.GetWidth()+10, patchImg.GetHeight()+10),style=wx.NO_BORDER)
                       
        mouseImg= wx.Bitmap("res//mouse.png")
        self.mouseBtn = wx.BitmapButton(self, -1, mouseImg, (20, 20),
                       (mouseImg.GetWidth()+10, mouseImg.GetHeight()+10),style=wx.NO_BORDER)
#        patchImg= wx.Bitmap("res//patch.png")
#        self.textBtn = wx.BitmapButton(self, -1, patchImg, (20, 20),
#                       (patchImg.GetWidth()+10, patchImg.GetHeight()+10))
#        patchImg= wx.Bitmap("res//patch.png")
#        self.textBtn = wx.BitmapButton(self, -1, patchImg, (20, 20),
#                       (patchImg.GetWidth()+10, patchImg.GetHeight()+10))
        
        self.sizer.Add(self.patchBtn, 0,wx.EXPAND|wx.ALIGN_CENTER )
        self.sizer.Add(self.textBtn, 0,wx.EXPAND|wx.ALIGN_CENTER)
        self.sizer.Add(self.mouseBtn, 0,wx.EXPAND|wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)
class BuilderFrame(wx.Frame):

    def __init__(self, parent, id=-1, title='PsychoPy Builder',
                 pos=wx.DefaultPosition, size=(800, 600),files=None,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, id, title, pos, size, style)
        self.parent=parent
        self._mgr = wx.aui.AuiManager(self)
        
        # create several text controls
        self.flowPanel=FlowPanel(parent=self, size=(600,200))
        self.procPanel=ProceduresPanel(self)
        self.procButtons=ProcButtonsPanel(self)
        # add the panes to the manager
        self._mgr.AddPane(self.procPanel,wx.CENTER, 'Procedures')
        self._mgr.AddPane(self.procButtons, wx.RIGHT)
        self._mgr.AddPane(self.flowPanel,wx.BOTTOM, 'Flow')

        # tell the manager to 'commit' all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        # deinitialize the frame manager
        self._mgr.UnInit()
        # delete the frame
        self.Destroy()


class IDEApp(wx.App):
    def OnInit(self):
        if len(sys.argv)>1:
            if sys.argv[1]==__name__:
                args = sys.argv[2:] # program was excecuted as "python.exe PsychoPyIDE.py %1'
            else:
                args = sys.argv[1:] # program was excecuted as "PsychoPyIDE.py %1'
        else:
            args=[]
        self.frame = BuilderFrame(None, -1, 
                                      title="PsychoPy Experiment Builder",
                                      files = args)
                                     
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True
    def MacOpenFile(self,fileName):
        self.frame.setCurrentDoc(fileName) 

if __name__=='__main__':
    app = IDEApp(0)
    app.MainLoop()