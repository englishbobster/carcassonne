import cv2
import json
import matplotlib.pyplot as plt


def do_something():
    # === Load & Resize ===
    img = cv2.imread("../test_images/tile.jpg")
    resized = cv2.resize(img, (300, 300))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # === HSV Feature Ranges ===
    masks = {
        "road": cv2.inRange(hsv, (0, 0, 200), (180, 40, 255)),          # white
        "city": cv2.inRange(hsv, (10, 50, 50), (30, 255, 255)),         # yellow/brown
        "field": cv2.inRange(hsv, (36, 25, 25), (90, 255, 255))         # green
    }

    grid = []
    cell_size = 100

    for row in range(3):
        row_labels = []
        for col in range(3):
            x1, y1 = col * cell_size, row * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size

            region_masks = {
                key: mask[y1:y2, x1:x2] for key, mask in masks.items()
            }

            label = classify_region(region_masks)
            row_labels.append(label)
        grid.append(row_labels)

    # === Save JSON ===
    with open("tile_quadrants.json", "w") as f:
        json.dump({"grid": grid}, f, indent=2)

    print("✅ Grid classification saved to tile_quadrants.json")

    # === Plot Result ===
    plt.figure(figsize=(6, 6))
    plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))

    # Draw grid and labels
    for row in range(3):
        for col in range(3):
            x, y = col * cell_size, row * cell_size
            label = grid[row][col]
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

# === Classify grid ===
def classify_region(region_masks):
    if cv2.countNonZero(region_masks["road"]) > 0:
        return "road"
    elif cv2.countNonZero(region_masks["city"]) > 0:
        return "city"
    else:
        return "field"

if __name__ == '__main__':
    do_something()