from time import sleep

from cmap import *
from gui import *
from utils import *
import numpy as np

MAX_NODES = 20000

################################################################################
# NOTE:
# Before you start, please familiarize yourself with class Node in utils.py
# In this project, all nodes are Node object, each of which has its own
# coordinate and parent if necessary. You could access its coordinate by node.x
# or node[0] for the x coordinate, and node.y or node[1] for the y coordinate
################################################################################

def step_from_to(node0, node1, limit=75):
    ############################################################################
    # TODO: please enter your code below.
    # 1. If distance between two nodes is less than limit, return node1
    # 2. Otherwise, return a node in the direction from node0 to node1 whose
    #    distance to node0 is limit. Recall that each iteration we can move
    #    limit units at most
    # 3. Hint: please consider using np.arctan2 function to get vector angle
    # 4. Note: remember always return a Node object
    ############################################################################
    distance = get_dist(node0, node1)
    if distance < limit:
        return node1
    else:
        dy = node1.y-node0.y
        dx = node1.x-node0.x
        angle = np.arctan2(dy,dx)
        return Node((limit*np.cos(angle), limit*np.sin(angle)))

def node_generator(cmap):
    ############################################################################
    # TODO: please enter your code below.
    # 1. Use CozMap width and height to get a uniformly distributed random node
    # 2. Use CozMap.is_inbound and CozMap.is_inside_obstacles to determine the
    #    legitimacy of the random node.
    # 3. Note: remember always return a Node object
    ############################################################################
    xCoor = np.random.rand()*cmap.width
    yCoor = np.random.rand()*cmap.height
    rand_node = Node((xCoor,yCoor))  # xCoor and yCor needs to make a cordinate, and plus parent_node.

    while not cmap.is_inbound(rand_node) or cmap.is_inside_obstacles(rand_node):
        xCoor = np.random.rand()*cmap.width
        yCoor = np.random.rand()*cmap.height
        rand_node = Node((xCoor, yCoor))
    return rand_node

def RRT(cmap, start):
    cmap.add_node(start)

    map_width, map_height = cmap.get_size()
    while (cmap.get_num_nodes() < MAX_NODES):
        ########################################################################
        # TODO: please enter your code below.
        # 1. Use CozMap.get_random_valid_node() to get a random node. This
        #    function will internally call the node_generator above
        # 2. Get the nearest node to the random node from RRT
        # 3. Limit the distance RRT can move
        # 4. Add one path from nearest node to random node
        #
        ########################################################################
        rand_node = cmap.get_random_valid_node() #get random node
        nodes = cmap.get_nodes() # get lists of all nodes
        closest = float('inf'); #sets initial value to infinity

        for node in nodes: #iterate among all nodes
            dist = get_dist(node, rand_node) #loop finds the closest node to the rand_node
            if  dist < closest:
                closest = dist
                nearest_node = node
        rand_node = step_from_to(nearest_node, rand_node)
        sleep(0.01)
        cmap.add_path(nearest_node, rand_node)
        if cmap.is_solved():
            break

    if cmap.is_solution_valid():
        print("A valid solution has been found :-) ")
    else:
        print("Please try again :-(")

################################################################################
#                     DO NOT MODIFY CODE BELOW                                 #
################################################################################

class RRTThread(threading.Thread):
    """Thread to run cozmo code separate from main thread
    """

    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        while not stopevent.is_set():
            RRT(cmap, cmap.get_start())
            sleep(100)
            cmap.reset()
        stopevent.set()


if __name__ == '__main__':
    global grid, stopevent
    stopevent = threading.Event()
    cmap = CozMap("maps/map2.json", node_generator)
    visualizer = Visualizer(cmap)
    robot = RRTThread()
    robot.start()
    visualizer.start()
    stopevent.set()
