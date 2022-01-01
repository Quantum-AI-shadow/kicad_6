import wx
import pcbnew
import os

def getNetID(netName):
    board = pcbnew.GetBoard()
    try:
       return board.GetNetcodeFromNetname(netName)
    except:
        return

def getLayerID(layerName):
    board = pcbnew.GetBoard()
    for i in range(1000):
        if(board.GetLayerName(i) == layerName):
            return i
    return

def addZone(points, layerName, netName, clearance = 0.5, refresh = 1): 
    board = pcbnew.GetBoard()
    zone = pcbnew.ZONE(board)
    zone.SetLayer(0)
    wx_vector = pcbnew.wxPoint_Vector(0)
    for point in points:
        pcbnew.wxPoint_Vector.append(wx_vector, pcbnew.wxPoint(point[0]*1e6, point[1]*1e6))
    zone.AddPolygon(wx_vector)
    zone.SetNetCode(getNetID(netName))
    zone.SetLayer(getLayerID(layerName))
    zone.SetLocalClearance(int(clearance*1e6))
    board.Add(zone)
    if(refresh == 1):
        pcbnew.Refresh()

def addVia(pos, width, drill, netName, refresh = 1):
    board = pcbnew.GetBoard()
    via = pcbnew.PCB_VIA(board)
    via.SetPosition(pcbnew.wxPoint(int(pos[0]*1e6), int(pos[1]*1e6)))
    via.SetDrill(int(drill*1e6))
    via.SetWidth(int(width*1e6))
    via.SetNetCode(getNetID(netName))
    board.Add(via)
    if(refresh == 1):
        pcbnew.Refresh()

def addTrack(start, end, layerName, netName, width, refresh = 1):
    board = pcbnew.GetBoard()
    track = pcbnew.PCB_TRACK(board)
    track.SetStart(pcbnew.wxPoint(start[0]*1e6, start[1]*1e6))
    track.SetEnd(pcbnew.wxPoint(end[0]*1e6, end[1]*1e6))
    track.SetLayer(getLayerID(layerName))
    track.SetNetCode(getNetID(netName))
    track.SetWidth(int(width*1e6))
    board.Add(track)
    if(refresh == 1):
        pcbnew.Refresh()

def getNetNames():
    board = pcbnew.GetBoard()
    netNames = []
    for i in board.GetNetsByName():
        netNames.append(i)
    return netNames

