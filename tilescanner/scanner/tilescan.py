import json

import cv2
import matplotlib.pyplot as plt

EDGE_THICKNESS = 10
TILE_SIDE = 300
EDGE_PORT_COORDS = {
    1: (0, 0, 100, EDGE_THICKNESS),
    2: (100, 0, 200, EDGE_THICKNESS),
    3: (200, 0, 300, EDGE_THICKNESS),
    4: (300 - EDGE_THICKNESS, 0, 300, 100),
    5: (300 - EDGE_THICKNESS, 100, 300, 200),
    6: (300 - EDGE_THICKNESS, 200, 300,300),
    7: (200, 300 - EDGE_THICKNESS, 300,300),
    8: (100, 300 - EDGE_THICKNESS, 200, 300),
    9: (0, 300 - EDGE_THICKNESS, 100, 300),
    10: (0, 200, EDGE_THICKNESS, 300),
    11: (0, 100, EDGE_THICKNESS, 200),
    12: (0, 0, EDGE_THICKNESS, 100)
}


def entry():
    # === Prepare and Normalize the image ===
    img = cv2.imread("../test_images/tile_2.jpg")
    resized_image = cv2.resize(img, (TILE_SIDE, TILE_SIDE))
    hsv = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)

    # === HSV Feature Range Colours ===
    masks = {
        "R": cv2.inRange(hsv, (0, 0, 200), (180, 40, 255)),  # white
        "C": cv2.inRange(hsv, (44, 50, 50), (30, 255, 255)),  # yellow/brown
        "F": cv2.inRange(hsv, (36, 25, 25), (90, 255, 255))  # green
    }

    ports = classify_ports(masks)
    draw_ports(resized_image, ports)
    write_json_file(ports)


def write_json_file(ports):
    with open("tile.json", "w") as f:
        json.dump({"ports": ports}, f, indent=2)
    print("✅ Ports saved to tile.json")


def classify_ports(masks):
    ports = []
    for port_coord in range(1, 13):
        x1, y1 = EDGE_PORT_COORDS[port_coord][0], EDGE_PORT_COORDS[port_coord][1]
        x2, y2 = x1 + EDGE_PORT_COORDS[port_coord][2], EDGE_PORT_COORDS[port_coord][3]

        region_masks = {
            key: mask[y1:y2, x1:x2] for key, mask in masks.items()
        }

        classification = classify_region(region_masks)
        ports.append({"id": port_coord, "type": classification})
    return ports


def classify_region(region_masks):
    if cv2.countNonZero(region_masks["R"]) > 0:
        return "R"
    elif cv2.countNonZero(region_masks["C"]) > cv2.countNonZero(region_masks["F"]):
        return "C"
    else:
        return "F"


def draw_ports(image, ports):
    plt.figure(figsize=(6, 6))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    for port_coord in range(12):
        x, y = EDGE_PORT_COORDS[port_coord + 1][0], EDGE_PORT_COORDS[port_coord + 1][1]
        label = ports[port_coord]["type"]

        if port_coord in range(3) or port_coord in range(6, 9):
            rect = plt.Rectangle((x, y), 100, 10, linewidth=1.5, edgecolor='red', facecolor='none')
        else:
            rect = plt.Rectangle((x, y), 10, 100, linewidth=1.5, edgecolor='red', facecolor='none')

        plt.gca().add_patch(rect)
        add_region_label(label, rect)

    plt.title("Edge Feature Classification")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def add_region_label(label, rect):
    x, y = rect.get_xy()
    width = rect.get_width()
    height = rect.get_height()
    center_x = x + width / 2
    center_y = y + height / 2
    plt.text(center_x, center_y, label, color='white', fontsize=9, ha='center', va='center',
             bbox=dict(facecolor='black', alpha=0.6, boxstyle='round'))


if __name__ == '__main__':
    entry()