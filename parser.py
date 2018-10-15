import cv2,os,sys,pcl
import numpy as np
from glob import glob

#assert len(sys.argv) > 1

def parse_depth(w,h,data,convertname):
    np_gray16_array = np.frombuffer(data[:w*h*2],dtype='uint16')
    print type(np_gray16_array)
    cloud = pcl.PointCloud()
    scale = 16
    fx = 528.0
    cx = 325.0
    fy = 519.0
    cy = 253.0
    cloud_points = []
    for m in range(0,h):
        for n in range(0,w):
            d = np_gray16_array[m*w+n]
            if d ==0:
                pass
            else:
                #z = float(d)/scale
                #x = (n - cx) * z / fx
                #y = (m - cy) *z / fy
                x = m
                z = -float(d)/scale
                y = n
                cloud_points.append([x,y,z])
    np_cloud_points = np.array(cloud_points,dtype = np.float32)
    cloud.from_array(np_cloud_points)
    pcl.save(cloud,'cloud.pcd',format = 'pcd')

os.system('rm transfer/*')

for path in glob(os.path.join('resource','*.raw')):
    with open(path,'rb') as file:
        convertname = file.name.replace('resource','transfer').replace('raw','png')
        #w = sys.argv[1].split('x')[0]
        #h = sys.argv[1].split('x')[1]
        data = file.read()
        rows = 480
        cols = 640
        parse_depth(cols,rows,data,convertname)
        os.system('pcl_viewer cloud.pcd -fc 100,100,100')


