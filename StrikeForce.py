# reversi.py

import wx
from copy import deepcopy
from math import floor
RUSSIAN = "Russian"
BLANK = "Empty"
AMERICAN = "American"
NULL_CELL = ' '
FOREST = 'Forest'
CITY = 'City'
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
        self.board = [[BLANK]* 9 for x in range(15)]

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
        self.unit = None
        self.over = False
        self.initial_board = deepcopy(self.board)
        self.battle = False
        
    def __getitem__(self, i):
        return self.board[i]  
    
    def reset_board(self):
        self.board = deepcopy(self.initial_board)
    
    def set_board(self):
        self.initial_board = deepcopy(self.board)
    
    def set_current(self, value):
        self.current = value
        
    def set_unit(self, value):
        self.unit = value
        
    def set_turns(self, value):
        self.turns = value
        

    
    def set_board_position(self, i, j, value):
        self.board[i][j] = value
        
    def check_city(self, row_column):
        for row in CITY_CELLS:
            if row == row_column:
                print("City!!!")
    def print_board(self):
        for row in self.board:
            print(row)
            
class Frame(wx.Frame):
    def __init__(self):
        style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX
        wx.Frame.__init__(self, None, -1, "Strike Force", style=style)
    
        self.panel = wx.Panel(self)
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.DisplayBoxInfo)
        self.panel.Bind(wx.EVT_PAINT, self.Refresh)
        self.Newgame(None)
    
        # Menubar.
        menu = wx.Menu()
        menu.Append(1, "Undo")
        menu.AppendSeparator()
        menu.Append(2, "Reset")
        menu.AppendSeparator()
        menu.Append(3, "End Turn")
        menu.AppendSeparator()
        menu.Append(4, "New Game")
        menu.AppendSeparator()
        menu.Append(5, "Quit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "Menu")
        
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.Reset, id=2)
        self.Bind(wx.EVT_MENU, self.EndTurn, id=3)
        self.Bind(wx.EVT_MENU, self.Newgame, id=4)
        self.Bind(wx.EVT_MENU, self.Quit, id=5)
    
        # Status bar.
        self.CreateStatusBar()
     
        self.Show()
        
    def Reset(self, event):
        if self.strikeforce.battle == False:
            self.strikeforce.reset_board()
            self.panel.Refresh()
            
    def EndTurn(self, event):
        
        if self.strikeforce.current == RUSSIAN:
            self.strikeforce.set_current(AMERICAN)
        else:
            self.strikeforce.set_current(RUSSIAN)
            self.strikeforce.set_turns(self.strikeforce.turns + 1)
            print("Start of Turn: {}".format(self.strikeforce.turns))
        self.strikeforce.set_unit(None)
        self.strikeforce.set_board()
        self.panel.Refresh()   

    def get_position(self, x, y):
        column_index = floor(x)
        if column_index % 2 == 0:
            row_index = floor(y)*2
            if row_index > 14:
                return None
        else:
            initial_position = y
            if initial_position < 0.5 or initial_position > 7.5:
                return None
            
            elif initial_position < 1.5:
                row_index = 1
            elif initial_position < 2.5:
                row_index = 3
            elif initial_position < 3.5:
                row_index = 5
            elif initial_position < 4.5:
                row_index = 7
            elif initial_position < 5.5:
                row_index = 9
            elif initial_position < 6.5:
                row_index = 11
            elif initial_position < 7.5:
                row_index = 13
        return (row_index, column_index)

    def DisplayBoxInfo(self, event):

        # Calculate coordinate from window coordinate.
        winx,winy = event.GetX(), event.GetY()
        w,h = self.panel.GetSize()
        print(winx, winy)
        x = winx / (w/9)
        y = winy / (h/9)
        
        row_column = self.get_position(x,y)
        if row_column:
            print(self.strikeforce[row_column[0]][row_column[1]])
            self.strikeforce.check_city(row_column)
            if self.strikeforce.current == self.strikeforce[
                    row_column[0]][row_column[1]]:
                if self.strikeforce.unit == row_column:
                    
                    print('{} infantry deselected'.format(self.strikeforce.current))
                    self.strikeforce.unit = None
                else:
                    print('{} infantry selected'.format(self.strikeforce.current))
                    self.strikeforce.unit = row_column
            elif self.strikeforce[row_column[0]][row_column[1]] == BLANK:
                if self.strikeforce.unit:
                    print("moving unit")
                    self.strikeforce.set_board_position(self.strikeforce.unit[0], self.strikeforce.unit[1], BLANK)
                    self.strikeforce.set_board_position(row_column[0],row_column[1], self.strikeforce.current)
                    self.strikeforce.unit = row_column
                    self.panel.Refresh()
                    
    def Quit(self, event):
        self.Close()
    
    def Newgame(self, event):
        
        self.strikeforce = StrikeForce()
        print('refreshing')
        self.panel.Refresh()


    def Refresh(self, event):
        print('refreshing screen')
        self.strikeforce.print_board()
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