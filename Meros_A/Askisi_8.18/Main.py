import cv2 as cv

from Utilities import getMacroblocks, getFrame

# Fortwnoume to video gia na epeksergastoume ta macroblocks.
vid = cv.VideoCapture('../videos/video_2.mp4')

# Arxikopioisi
previousExists = False
previousMs16 = None
previousMs8 = None
previousMs4 = None

while vid.isOpened():
    readable, currentFrame = vid.read()

    # Break an to video teleiwse.
    if not readable:
        break

    #Eksagoume macroblocks me megethos 16, 8 kai 4.
    MacroblockSize16 = getMacroblocks(currentFrame, window=16)
    MacroblockSize8 = getMacroblocks(currentFrame, window=8)
    MacroblockSize4 = getMacroblocks(currentFrame, window=4)

    #Kratame ta prohgoumena macroblocks ektos ta macroblocks apo thn prwth epanalhpsh.
    if not previousExists:
        previousExists = True
        previousMs16 = MacroblockSize16
        previousMs8 = MacroblockSize8
        previousMs4 = MacroblockSize4
        continue

    # Antikathistoume ta macroblcoks gia na kripsoume tin kinisi.
    # Testaroume tyxaious arithmous gia na doume
    for i in range(1, 20):
        MacroblockSize16[i] = previousMs16[i]

    for j in range(17, 40):
        MacroblockSize8[j] = previousMs8[j]

    for m in range(37, 85):
        MacroblockSize4[m] = previousMs4[m]

    MacroblockSizeFrame16 = getFrame(MacroblockSize16)
    MacroblockSizeFrame8 = getFrame(MacroblockSize8)
    MacroblockSizeFrame4 = getFrame(MacroblockSize4)

    # Emfanizoume kai ta tesera frames kai tiw allages tous.
    cv.imshow('Arxiko Video', currentFrame)
    cv.imshow('Diagrafi Antikeimenou - Megethos 16', MacroblockSizeFrame16)
    cv.imshow('Diagrafi Antikeimenou - Megethos 8', MacroblockSizeFrame8)
    cv.imshow('Diagrafi Antikeimenou - Megethos 4', MacroblockSizeFrame4)

    # Kratame ta prohgoumena macroblocks.
    previousMs16 = MacroblockSize16
    previousMs8 = MacroblockSize8
    previousMs4 = MacroblockSize4
    cv.waitKey(35)

vid.release()
cv.destroyAllWindows()
