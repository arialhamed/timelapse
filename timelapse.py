# Dependancies
# cv2 must be OpenCV 3

# Last updated
# - TIME: 2020/1/2/18:11
# - PLACE: SINGAPORE

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
    print('\nExiting software...')
    sys.exit()

name = ''
outname = ''
flag_clearframes = 1
create_timelapse = 1
val_frame = 25
cwd = os.getcwd()
candidates = [x for x in os.listdir() if x[len(x)-4:] in ('.mp4','.avi')]

check = 1

print()
print('Current working Directory')
print(cwd)
    
print()
print('Current items in Directory')

for i in range(len(candidates)):
    print('{}: {}'.format(str(i+1).zfill(3),candidates[i]))
        
while check:
    print()
    print('Enter number index.')
    try:
        name = candidates[int(input('>>> '))-1]
        print()
        print('Name of file: '+name)
        out_name = input('Enter name of output video (default ext: mp4): ')
        flag_clearframes = 1 if input('Clear frames after processing? (Y/N): ') in 'Yy' else 0
        val_frame = int(input('Enter how far each frame should be seperated (all frames: 1; recommended: 25): '))
        create_timelapse = 1 if input('Create timelapse video? (Y/N if only frames are needed): ') in 'Yy' else 0
        check = 0
    except:
        print('Something went wrong. Start again.')
        sys.exit()


#-----------------------------------------------------------------------------#
### FRAME EXTRACTION ###


cap = cv2.VideoCapture(name)

frame_name = 'timelapse_'+out_name
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#flag = val_frame
in_frames = total_frames//val_frame

message1 = ('',
            'Total frames in input video: '+str(total_frames),
            'Approximate total frames in output video: '+str(in_frames),
            '',
            'DO NOT PRESS SPACE ELSE AN ERROR MAY OCCUR',
            '',
            'Creating necessary frames in current working directory',
            '## {}'.format('-'*50)
            )
[print(x) for x in message1]


frame_no = 0
prog_bar = in_frames // 50

print('## ', end='')
while(cap.isOpened()):
    frame_no += 1
    ret, img = cap.read()
    if ret==True:
        if frame_no % val_frame != 0: continue
        else:
            cv2.imwrite('./'+frame_name+'_'+str(frame_no//val_frame).zfill(10)+'.png', img)
            if frame_no % prog_bar == 0:
                print('-', end='')
        if cv2.waitKey(1) & 0xFF == ord(' '):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()


#-----------------------------------------------------------------------------#
### CREATING VIDEO OUTPUT ###

if create_timelapse:
    message2 = ('\n',
                'Collecting frames...',
                '## {}'.format('-'*50)
                )
    [print(x) for x in message2]
    print('## ', end='')


    img_array = []
    frame_no = 0

    for filename in glob.glob(cwd+'/'+frame_name+'_*.png'):
        try:
            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)
            frame_no += 1
            if frame_no % prog_bar == 0:
                print('-', end='')
        except:
            pass


    message3 = ('\n',
                'Writing to output video...',
                '## {}'.format('-'*50)
                )
    [print(x) for x in message3]
    print('## ', end='')


    out = cv2.VideoWriter(out_name+'.mp4',cv2.VideoWriter_fourcc(*'XVID'), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
        if i % prog_bar == 0:
            print('-', end='')
    out.release()

#-----------------------------------------------------------------------------#
### CLEARING PRODUCED FRAMES FROM DIRECTORY ###

frame_no = 0

message4 = ('\n',
            'Clearing frames...',
            '## {}'.format('-'*50)
            )
            
if flag_clearframes:
    try:
    ##    print('Clear frames?')
    ##    isit = input('>>> ')
    ##    if not(isit in 'yY'):
    ##        break
        
        [print(x) for x in message4]
        print('## ', end='')
        
        #candidates = 
        
        for filename in glob.glob(cwd+'/'+frame_name+'_*.png'):
            os.remove(filename)
            frame_no += 1
            if frame_no % prog_bar == 0:
                print('-', end='')
            
        
    except:
        print('Something failed. Exiting software')
        sys.exit()

print('\n\n')

if out_name+'.mp4' in os.listdir() and create_timelapse:
    print('Checking if output video exists...')
    print(str(out_name+'.mp4')+' exists. Creation successful!')
    print()

print('Restart Shell (Ctrl + F6) to clear cache' if 'idlelib.run' in sys.modules else '')

