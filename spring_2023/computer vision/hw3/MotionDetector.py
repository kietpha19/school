import numpy as np
import matplotlib.pyplot as plt
import skvideo.io
from skimage.color import rgb2gray, gray2rgb
from skimage.measure import label, regionprops
from skimage.morphology import dilation
import cv2
import skimage.io as io
from KalhmanFilter import KalhmanFilter

np.float = np.float64
np.int = np.int_

class MotionDetector:
    def __init__(self, frames, frame_hysteresis=5, motion_threshold=0.05, distance_threshold=50,
                skip_frames=3, max_objects=10):
        self.frames = frames
        self.frame_hysteresis = frame_hysteresis # active or inactive object
        self.motion_threshold = motion_threshold  # something that moving too slow
        self.distance_threshold = distance_threshold # determine if an object candidate belongs to an object currently being tracked.
        self.skip_frames = skip_frames
        self.max_objects = max_objects
        self.tracking_objects = []
        self.last_frame_idx = 0
        self.candidates = self.detect_objects(2)
        self.draw_candidates(2)
        
    
    '''
    the object could be active or inactive
    think about, an object can stop for a while, then start moving back
    that is the reason why we need to consider an object is active or inactive
    noticed that being actived doesn't mean being tracked (very important)
    '''
    def update_tracking(self, frame_idx):
        if frame_idx - self.last_frame_idx < self.skip_frames:
            self.draw_tracking_objects(frame_idx)
            self.draw_candidates(frame_idx)
            return
        
        # detect new object (observation/measurement), to compare with the prediction
        new_objects = self.detect_objects(frame_idx)

        # loop through the current tracked object, compare its predicted X with new dectected obj
        # if the L2 norm is closed enough, which mean that's a match
        # we should use that measurement to update our object and remove that out of the new_objects set
        # also, we need to update the last updated frame
        # otherwive, check if the object inactive for too long, if yes, then remove obj out of tracking list
        for obj in self.tracking_objects:
            predicted_X = obj.predict()
            min_diff = self.distance_threshold
            matched_obj = None
            for new_obj in new_objects:
                diff = np.linalg.norm(predicted_X - new_obj.X)
                if diff < min_diff:
                    matched_obj = new_obj
            if matched_obj:
                obj.update(matched_obj.X[0:2])
                obj.last_updated_frame = frame_idx
                obj.region = matched_obj.region
                new_objects.remove(matched_obj)
            # remove long-enough UN-UPDATED tracked object out of tracking list
            elif frame_idx - obj.last_updated_frame > 15:
                self.tracking_objects.remove(obj)
        
        # do the same thing with list of candidates
        for obj in self.candidates:
            predicted_X = obj.predict()
            # print(predicted_X)
            min_diff = self.distance_threshold
            matched_obj = None
            for new_obj in new_objects:
                diff = np.linalg.norm(predicted_X - new_obj.X)
                if diff < min_diff:
                    matched_obj = new_obj
            if matched_obj:
                obj.update(matched_obj.X[0:2])
                obj.last_updated_frame = frame_idx
                obj.region = matched_obj.region
                # if the object is being active long enough and the tracking list is not full,
                # then add it to tracking list and remove out of candidates list
                if obj.last_updated_frame - obj.start_frame > self.frame_hysteresis \
                and len(self.tracking_objects) < self.max_objects:
                    self.tracking_objects.append(obj)
                    self.candidates.remove(obj)
                new_objects.remove(matched_obj)
            # remove long-enough UN-UPDATED tracked object out of candidates list
            elif frame_idx - obj.last_updated_frame > 15:
                self.candidates.remove(obj)

        # the rest of the new obj should be added to be new candidates
        for new_obj in new_objects:
            self.candidates.append(new_obj)
        
        self.last_frame_idx = frame_idx
        self.draw_tracking_objects(frame_idx)
        self.draw_candidates(frame_idx)


    def detect_objects(self, frame_idx):
        if frame_idx < 2:
            frame_idx = 2
        
        frame1 = rgb2gray(self.frames[frame_idx-2])
        frame2 = rgb2gray(self.frames[frame_idx-1])
        frame3 = rgb2gray(self.frames[frame_idx])
        diff1 = np.abs(frame3-frame2)
        diff2 = np.abs(frame2-frame1)

        motion_frame = np.minimum(diff1, diff2)
        thresh_frame = motion_frame > self.motion_threshold
        dilated_frame = dilation(thresh_frame, np.ones((9, 9)))
        label_frame = label(dilated_frame)
        regions = regionprops(label_frame)
        detected_objects = []
        for region in regions:
            # skip if the region is too small
            if region.area < 100:
                continue
            X = np.array((region.centroid, [0.1,0.1])).reshape(4,1)
            # print(X)
            object = KalhmanFilter(X, dt=frame_idx - self.last_frame_idx,
                                   start_frame= frame_idx, last_updated_frame=frame_idx, region=region)
            detected_objects.append(object)
        
        self.last_frame_idx = frame_idx
        return detected_objects
    
    def draw_tracking_objects(self, frame_idx):
        color = (0,0,255) #blue
        thick = 2
        for obj in self.tracking_objects:
            bbox = obj.region.bbox
            left,top,right,bottom = bbox
            cv2.rectangle(self.frames[frame_idx], (top, left), (bottom, right), color, thick)
    
    def draw_candidates(self, frame_idx):
        color = (0,255,0) #green
        thick = 1
        for obj in self.candidates:
            bbox = obj.region.bbox
            left,top,right,bottom = bbox
            cv2.rectangle(self.frames[frame_idx], (top, left), (bottom, right), color, thick)

    # testing function
    def test(self):
        idx = 2
        threshold = 0.05

        ppframe = rgb2gray(self.frames[idx-2])
        pframe = rgb2gray(self.frames[idx-1])
        cframe = rgb2gray(self.frames[idx])
        diff1 = np.abs(cframe - pframe)
        diff2 = np.abs(pframe - ppframe)

        motion_frame = np.minimum(diff1, diff2)
        thresh_frame = motion_frame > threshold
        dilated_frame = dilation(thresh_frame, np.ones((9, 9)))
        label_frame = label(dilated_frame)
        regions = regionprops(label_frame)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.frames[2], cmap='gray')
        ax.set_axis_off()
        ax.margins(0, 0)
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())

        for r in regions:
            minr, minc, maxr, maxc = r.bbox
            bx = (minc, maxc, maxc, minc, minc)
            by = (minr, minr, maxr, maxr, minr)
            ax.plot(bx, by, '-b', linewidth=2)
        
        plt.show()