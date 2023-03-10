import numpy as np

'''
this implementation refer to these 2 websites
https://arxiv.org/pdf/1204.0375.pdf#:~:text=A%20Kalman%20Filtering%20is%20carried,in%20wireless%20networks%20is%20given.
https://thekalmanfilter.com/kalman-filter-explained-simply/

Assume we only track position and velocity
'''

class KalhmanFilter:
    def __init__(self, X, dt=1, start_frame=0, last_updated_frame=0, region=None):
        '''
        X : The mean state estimate of the previous step (k−1).
        P : The state covariance of previous step (k−1).
        A : The transition n n × matrix.
        Q : The process noise covariance matrix.
        B : The input effect matrix.
        U : The control input. 
        H : State-to-measurement matrix
        R : Measurement covariance matrix

        There are some matrix that we don't need in this implementation, it's here for study purpose
        '''
        self.X = X

        self.dt = dt
        self.P = np.diag((5, 5, 5, 5))
        self.A = np.array([[1, 0, dt , 0], 
                           [0, 1, 0, dt], 
                           [0, 0, 1, 0], 
                           [0, 0, 0,1]])
        self.Q = np.eye(4)
        self.B = np.eye(4)
        self.U = np.zeros((4,1))
        self.H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]]) 

        self.start_frame = last_updated_frame
        self.last_updated_frame = last_updated_frame
        self.region = region

    def predict(self):
        # predicted state
        self.X = np.dot(self.A, self.X) + np.dot(self.B, self.U)
        #predicted covariance
        self.P = np.dot(self.A, np.dot(self.P, self.A.T)) + self.Q  
        return self.X

    def update(self, Y):
        # np.eye return matrix with 1 in diagonal and 0 else where
        # probably want to set R to some sort of motion_threshold = 0.05
        # R=np.diag([self.motion_threshold, self.motion_threshold])) 
        # right now R has 1 in diagonal
        R = np.eye(1) 
        IM = np.dot(self.H, self.X)
        IS = R + np.dot(self.H, np.dot(self.P, self.H.T))
        #IS = R + np.dot(self.H, np.dot(self.P, self.H.T)) - np.dot(K, np.dot(self.H, self.P))
        K = np.dot(self.P, np.dot(self.H.T, np.linalg.inv(IS)))

        #update state and state covariance
        self.X = self.X + np.dot(K, (Y-IM))
        self.P = self.P - np.dot(K, np.dot(IS, K.T))
        # LH = gauss_pdf(Y, IM, IS) this is the likelyhood, we probably don't need this
