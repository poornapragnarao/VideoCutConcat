import cv2
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
out_file = file_path.split('.')[0] + '_out.' + file_path.split('.')[1]
cap = cv2.VideoCapture(file_path)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
print('Frame width = ',frame_width)
print('Frame height = ',frame_height)

out = cv2.VideoWriter(out_file,cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width,frame_height))

pause = False
start_record = False
start_frames = []
end_frames = []

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,frame_height - 100)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

cv2.namedWindow('frame',cv2.WINDOW_AUTOSIZE | cv2.WINDOW_KEEPRATIO | cv2.WINDOW_GUI_EXPANDED)
frame = []
while(cap.isOpened()):
    if not pause:
        curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()

    cv2.imshow('frame',cv2.resize(frame, (int(frame_width/2), int(frame_height/2))))
    
    curr_key = cv2.waitKey(1) & 0xFF
    if curr_key != 255:
        print(curr_key)
    if curr_key == ord('q') or curr_key == ord('p'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        break
    if curr_key == 32:
        pause = not pause
        cv2.putText(frame,'| |', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
    if curr_key == ord(','):
        cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_num - 1)
        curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()
    if curr_key == ord('.'):
        curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()
    if curr_key == ord('m'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_num - 5)
        curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()
    if curr_key == ord('/'):
        cap.set(cv2.CAP_PROP_POS_FRAMES, curr_frame_num + 5)
        curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()
    if curr_key == ord('s'):
        start_frames.append(curr_frame_num)
    if curr_key == ord('e'):
        end_frames.append(curr_frame_num)


cv2.putText(frame,'Processing...', 
    bottomLeftCornerOfText, 
    font, 
    fontScale*3,
    fontColor,
    lineType)
cv2.imshow('frame',cv2.resize(frame, (int(frame_width/2), int(frame_height/2))))

while(cap.isOpened()):
    for i in range(len(start_frames)):
        start_frame = start_frames[i]
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        end_frame = end_frames[i]
        curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        while curr_frame < end_frame:
            curr_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            ret, frame = cap.read()
            out.write(frame)
    break

cap.release()
out.release()
cv2.destroyAllWindows()