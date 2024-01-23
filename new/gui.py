import cv2

# Read input image
img = cv2.imread(r"C:\Users\hp\Desktop\new\audi3.jpg")

# Check if the image was loaded successfully
if img is None:
    print("Error: Unable to load the image.")
    exit()

# convert input image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# read haarcascade for number plate detection
cascade = cv2.CascadeClassifier('haarcascade_russian_plate_number.xml')

# Check if the cascade classifier was loaded successfully
if cascade.empty():
    print("Error: Unable to load the Haar Cascade XML file.")
    exit()

# Detect license number plates
plates = cascade.detectMultiScale(gray, 1.2, 5)
print('Number of detected license plates:', len(plates))

# loop over all plates
for (x, y, w, h) in plates:
    # draw bounding rectangle around the license number plate
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    gray_plates = gray[y:y+h, x:x+w]
    color_plates = img[y:y+h, x:x+w]

    # save number plate detected
    cv2.imwrite('Numberplate.jpg', gray_plates)

# Display the original image with bounding boxes
cv2.imshow('Number Plate Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
