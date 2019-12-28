# Dependancies
# cv2 must be OpenCV 3
import cv2
import numpy as np
import glob
import os
import sys

### INPUT VALIDATION ###

message0 = ('Timelapse Processor V1.0',
            '- Created in Python 3.5.2',
            '- Only compatible with OpenCV 3',
            '- Currently only runs under Python shell and in .py file extension',
            '- Last updated on 28 DEC 2019',
            'Continue? (Y/N)')

[print(x) for x in message0]

enter0 = input('>>> ')
if not(enter0 in 'Yy'):
    print('Exiting software...')
    sys.exit()

name = ''
cwd = os.getcwd()
check = 1

while check:
    print()
    print('Current working Directory')
    print(cwd)
        
    print()
    print('Current items in Directory')

    for i in range(len(os.listdir())):
        print('{}: {}'.format(str(i+1).zfill(3),os.listdir()[i]))
        
    print()
    print('Enter number index.')
    try:
        name = os.listdir()[int(input('>>> '))-1]
        out_name = input('Enter name of output video (default ext: mp4): ')
        # next task: enable customization of speed (waitKey)
        check = 0
    except:
        print('Invalid input. Exiting software...')
        sys.exit()


#-----------------------------------------------------------------------------#
### FRAME EXTRACTION ###

message1 = ('',
            'Creating timelapse_frames in current working directory',
            'Press Space to stop process and start next process',
            '')
[print(x) for x in message1]

cap = cv2.VideoCapture(name)

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('Total frames in input video: '+str(total_frames))
flag = 25
print('Approximate total frames in output video: '+str(total_frames//flag))
frame_no = 0

print()
print('# {} #'.format('-'*50))
while(cap.isOpened()):
    frame_no += 1
    ret, img = cap.read()
    if ret==True:
        if frame_no % flag != 0: continue
        else:
            cv2.imwrite('./timelapse_frame_'+str(frame_no).zfill(10)+'.png', img)
        
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()

#-----------------------------------------------------------------------------#
### CREATING VIDEO OUTPUT ###

message2 = ('',
            'Creating output video...',
            '')

[print(x) for x in message2]
img_array = []
for filename in glob.glob(cwd+'/timelapse_frame_*.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)

out = cv2.VideoWriter(out_name+'.mp4',cv2.VideoWriter_fourcc(*'XVID'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()

#-----------------------------------------------------------------------------#
### CLEARING PRODUCED FRAMES FROM DIRECTORY ###

try:
    print()
    print('Clearing frames...')
    #candidates = 
    
    for filename in glob.glob(cwd+'/timelapse_frame_*.png'):
        os.remove(filename)
    
except:
    print('Something failed. Exiting software')
    sys.exit()

print()
print('Checking if output video exists...')

if name+'.mp4' in os.listdir():
    print(str(name+'.mp4')+' exists. Creation successful!')




