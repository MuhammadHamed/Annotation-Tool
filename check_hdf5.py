import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# change the file path and the color flag if desired
hdf5_folder = "/home/mohamed/Desktop/Opto/AnnotationTool/Pendulum/masks/hdf5"
filename = hdf5_folder + "/pendulum_test2_run01_camera02_fps_1.hdf5"
color = False

f=h5py.File(filename,"r")

print "-----------------------------------"
print "-Labels (Masks):"
label = f['label']
print "\t-shape:", label.shape
print "\t-max value: ",np.max(label)
print "\t-min value: ",np.min(label)
print "\t-type:", label.dtype
print "-----------------------------------"
print "-Data (Frames):"
data = f['data']
print "\t-shape:", data.shape
print "\t-max value: ", np.max(data)
print "\t-min value: ",np.min(data)
print "\t-type:", data.dtype
print "-----------------------------------"



examples = data.shape[0]
# load the first N examples of the training set
for exp in range(0,examples):
  print "-----------------------------------------------"
  print "Example", exp+1
  if color:
    frame = np.zeros((data.shape[2],data.shape[3],data.shape[1]))
    mask = np.zeros((data.shape[2],data.shape[3],data.shape[1]))
    frame[:,:,0] = data[exp,0,:,:]
    frame[:,:,1] = data[exp,1,:,:]
    frame[:,:,2] = data[exp,2,:,:]
  else:
    frame = data[exp,0,:,:]
  mask = label[exp,0,:,:]

  print "-Data size:", frame.shape
  print "-Label size:", mask.shape

  if (data.shape[2]==label.shape[2]) and (data.shape[3]==label.shape[3]):
    plt.figure
    if color:
      plt.subplot(121)
      plt.imshow(frame)
    else:
      plt.subplot(121)
      plt.imshow(frame,cmap='gray')

    plt.subplot(122)
    plt.imshow(mask,cmap='gray')
    plt.show

    if np.max(mask) != np.min(mask):
      print "-Object visible"
      plt.pause(0.5)
    else:
      print "-Object not visible"

  else:
    #mask.resize(frame.shape);
    #print np.max(mask)
    #print np.min(mask)
    mask[np.where(mask>0)] = 255  # change max value to 1 !

    mask_cp = np.zeros(frame.shape)
    for y in range(10):
      for x in range(10):
        for cntx in range(10):
          for cnty in range(10):
            mask_cp[x*10-cntx,y*10-cnty]=mask[x,y]


    xmax = 0
    xmin = 1000
    ymax = 0
    ymin = 1000
    for x in range(mask.shape[1]):
      for y in range(mask.shape[0]):
        if mask[y,x] > 0:
          if x<xmin:
            xmin=x
          if x>xmax:
            xmax=x
          if y<ymin:
            ymin=y
          if y>ymax:
            ymax=y

    #print xmin,xmax,ymin,ymax


    vis = np.concatenate((mask_cp,frame),axis=1)
    #plt.figure(1)
    fig1 = plt.figure(1)
    fig1.clf()
    #ax1 = fig1.add_subplot(111,aspect='equal')
    ax1 = plt.gca()
    ax1.imshow(vis,cmap='gray')
    #ax1.imshow(vis)
    # draw rectangle on top
    xpos = 0.5 +  xmin/10.*0.5
    ypos =        ymin/10.*0.5

    #print xpos
    #print ypos

    #ax1.add_patch(patches.Rectangle((xpos,ypos),100/640,50/480,linewidth=3,edgecolor='r',facecolor="red"))

    ax1.add_patch(patches.Rectangle((320+(xmin)*32,240-(9.5-ymin)*32),50,25,linewidth=3,edgecolor='r',facecolor="none"))
    plt.show

    if np.max(mask) != np.min(mask):
      plt.pause(0.5)

f.close()
