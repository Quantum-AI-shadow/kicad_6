import pcbnew
from pcbnew import *

board = pcbnew.GetBoard()

def get_component(name):
    return [x for x in board.GetModules() if x.GetReference() == name][0]

def getnetID(netName):
    nets    = board.GetNetsByName()
    netCode = nets.find(netName).value()[1].GetNet()
    return netCode

def getLayerID(layerName):
    for i in range(pcbnew.PCB_LAYER_ID_COUNT):
        if(board.GetLayerName(i) == layerName):
            layerID = i
            return layerID

def addVia(x, y, drill, width, netName, refresh = 1):
    newVia = pcbnew.VIA(board)
    newVia.SetPosition(pcbnew.wxPoint(x*1e6, y*1e6))
    newVia.SetDrill(int(drill*1e6))
    newVia.SetWidth(int(width*1e6))
    newVia.SetNetCode(getnetID(netName))
    board.Add(newVia)
    if(refresh == 1):
        pcbnew.Refresh()

def addTrack(x1, y1, x2, y2, trackWidth, netName, layerName, refresh = 1):
    track = pcbnew.TRACK(board)
    track.SetStart(pcbnew.wxPoint(int(x1*1e6), int(y1*1e6)))
    track.SetEnd(pcbnew.wxPoint(int(x2*1e6), int(y2*1e6)))
    track.SetNetCode(getnetID(netName))
    track.SetLayer(getLayerID(layerName))
    board.Add(track)
    if(refresh == 1):
        pcbnew.Refresh()

def addZone(points, layerName, netName, padConnection, refresh = 1): #padConnection is thermal/solid
    zone = pcbnew.ZONE_CONTAINER(board)
    nets = board.GetNetsByName()
    netCode = nets.find(netName).value()[1].GetNet()
    zone.SetNetCode(netCode)
    zone.SetTimeStamp(420)
    zone.SetLayer(getLayerID(layerName))
    zone.SetPadConnection(padConnection)
    wx_vector = pcbnew.wxPoint_Vector(0)
    for point in points:
        pcbnew.wxPoint_Vector.append(wx_vector, pcbnew.wxPoint(point[0]*1e6, point[1]*1e6))
    zone.AddPolygon(wx_vector)
    board.Add(zone)
    if(refresh == 1):
        pcbnew.Refresh()
