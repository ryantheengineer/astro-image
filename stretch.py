from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import argparse

# Method to process the red band of the image
def normalizeRed(intensity):
    iI      = intensity

    minI    = 86
    maxI    = 230

    minO    = 0
    maxO    = 255

    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO

# Method to process the green band of the image
def normalizeGreen(intensity):
    iI      = intensity

    minI    = 90
    maxI    = 225

    minO    = 0
    maxO    = 255

    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO

# Method to process the blue band of the image
def normalizeBlue(intensity):
    iI      = intensity

    minI    = 100
    maxI    = 210

    minO    = 0
    maxO    = 255

    iO      = (iI-minI)*(((maxO-minO)/(maxI-minI))+minO)
    return iO

def centraldifference(xdata,ydata):
    derivative = np.zeros(np.shape(ydata))

    for i in range(len(derivative)):
        if i == 0:
            derivative[i] = (ydata[i+1] - ydata[i]) / (xdata[i+1] - xdata[i])

        elif i == len(derivative)-1:
            derivative[i] = (ydata[i] - ydata[i-1]) / (xdata[i] - xdata[i-1])

        else:
            derivative[i] = (ydata[i+1] - ydata[i-1]) / (xdata[i+1] - xdata[i-1])

    return derivative


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to image")
args = vars(ap.parse_args())

image = Image.open(args["image"])
print("[INFO] Opening image...")

# Get the color histogram of the image
histogram = image.histogram()

# Take only the Red counts
l1 = histogram[0:256]

# Take only the Blue counts
l2 = histogram[256:512]

# Take only the Green counts
l3 = histogram[512:768]

# Line plot of the histograms, with line colors corresponding to the RGB color
plt.figure(0)
plt.plot(l1[2:40], color = "r")
print("Max R value: {}".format(max(l1)))
plt.plot(l2[2:40], color = "g")
print("Max G value: {}".format(max(l2)))
plt.plot(l3[2:40], color = "b")
print("Max B value: {}".format(max(l3)))
plt.title("Original image histogram")

plt.figure(1)
derivative1R = centraldifference(range(0,256),l1)
derivative1G = centraldifference(range(0,256),l2)
derivative1B = centraldifference(range(0,256),l3)
plt.plot(derivative1R[2:40], color = "r")
plt.plot(derivative1G[2:40], color = "g")
plt.plot(derivative1B[2:40], color = "b")
plt.title("1st derivative of original histogram")
plt.show()

# split the red, green and blue bands from the image for individual constrast
# stretching
multiBands = image.split()

# Apply point operations that does contrast stretching on each color band
normalizedRedBand      = multiBands[0].point(normalizeRed)
normalizedGreenBand    = multiBands[1].point(normalizeGreen)
normalizedBlueBand     = multiBands[2].point(normalizeBlue)

# Create a new image from the contrast stretched red, green and blue brands
normalizedImage = Image.merge("RGB", (normalizedRedBand, normalizedGreenBand, normalizedBlueBand))

# Display the image before contrast stretching
image.show()

# Display the image after contrast stretching
normalizedImage.show()

# Get the color histogram of the image
histogram = normalizedImage.histogram()

# Take only the Red counts
l1 = histogram[0:256]

# Take only the Blue counts
l2 = histogram[256:512]

# Take only the Green counts
l3 = histogram[512:768]

# Line plot of the histograms, with line colors corresponding to the RGB color
print("[INFO] Plotting contrast stretched histogram...")
plt.figure(1)
plt.plot(range(256), l1, color = "r")
plt.plot(range(256), l2, color = "g")
plt.plot(range(256), l3, color = "b")
plt.title("Contrast stretched histogram")
plt.show()
