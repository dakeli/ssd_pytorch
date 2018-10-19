import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cv2

img = cv2.imread("3.png")
save_folder='eval/'
cv2.rectangle(img, (100, 100), (367, 461), (0, 0, 255), 10)
# cv2.rectangle(img, (10, 10), (100, 100), (0, 0, 255), 10)
cv2.imwrite('contours.png', img)







img=cv2.imread("1.png")
plt.figure(8)
plt.imshow(img)
currentAxis = plt.gca()
rect = patches.Rectangle((100, 100), 200, 200, linewidth=1, edgecolor='r', facecolor='none')
currentAxis.add_patch(rect)
print('end')