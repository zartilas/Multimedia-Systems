import cv2 as cv

vid = cv.VideoCapture('../videos/video_1.mp4')

previousFrame = None

while vid.isOpened():
    readable, currentFrame = vid.read()  # Apothikeute true i false sto success ean diavazete to video kai stin sinexeia apothikeuete to plaisio pou vriskete kathe fora.

    if not readable:  # Ean to video exei teleiosei tote me tin entoli break vgenoume apo to loop.
        break

    if previousFrame is None:  # Diatiroume to proigoumeno plaisio alla oxi stin prwti epanalipsi, epeidi to exoume arxikopioisi san None.
        previousFrame = currentFrame.copy()
        continue  # Metavenoume stin arxi tou loop kai sinexizoume

    errorFrame = cv.absdiff(currentFrame, previousFrame)  # Apoliti diafora metaksi tou parondos plaisiou kai tou proigoumenou.
    cv.imshow('Plaisia Sfalmatos', errorFrame)
    cv.waitKey(50)

    previousFrame = currentFrame.copy()

vid.release()
cv.destroyAllWindows()
