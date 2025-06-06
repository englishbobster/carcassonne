import cv2
import numpy as np

def find_tile_contour_old(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            return approx.reshape(4, 2)
    return None

def find_tile_contour(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in sorted(contours, key=cv2.contourArea, reverse=True):
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.isContourConvex(approx):
            return approx.reshape(4, 2)
    return None


def order_points(pts):
    # Order: top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]   # top-left
    rect[2] = pts[np.argmax(s)]   # bottom-right
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect

def warp_tile(image, pts, size=300):
    rect = order_points(pts)
    dst = np.array([
        [0, 0],
        [size - 1, 0],
        [size - 1, size - 1],
        [0, size - 1]], dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (size, size))
    return warped

def main():
    W=640
    H=480
    cap = cv2.VideoCapture(0, cv2.CAP_ANY)
#    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('Y','U','Y','V'))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
#    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
#    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
#    cap.set(cv2.CAP_PROP_FPS, 30)
    print("Press 's' to capture tile, 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        display_frame = frame.copy()
        tile = find_tile_contour(frame)
        if tile is not None:
            cv2.polylines(display_frame, [tile], True, (0, 255, 0), 2)

        cv2.imshow("Camera", display_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s') and tile is not None:
            warped = warp_tile(frame, tile)
            cv2.imshow("Warped Tile", warped)
            cv2.imwrite("tile.png", warped)
            print("Tile saved as tile.png")
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

#=== This seems to be able to grab a tile on a white background, a desk top for instance

if __name__ == "__main__":
    main()