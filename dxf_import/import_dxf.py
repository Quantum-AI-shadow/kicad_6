import wx
import pcbnew
import os
import subprocess
import sys


## Defining functions ##
def fileDialog(fileType):
	openFileDialog = wx.FileDialog(None, "Open", "", "", "Kicad pcbnew files "+fileType, wx.FD_OPEN|wx.FD_FILE_MUST_EXIST)
	if(openFileDialog.ShowModal() == wx.ID_CANCEL):
		return
	else:
		return openFileDialog.GetPath()
	openFileDialog.Destroy()

def addZone(points, refresh = 1): #padConnection is thermal/solid
    board = pcbnew.GetBoard()
    zone = pcbnew.ZONE(board)
    zone.SetLayer(0)
    wx_vector = pcbnew.wxPoint_Vector(0)
    for point in points:
        pcbnew.wxPoint_Vector.append(wx_vector, pcbnew.wxPoint(point[0]*1e6, point[1]*1e6))
    zone.AddPolygon(wx_vector)
    board.Add(zone)
    if(refresh == 1):
        pcbnew.Refresh()

def addVia(pos, width, drill, refresh = 1):
	board = pcbnew.GetBoard()
	via = pcbnew.PCB_VIA(board)
	via.SetPosition(pcbnew.wxPoint(int(pos[0]*1e6), int(pos[1]*1e6)))
	via.SetDrill(int(drill*1e6))
	via.SetWidth(int(width*1e6))
	board.Add(via)
	if(refresh == 1):
		pcbnew.Refresh()

## class definition for plugin ##
class import_dxf(pcbnew.ActionPlugin):
	def defaults(self):
		self.name         = "DXF import to copper layer"
		self.category     = "Modify PCB"
		self.description  = "Importing dxf file as copper layer"
		self.show_toolbar = False

	def Run(self):
		try:
			import dxfgrabber
		except:
			import pip
			print("Installing dxfgrabber package")
			if hasattr(pip, 'main'):
				pip.main(['install', 'dxfgrabber'])
			else:
				pip._internal.main(['install', 'dxfgrabber'])
			import dxfgrabber

		filePath = fileDialog("(*.dxf)|*.dxf")
		if(filePath):
			try:
				dxf = dxfgrabber.readfile(filePath)
				output = [entity for entity in dxf.entities]
				viaCount = 0
				for entity in output:
					if((entity.dxftype == 'LWPOLYLINE') and (len(entity.points) > 2)):
						points = []
						for point in entity.points:
							points.append(list(point))
						addZone(points)
					if(entity.dxftype == 'CIRCLE'):
						rad = entity.radius
						center = entity.center[0:2]
						drill = rad*0.6
						viaCount += 1
						if(viaCount == 50):
							addVia(center, rad, drill)
							viaCount = 0
						else:
							addVia(center, rad, drill, 0)
			except:
				wx.LogMessage("DXF file is not proper!")
		pcbnew.Refresh()