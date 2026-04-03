from tkinter import *
import random
import math

'''Bounds any point set with the smallest sided polygon whose vertices belong to the point set'''
'''Approach: Take max_y point, then find point which forms max angle. This becomes current point (pivot) and find largest
 angle w.r.t. previous point. Iterate till start point.'''


class BoundingPolygon:
    def __init__(self):
        self.pl = []
        self.numOfPoints = 10
        self.done = False
        self.window = Tk()
        self.window.geometry("550x600")
        self.window.title("Bounding Polygon")
        self.canvas = Canvas(self.window, height=500, width=500, bg="white")
        self.canvas.grid(row=1, column=1)
        self.frame = Frame(self.window)
        self.frame.grid(row=2, column=1)
        self.frame2 = Frame(self.window).grid(row=3, column=1)
        b = Button(self.frame, text="Generate New Point Set",
                   command=self.create_new_points)
        b.grid(row=1, column=1)
        b1 = Button(self.frame, text="Draw Bounding Polygon",
                    command=self.draw)
        b1.grid(row=1, column=2)
        self.canvas.bind('<Button-1>', self.addPoint)
        Label(self.frame2, text="").grid(row=2, column=1)
        Label(self.frame2, text="Click to add point.",
              fg="grey").grid(row=3, column=1)
        self.window.mainloop()

    def create_new_points(self):
        self.done = False
        self.canvas.delete('all')
        px = 5  # Point width
        self.pl = []  # format --> [[x0,y0],[x1,y1],[x2,y2],...]
        for i in range(self.numOfPoints):
            x = random.randint(20, 480)
            y = random.randint(20, 480)
            self.canvas.create_oval(x-px, y-px, x+px, y+px, fill="grey")
            point = [x, y]
            self.pl.append(point)

    def addPoint(self, event):
        '''To add a point by clicking on location'''
        x = event.x
        y = event.y
        px = 5
        self.canvas.create_oval(x-px, y-px, x+px, y+px, fill="grey")
        self.pl.append([x, y])
        self.canvas.delete('line')
        if self.done:
            self.draw()

    def draw(self):
        '''Draws the bounding polygon for any given set of points.'''
        if self.pl != []:
            self.done = True
            self.canvas.delete('lines')
            # Start with max y
            max_y = self.pl[0][1]
            max_y_point = self.pl[0]
            for i in self.pl:
                if i[1] > max_y:
                    max_y_point = i
                    max_y = i[1]

            current_x = max_y_point[0]    # Initialise with max_y point
            current_y = max_y_point[1]

            # Reference to stop iteration (loop ends upon reaching this point)
            start_x = current_x
            start_y = current_y

            # Any point along the same horizontal (to calculate initial largest angle)
            prev_x = current_x - 20
            prev_y = current_y

            max_angle = 0
            for point in self.pl:
                if point != [current_x, current_y] != [prev_x, prev_y]:
                    angle = self.find_angle(
                        current_x, current_y, prev_x, prev_y, point[0], point[1])
                    if angle > max_angle:
                        max_angle = angle
                        max_angle_point = point
            self.canvas.create_line(
                current_x, current_y, max_angle_point[0], max_angle_point[1], fill="blue", width="1.5", tags="line")

            # Modify current point
            current_x, current_y = max_angle_point[0], max_angle_point[1]

            # Draw rest of the polygon
            run = True
            while run:
                max_angle = 0
                for point in self.pl:
                    if [current_x, current_y] != point != [prev_x, prev_y]:  # avoid div by 0 error
                        angle = self.find_angle(
                            current_x, current_y, prev_x, prev_y, point[0], point[1])
                        if angle > max_angle:
                            max_angle = angle
                            max_angle_point = point

                # Make bounding polygon blue
                self.canvas.create_line(
                    current_x, current_y, max_angle_point[0], max_angle_point[1], fill="blue", width=1.5, tags="line")

                if [current_x, current_y] == [start_x, start_y]:  # if back to start, end
                    run = False

                # Modify values
                prev_x = current_x
                prev_y = current_y
                current_x = max_angle_point[0]
                current_y = max_angle_point[1]

    def find_angle(self, x_pivot, y_pivot, x_hori, y_hori, x_new, y_new):
        '''Returns angle formed by 3 points (1 pivot)'''
        vec1_x = x_pivot - x_hori
        vec1_y = y_pivot - y_hori
        vec2_x = x_pivot - x_new
        vec2_y = y_pivot - y_new
        angle = math.acos((vec1_x * vec2_x + vec1_y * vec2_y) / (
            (math.sqrt(vec1_x**2 + vec1_y**2)) * (math.sqrt(vec2_x**2 + vec2_y**2))))
        return angle


BoundingPolygon()
