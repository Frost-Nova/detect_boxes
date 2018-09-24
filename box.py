import cv2
from matplotlib import pyplot as plt

class find_box:

    def __init__(self, filename, binary_threshold=200, min_area=5000):
        self.name = filename
        self.structure_size = 40
        self.binary_threshold = binary_threshold
        self.min_area = min_area

    # Using erosion followed by dilation to find table grids
    def get_mask_joint(self, img):
        h_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (self.structure_size, 1))
        #h_erosion = cv2.erode(img, h_kernel, iterations=1)
        #h = cv2.dilate(h_erosion, h_kernel, iterations=1)
        h = cv2.morphologyEx(img, cv2.MORPH_OPEN, h_kernel)
        v_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, self.structure_size))
        #v_erosion = cv2.erode(img, v_kernel, iterations=1)
        #v = cv2.dilate(v_erosion, v_kernel, iterations=1)
        v = cv2.morphologyEx(img, cv2.MORPH_OPEN, v_kernel)
        mask = h + v
        #joint = cv2.bitwise_and(h, h, mask=v)
        return mask

    # From grid mask get bounding rectangles(boxes)
    def get_boxes(self, contours, width, height):
        rectangle = []
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            # Filter contours too small or too large
            if area<self.min_area or area>width*height/2:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            rectangle.append([[x,y], [x+w,y], [x+w,y+h], [x,y+h], [x,y]])
        return rectangle
    
    def find_box(self):
        img = cv2.imread(self.name)
        h, w = img.shape[:2]
        # Convert image to grayscale and invert color
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(img_gray, self.binary_threshold, 255, cv2.THRESH_BINARY_INV)

        # Find grid mask
        mask = self.get_mask_joint(thresh)
        _, contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Find and draw boxes in the grid mask
        rectangles = self.get_boxes(contours, w, h)
        for rect in rectangles:
            cv2.rectangle(img, tuple(rect[0]), tuple(rect[2]), (200,0,200), 3)
        return img, rectangles

    def plot(self, img):
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()
