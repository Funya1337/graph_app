from tkinter import *
import os

root = Tk()
root.resizable(False, False)
myCanvas = Canvas(root, width=500, height = 500)
myCanvas.pack()

centers = []
ids = []
radius = 20

class Vertex():
    def __init__(self, r, canvasName, buff, color):
        self.r = r
        self.color = color
        self.canvasName = canvasName
        self.buff = buff

    def createVertex(self, x, y):
        x0 = x - self.r
        y0 = y - self.r
        x1 = x + self.r
        y1 = y + self.r
        return self.canvasName.create_oval(x0, y0, x1, y1, fill=self.color)

    def selectVertex(self, num):
        if self.canvasName.itemconfig(num)['fill'][-1] == 'red':
            self.buff.append(num)
            self.canvasName.itemconfig(num, fill = 'blue')
        else:
            try:
                idx = self.buff.index(num)
                del self.buff[idx]
            except:
                pass
            self.canvasName.itemconfig(num, fill = 'red')

    def getBuff(self):
        return self.buff

    def clearBuff(self):
        self.buff = []

class Line():
    def __init__(self, color, width, points, canvasName):
        self.color = color
        self.points = points
        self.canvasName = canvasName
        self.width = width

    def createLine(self, x0, y0, x1, y1):
        self.canvasName.create_line(x0, y0, x1, y1, fill = self.color, width = self.width)

    def addDataToPoints(self, data):
        self.points.append(data)

    def getPoints(self):
        return self.points

def plotGraph():
    output = open('output.txt', 'w')
    points = line.getPoints()
    graph = [[0] * len(ids) for _ in range(len(ids))]
    for i in range(len(graph)):
        for j in range(len(graph)):
            for k in range(len(points)):
                graph[points[k][0] - 1][points[k][1] - 1] = 1
                graph[points[k][1] - 1][points[k][0] - 1] = 1

    for i in graph:
        print(*i)
        output.write(" ".join(str(x) for x in i))
        output.write('\n')
    output.close()

def clearCanvas():
    root.destroy()
    os.startfile("graph.py")

def getCoords(event):
    global x, y
    x = event.x
    y = event.y
    for i in range(len(centers)):
        if (x - centers[i][0])**2 + (y - centers[i][1])**2 <= radius**2:
            vertex.selectVertex(i + 1)
            break
    else:
        ids.append(vertex.createVertex(x, y))
        centers.append((x, y))

    buff = vertex.getBuff()

    if len(buff) == 2:
        x0 = centers[buff[0] - 1][0]
        y0 = centers[buff[0] - 1][1]
        x1 = centers[buff[1] - 1][0]
        y1 = centers[buff[1] - 1][1]

        line.createLine(x0, y0, x1, y1)
        line.addDataToPoints(buff)
        
        myCanvas.itemconfig(buff[0], fill = 'red')
        myCanvas.itemconfig(buff[1], fill = 'red')
        vertex.clearBuff()

vertex = Vertex(radius, myCanvas, [], 'red')
line = Line('green', 5, [], myCanvas)
btn = Button(root, text = 'Create Matrix', bd = '5', command = plotGraph)
clearBtn = Button(root, text = 'Clear Canvas', bd = '5', command = clearCanvas)
btn.pack(side = 'bottom')
clearBtn.pack(side = 'bottom')
myCanvas.bind('<Button 1>', getCoords)
myCanvas.pack()
root.mainloop()
