import json

import cv2
import matplotlib.pyplot as plt

EDGE_THICKNESS = 10
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
    tile_side = 300
    img = cv2.imread("../test_images/tile.jpg")
    resized = cv2.resize(img, (tile_side, tile_side))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # === HSV Feature Range Colours ===
    masks = {
        "R": cv2.inRange(hsv, (0, 0, 200), (180, 40, 255)),  # white
        "C": cv2.inRange(hsv, (10, 50, 50), (30, 255, 255)),  # yellow/brown
        "F": cv2.inRange(hsv, (36, 25, 25), (90, 255, 255))  # green
    }

    # === Determine the edges ===
    cell_size, cells_per_side, grid = classify_edges(masks, tile_side)

    # === Save JSON ===
    with open("tile_quadrants.json", "w") as f:
        json.dump({"grid": grid}, f, indent=2)

    print("✅ Grid classification saved to tile_quadrants.json")

    # === Plot Result ===
    plt.figure(figsize=(6, 6))
    plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    draw_ports(cell_size, cells_per_side, grid)


def classify_edges(masks, tile_side):
    ports = []
    cells_per_side = 3
    cell_size = tile_side // cells_per_side
    row_labels = []
    for port_coord in range(12):
        x1, y1 = EDGE_PORT_COORDS[port_coord + 1][0], EDGE_PORT_COORDS[port_coord + 1][1]
        x2, y2 = x1 + EDGE_PORT_COORDS[port_coord + 1][2], EDGE_PORT_COORDS[port_coord + 1][3]

        region_masks = {
            key: mask[y1:y2, x1:x2] for key, mask in masks.items()
        }

        label = label_region(region_masks)
        row_labels.append(label)
        ports.append(row_labels)
    return cell_size, cells_per_side, ports


def draw_ports(cell_size, cells_per_side, ports):
    # Draw grid and labels
    for row in range(cells_per_side):
        for col in range(cells_per_side):
            x, y = col * cell_size, row * cell_size
            label = ports[row][col]
            # Draw rectangle
            rect = plt.Rectangle((x, y), cell_size, cell_size, linewidth=1.5, edgecolor='red', facecolor='none')
            plt.gca().add_patch(rect)
            # Draw label
            plt.text(x + 50, y + 55, label, color='white', fontsize=9, ha='center', va='center',
                     bbox=dict(facecolor='black', alpha=0.6, boxstyle='round'))
    plt.title("Quadrant Feature Classification")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


def label_region(region_masks):
    if cv2.countNonZero(region_masks["R"]) > 0:
        return "R"
    elif cv2.countNonZero(region_masks["C"]) > 0:
        return "C"
    else:
        return "F"

if __name__ == '__main__':
    entry()