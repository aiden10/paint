import os
import pyautogui
import time
import math
import random
import numpy as np

CURRENT_DIR = os.getcwd()
file_name = 'sphere.stl'
files_folder = os.path.join(CURRENT_DIR, 'STL')
file_path = os.path.join(files_folder, file_name)
camera_vector = [0, 0, 10]
TOP_LEFT = (640, 280)
TOP_RIGHT = (1275, 280)
BOTTOM_LEFT = (640, 910)
BOTTOM_RIGHT = (1275, 910)

def parse_STL(file):
    lines = file.readlines()
    facets = []
    vertices = []
    normal = []
    vertex_count = 0
    for line in lines:
        if 'normal' in line:
            n = line.split()[-3:]
            n = [num.strip() for num in n]
            n = [float(num) for num in n]
            normal.append(n)

        elif 'vertex' in line:
            vertex = line.split()[-3:]
            vertex = [num.strip() for num in vertex]
            vertex = [float(num) for num in vertex]
            vertices.append(vertex)
            vertex_count += 1

        if vertex_count == 3:
            facets.append((normal, vertices))
            vertex_count = 0
            vertices = []
            normal = []

    return facets

def is_visible(facet, camera):
    normal = facet[0][0]
    vertices = facet[1]
    view_vector = [
        vertices[0][0] - camera[0],
        vertices[0][1] - camera[1],
        vertices[0][2] - camera[2],
    ]
    return np.dot(view_vector, normal) > 0

def convert_2d(vertices, camera_vector):
    camera_x, camera_y, camera_z = camera_vector[0], camera_vector[1], camera_vector[2]
    projected_points = []
    for vertex in vertices:
        x, y, z = vertex[0], vertex[1], vertex[2] + 0.00001
        F = z - camera_z
        x_prime = ((x - camera_x) * (F/z) + camera_x)
        y_prime = ((y - camera_y) * (F/z) + camera_y)
        projected_points.append((x_prime, y_prime))
    return projected_points

def get_scales(projected_points):
    # Finds the largest and smallest x, y values of the projected points
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    for vertices in projected_points:
        for point in vertices:
            x, y = point[0], point[1]
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y

    scale_x = (TOP_RIGHT[0] - TOP_LEFT[0]) / (max_x - min_x)
    scale_y = (BOTTOM_LEFT[1] - TOP_LEFT[1]) / (max_y - min_y)
    
    return scale_x, scale_y, min_x, min_y

def rotate_x(facet, theta):
    x_rotation_matrix = [
    [1, 0, 0],
    [0, math.cos(theta), - math.sin(theta)],
    [0, math.sin(theta), math.cos(theta)] 
]
    for vertex in facet:
        for point in vertex:
            x, y, z = point[0], point[1], point[2]
            transformed_vector = np.matmul(x_rotation_matrix, [x, y, z])
            transformed_x, transformed_y, transformed_z = transformed_vector[0], transformed_vector[1], transformed_vector[2]

            vertex_index = facet.index(vertex) 
            point_index = vertex.index(point)
            # update the x, y, z
            facet[vertex_index][point_index][0] = transformed_x
            facet[vertex_index][point_index][1] = transformed_y
            facet[vertex_index][point_index][2] = transformed_z

def rotate_y(facet, theta):
    y_rotation_matrix = [
        [math.cos(theta), 0, math.sin(theta)],
        [0, 1, 0],
        [-math.sin(theta), 0, math.cos(theta)]
    ]
    for vertex in facet:
        for point in vertex:
            x, y, z = point[0], point[1], point[2]
            transformed_vector = np.matmul(y_rotation_matrix, [x, y, z])
            transformed_x, transformed_y, transformed_z = transformed_vector[0], transformed_vector[1], transformed_vector[2]

            vertex_index = facet.index(vertex) 
            point_index = vertex.index(point)
            # update the x, y, z
            facet[vertex_index][point_index][0] = transformed_x
            facet[vertex_index][point_index][1] = transformed_y
            facet[vertex_index][point_index][2] = transformed_z

def rotate_z(facet, theta):
    z_rotation_matrix = [
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ]
    for vertex in facet:
        for point in vertex:
            x, y, z = point[0], point[1], point[2]
            transformed_vector = np.matmul(z_rotation_matrix, [x, y, z])
            transformed_x, transformed_y, transformed_z = transformed_vector[0], transformed_vector[1], transformed_vector[2]

            vertex_index = facet.index(vertex) 
            point_index = vertex.index(point)
            # update the x, y, z
            facet[vertex_index][point_index][0] = transformed_x
            facet[vertex_index][point_index][1] = transformed_y
            facet[vertex_index][point_index][2] = transformed_z

def erase():
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press('delete')
    pencil_button()

def pencil_button():
    pyautogui.click((325, 110)) # pencil button

def change_color(hex):
    pyautogui.click((1300, 140)) # edit color
    time.sleep(0.35)
    pyautogui.click((1150, 220)) # hex text field
    time.sleep(0.35)
    pyautogui.hotkey('ctrl', 'a', 'backspace')
    time.sleep(0.35)
    pyautogui.write(hex)
    pyautogui.click((775, 850))

with open(file_path) as f:
    facets = parse_STL(f)

time.sleep(2)
erase()
while True:
    color = "%06x" % random.randint(0, 0xFFFFFF) # generate random hex color
    change_color(color)
    projected_points = []
    for facet in facets:
        # apply rotations
        rotate_x(facet, 25)
        rotate_y(facet, 25)
        rotate_z(facet, 25)
        if is_visible(facet, camera_vector): # check if facet is visible
            vertices = facet[1] # store its vertices
            projected_points.append(convert_2d(vertices, camera_vector)) # convert vertices to 2d

    scale_x, scale_y, min_x, min_y = get_scales(projected_points) # calculate scale

    for vertices in projected_points: 
        points = []
        for point in vertices:
            # calculate x,y position to draw the vertices
            x, y = point[0], point[1]
            scaled_x = TOP_LEFT[0] + ((x - min_x) * scale_x)
            scaled_y = TOP_LEFT[1] + ((y - min_y) * scale_y)
            points.append((scaled_x, scaled_y))
        p1, p2, p3 = points[0], points[1], points[2]
        
        # draw the line between the points
        pyautogui.moveTo(p1[0], p1[1])
        pyautogui.click()
        pyautogui.dragTo(p2[0], p2[1], button='left')
        pyautogui.dragTo(p3[0], p3[1], button='left')
        points = []
    