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
    img = cv2.imread("../test_images/tile_city_3_side.jpg")
    img = remove_white_border(img)
    resized_image = cv2.resize(img, (TILE_SIDE, TILE_SIDE))
    hsv_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2HSV)
    ports = classify_ports(hsv_image)
    draw_ports(resized_image, ports)
    write_json_file(ports)

def remove_white_border(image, threshold=245):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create a binary mask of "non-white" areas
    _, mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # Find bounding box of the non-white area
    coords = cv2.findNonZero(mask)
    x, y, w, h = cv2.boundingRect(coords)

    # Crop the image to that bounding box
    return image[y:y+h, x:x+w]


def write_json_file(ports):
    with open("tile.json", "w") as f:
        json.dump({"ports": ports}, f, indent=2)
    print("✅ Ports saved to tile.json")


def classify_ports(image):
    ports = []

    masks = {
        # === HSV field, city and road range colours ===
        # Conversion from HSV colorpicker values to cv2: colorpicker => (/2, *2.55, *2.55) => cv2
        "R": cv2.inRange(image, (0, 0, 230), (180, 25, 255)),  # white
        "C": cv2.inRange(image, (10, 50, 50), (30, 255, 255)),  # yellow/brown
        "F": cv2.inRange(image, (50, 100, 100), (70, 255, 255))  # green
    }

    for port_coord in range(1, 13):
        x1, y1 = EDGE_PORT_COORDS[port_coord][0], EDGE_PORT_COORDS[port_coord][1]
        x2, y2 = EDGE_PORT_COORDS[port_coord][2], EDGE_PORT_COORDS[port_coord][3]

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

    for port_coord in range(1, 13):
        x1, y1 = EDGE_PORT_COORDS[port_coord][0], EDGE_PORT_COORDS[port_coord][1]
        x2, y2 = EDGE_PORT_COORDS[port_coord][2], EDGE_PORT_COORDS[port_coord][3]
        label = ports[port_coord - 1]["type"]

        if port_coord in range(1, 4) or port_coord in range(7, 10):
            rect = plt.Rectangle((x1, y1), (x2 - x1), EDGE_THICKNESS, linewidth=1.5, edgecolor='red', facecolor='none')
        else:
            rect = plt.Rectangle((x1, y1), EDGE_THICKNESS, (y2 - y1), linewidth=1.5, edgecolor='red', facecolor='none')

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
    center_x = x + width // 2
    center_y = y + height // 2
    plt.text(center_x, center_y, label, color='white', fontsize=12, ha='center', va='center',
             bbox=dict(facecolor='black', alpha=0.6, boxstyle='round'))


if __name__ == '__main__':
    entry()