# reversi.py

import wx
from copy import deepcopy
RUSSIAN = -1
BLANK = 0
AMERICAN = 1
NULL_CELL = ' '
FOREST = 'F'
CITY = 'C'
RUSSIAN_START_CELLS = [
    (0, 8),
    (1 ,7),
    (2, 8),
    (11,7),
    (12,8),
    (14,8)
    ]
AMERICAN_START_CELLS = [
    (2, 2),
    (5 ,3),
    (9, 3),
    (13,1)    
    ]

CITY_CELLS = [
    (12, 0),
    (2 ,2),
    (5, 3)
    ]

FOREST_CELLS = [
    (11, 1),
    (12 ,2),
    (4, 2),
    (10, 4),
    (5, 5)
    ]

def Notify(caption, message):
    dialog = wx.MessageDialog(None, 
                          message=message, 
                          caption=caption, 
                          style=wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

class StrikeForce(object):
    def __init__(self):
        self.board = [[0]* 9 for x in range(15)]

        for i in range(15):
            for j in range(9):
                if (i + j) % 2 != 0:
                    self.board[i][j] = NULL_CELL
                    
        for row in RUSSIAN_START_CELLS:
            self.board[row[0]][row[1]] = RUSSIAN
            
        for row in AMERICAN_START_CELLS:
            self.board[row[0]][row[1]] = AMERICAN
            
        for row in FOREST_CELLS:
            self.board[row[0]][row[1]] = FOREST
        #need new data representation to check for cities.    
        #for row in CITY_CELLS:
        #    self.board[row[0]][row[1]] = CITY
            
        for row in self.board:
            print(row)
        self.turns = 1              # Turn counter.
        self.current = RUSSIAN        # Current player.
       
        self.over = False

    def __getitem__(self, i):
        return self.board[i]




class Frame(wx.Frame):
    def __init__(self):
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None, -1, "Strike Force", style=style)
    
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_PAINT, self.Refresh)
        self.Newgame(None)
    
        # Menubar.
        menu = wx.Menu()
        menu.Append(1, "New game")
        menu.AppendSeparator()
        menu.Append(2, "Quit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "Menu")
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Newgame, id=1)
        self.Bind(wx.EVT_MENU, self.Quit, id=2)
    
        # Status bar.
        self.CreateStatusBar()
     
        self.Show()



    def Quit(self, event):
        self.Close()
    
    def Newgame(self, event):
        # Initialize reversi and Refresh screen.
        
        self.strikeforce = StrikeForce()
        print('refreshing')
        self.panel.Refresh()


    def Refresh(self, event):
        print('refreshing screen')
        dc = wx.AutoBufferedPaintDCFactory(self.panel)
        dc = wx.GCDC(dc)
        w,h = self.panel.GetSize()
        print(w, h)
        # Background.
        dc.SetBrush(wx.Brush("#456F98"))
        dc.DrawRectangle(0,0,w,h)
        # Grid.
        
        px,py = w/9,h/9
        dc.SetBrush(wx.Brush("#4b5320"))
        for i in range(15):
            for j in range(9):
                c = self.strikeforce[i][j]
                if c == NULL_CELL:
                    continue
                if (i+j) % 2 == 0:
                    dc.DrawEllipse(j*px , i/2*py , px, py)
                else:
                    dc.DrawEllipse(j*px , i/2*py , px, py)
        dc.DrawLine(w-1, 0, w-1, h-1)
        dc.DrawLine(0, h-1, w-1, h-1)
        # Stones.
        brushes = {RUSSIAN: wx.Brush("red"), AMERICAN: wx.Brush("green") ,
                   FOREST: wx.Brush("#013B0E")}
        for i in range(15):
            for j in range(9):
                c = self.strikeforce[i][j]
                if c != BLANK and c != NULL_CELL:
                    dc.SetBrush(brushes[c])
                    dc.DrawEllipse(j*px , i/2*py , px, py)
                    
        for coordinate in CITY_CELLS:
            dc.DrawLine(coordinate[1]*px, coordinate[0]/2*py, 
                        (coordinate[1]+1)*px, (coordinate[0])/2*py)
            
            dc.DrawLine(coordinate[1]*px , (coordinate[0]+2)/2*py, 
                        (coordinate[1]+1)*px , (coordinate[0]+2)/2*py)
            
            dc.DrawLine(coordinate[1]*px, (coordinate[0])/2*py, 
                        (coordinate[1])*px, (coordinate[0]+2)/2*py)
            
            dc.DrawLine((coordinate[1]+1)*px , (coordinate[0])/2*py, 
                        (coordinate[1]+1)*px , (coordinate[0]+2)/2*py)
            dc.DrawLine((coordinate[1])*px , (coordinate[0])/2*py , 
                        (coordinate[1]+1)*px , (coordinate[0]+2)/2*py )
            dc.DrawLine((coordinate[1])*px , (coordinate[0]+2)/2*py , 
                        (coordinate[1]+1)*px , (coordinate[0])/2*py )
def main():
    app = wx.App(False)
    frame = Frame()
    frame.SetSize((450, 600))
    app.MainLoop()

if __name__ == '__main__':
    main()