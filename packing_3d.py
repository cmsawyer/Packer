from random import randint
from graphics import *


class Node():
    def __init__(self, x, y, z, width, height, length):
        self.used = False
        self.l = None
        self.d = None
        self.r = None
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.length = length
        self.xyView = Rectangle(Point(x, y), Point(x + width, y + height))
        self.zyView = Rectangle(Point(y, z), Point(y + height, z + length))
        self.xzView = Rectangle(Point(z, x), Point(z + length, x + width))


class Tree():
    def __init__(self, width, height, length):
        self.root = Node(x=0, y=0, z=0, width=width, height=height, length=length)

    def fit(self, blocks):
        for block in blocks:
            node = self.findNode(self.root, block['width'], block['height'], block['length'])
            if node is not None:
                block['fit'] = self.splitNode(node, block['width'], block['height'], block['length'])

    def findNode(self, node, width, height, length):
        if node.used is True:
            return self.findNode(node.r, width, height, length) \
                   or self.findNode(node.l, width, height, length) \
                   or self.findNode(node.d, width, height, length)
        elif width <= node.width and height <= node.height and length <= node.length:
            return node
        else:
            return None

    def splitNode(self, node, width, height, length):
        node.used = True
        # dim = x-y (l-r), z-y (d-r), x-z (l-d)
        # node with adjusted width
        node.r = Node(x=node.x + width, y=node.y, z=node.z,
                      width=node.width - width, height=height, length=length)
        # node with adjusted height
        node.l = Node(x=node.x, y=node.y + height, z=node.z,
                      width=node.width, height=node.height - height, length=length)
        # node with adjusted length
        node.d = Node(x=node.x, y=node.y, z=node.z + length,
                      width=node.width, height=node.height, length=node.length - length)
        node.xyView = Rectangle(Point(node.x, node.y),
                                Point(node.x + width, node.y + height))
        node.zyView = Rectangle(Point(self.root.length - node.z, node.y),
                                Point(self.root.length - (node.z + length), node.y + height))
        # (0, 0), (0, 128), (0, 64), (0, 32), (0, 16), (0, 8), (0, 4), (0, 2)
        node.xzView = Rectangle(Point(node.x, self.root.length - node.z),
                                Point(node.x + width, self.root.length - (node.z + length)))
        return node


def main(dim, blocks):
    print(len(blocks), 'blocks', blocks)
    padding = 25
    # Draw the canvas
    win = GraphWin("Binary Fill",
                   dim['width'] + dim['length'] + padding * 4,  # x dim of window
                   dim['height'] + dim['length'] + padding * 4)  # y dim of window
    canvas = [{'axis': Line(Point(padding, padding), Point(padding + dim['width'], padding)),
               'label': Text(Point(int(padding + dim['width'] / 2), int(padding / 2)), 'X')},  # topleft X
              {'axis': Line(Point(padding, padding), Point(padding, padding + dim['height'])),
               'label': Text(Point(int(padding / 2), int(padding + dim['height'] / 2)), 'Y')},  # topleft Y
              {'axis': Line(Point(win.width - padding, padding), Point(win.width - dim['length'] - padding, padding)),
               'label': Text(Point(win.width - padding - int(dim['length'] / 2), int(padding / 2)), 'Z')},  # topright Z
              {'axis': Line(Point(win.width - padding, padding), Point(win.width - padding, padding + dim['height'])),
               'label': Text(Point(win.width - int(padding / 2), padding + int(dim['height'] / 2)), 'Y')},  # topright Y
              {'axis': Line(Point(padding, win.height - padding), Point(padding + dim['width'], win.height - padding)),
               'label': Text(Point(padding + int(dim['width'] / 2), win.height - int(padding / 2)), 'X')},
              # bottomleft X
              {'axis': Line(Point(padding, win.height - padding), Point(padding, win.height - dim['length'] - padding)),
               'label': Text(Point(int(padding / 2), win.height - padding - int(dim['length'] / 2)),
                             'Z')}]  # bottomleft Z
    # Fit blocks to nodes in the tree space
    for obj in canvas:
        obj['axis'].draw(win)
        obj['label'].draw(win)
    tree = Tree(dim['width'], dim['height'], dim['length'])
    tree.fit(blocks)
    unfit = []
    # Draw blocks to the canvas
    for block in blocks:
        fit = block['fit']
        if fit is not None:
            xyCuboid = fit.xyView
            zyCuboid = fit.zyView
            xzCuboid = fit.xzView
            r = int((int((fit.x * 2 + fit.width) / 2) * 255) / dim['width'])
            g = int((int((fit.y * 2 + fit.height) / 2) * 255) / dim['height'])
            b = int((int((fit.z * 2 + fit.length) / 2) * 255) / dim['length'])
            # Draw the X-Y View in the bottom right
            xyCuboid.setFill(color_rgb(r, g, b))
            xyCuboid.move(padding, padding)
            xyCuboid.draw(win)
            # Draw Z-Y View in the bottom left
            zyCuboid.setFill(color_rgb(r, g, b))
            zyCuboid.move(dim['width'] + (padding * 3), padding)
            zyCuboid.draw(win)
            # Draw Z-X View in the top right
            xzCuboid.setFill(color_rgb(r, g, b))
            xzCuboid.move(padding, dim['height'] + (padding * 3))
            xzCuboid.draw(win)
        else:
            unfit.append(block)
    print(len(unfit), 'unfit blocks', unfit)
    win.getMouse()
    win.close()


def setup():
    dim256 = {'width': 256, 'height': 256, 'length': 256}
    dimTrailer = {'width': 105, 'height': 99, 'length': 564}

    random = []
    for i in range(0, randint(64, 128)):
        width = randint(16, 128)
        height = randint(16, 128)
        length = randint(16, 128)
        random.append({'width': width, 'height': height, 'length': length, 'fit': None})
    big = []
    for i in range(0, 5):
        size = 128
        big.append({'width': 256, 'height': 128, 'length': 128, 'fit': None})
    tall = [{'width': 256, 'height': 256, 'length': 128, 'fit': None},
            {'width': 256, 'height': 256, 'length': 128, 'fit': None}]
    power2 = []
    for i in range(0, 7):
        size = 2 ** (i + 1)
        for y in range(0, int(256 / size)):
            power2.append({'width': size, 'height': size, 'length': size, 'fit': None})
    randpower = []
    for i in range(0, 7):
        size = 2 ** (i + 1)
        for y in range(0, int(256 / size) * randint(1, 8)):
            randpower.append({'width': size, 'height': size, 'length': size, 'fit': None})
    pallets = []
    for i in range(0, 64):
        height = randint(25, 90)
        pallets.append({'width': 48, 'height': height, 'length': 44, 'fit': None})

    dim = dimTrailer
    blocks = sorted(pallets, key=lambda x: (x['width'], x['height'], x['length']), reverse=True)
    return {'dim': dim, 'blocks': blocks}


info = setup()
main(info['dim'], info['blocks'])
