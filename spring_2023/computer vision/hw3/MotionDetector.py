import numpy as np
import matplotlib.pyplot as plt
import skvideo.io
from skimage.color import rgb2gray, gray2rgb
from skimage.measure import label, regionprops
from skimage.morphology import dilation
import cv2
from KalhmanFilter import KalhmanFilter

np.float = np.float64
np.int = np.int_

class MotionDetector:
    def __init__(self, frames, frame_hysteresis=10, motion_threshold=0.05, distance_threshold=3, 
                skip_frames=3, max_objects=5):
        self.frames = frames
        self.frame_hysteresis = frame_hysteresis # active or inactive object
        self.motion_threshold = motion_threshold  # something that moving too slow
        self.distance_threshold = distance_threshold # determine if an object candidate belongs to an object currently being tracked.
        self.skip_frames = skip_frames
        self.max_objects = max_objects
        self.tracking_objects = []
        self.current_frame_idx = 0
        self.candidates = self.detect_objects(3)
        
    
    '''
    the object could be active or inactive
    think about, an object can stop for a while, then start moving back
    that is the reason why we need to consider an object is active or inactive
    noticed that being actived doesn't mean being tracked (very important)
    '''
    def update_tracking(self, frame_idx):
        if frame_idx - self.current_frame_idx < self.skip_frames:
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
                diff = np.linalg.norm(predicted_X, new_obj.X)
                if diff < min_diff:
                    matched_obj = new_obj
            if matched_obj:
                obj.update(predicted_X[0:2])
                obj.last_updated_frame = frame_idx
                new_objects.remove(matched_obj)
            # remove long-enough UN-UPDATED tracked object out of tracking list
            elif frame_idx - obj.last_update_frame > self.frame_hysteresis:
                self.tracking_objects.remove(obj)
        
        # do the same thing with list of candidates
        for obj in self.candidates:
            predicted_X = obj.predict()
            min_diff = self.distance_threshold
            matched_obj = None
            for new_obj in new_objects:
                diff = np.linalg.norm(predicted_X, new_obj.X)
                if diff < min_diff:
                    matched_obj = new_obj
            if matched_obj:
                obj.update(predicted_X[0:2])
                obj.last_updated_frame = frame_idx
                # if the object is being active long enough and the tracking list is not full,
                # then add it to tracking list and remove out of candidates list
                if obj.last_updated_frame - obj.start_frame > self.frame_hysteresis \
                and len(self.tracking_objects) < self.max_objects:
                    self.tracking_objects.add(obj)
                    self.candidates.remove(obj)
                new_objects.remove(matched_obj)
            # remove long-enough UN-UPDATED tracked object out of candidates list
            elif frame_idx - obj.last_update_frame > self.frame_hysteresis:
                self.candidates.remove(obj)

        # the rest of the new obj should be added to be new candidates
        self.candidates.add(new_objects)
        
        self.last_frame_idx = frame_idx


    def detect_objects(self, frame_idx):
        if frame_idx < 2:
            frame_idx = 2
        detected_objects = []
        frame1 = rgb2gray(self.frames[frame_idx])
        frame2 = rgb2gray(self.frames[frame_idx-1])
        frame3 = rgb2gray(self.frames[frame_idx-2])
        diff1 = np.abs(frame2-frame1)
        diff2 = np.abs(frame3-frame2)

        motion_frame = np.minimum(diff1, diff2)
        thresh_frame = motion_frame > self.motion_threshold
        dilated_frame = dilation(thresh_frame, np.ones((9, 9)))
        label_frame = label(dilated_frame)
        regions = regionprops(label_frame)

        for region in regions:
            X = np.array((region.centroid, [0.1,0.1])).reshape(4,1)
            object = KalhmanFilter(X, dt=frame_idx - self.current_frame_idx,
                                   start_frame= frame_idx, last_updated_frame=frame_idx)
            detected_objects.add(object)
        
        self.current_frame_idx = frame_idx
        return detected_objects

        
        