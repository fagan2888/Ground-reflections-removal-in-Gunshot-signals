
import math, copy
import numpy as np
import matplotlib.pyplot as plt
import librosa

from MyPythonCodes.tools import detect_peaks

# factor of the 0-delay auto-correlation (mean square) for secondary correlation
# peak to be considered a genuine reflection (instead of noise)
MinPeakHeight = 0.1
# number of repetitive corrections to be applied to reduce reflection artifact
MaxCorrIter = 4

x, sr = librosa.load('/home/administrator/Downloads/ML_work/Gunshot_detection_CNN/Rifle_carbine.mp3') # Path of mp3 file

class EventReflection(object):
    """ obj = EventReflection(x,options)
        
        Starts a class for detecting reflection artifacts in a signal, and
        correct for the same
        
        INPUTS (to constructor):
            x - data timeseries in which there is a single 'main' event, and
                possibly secondary reflection events, the largest of the latter
                is to be detected and corrected

        ATTRIBUTES:
            x         - data timeseries supplied to constructor
            iDelay    - number of samples of delay between main event and its
                        main secondary reflection
            ratioCorr - ratio of amplitude of auto-correlation peak at above
                        delay to that at 0 delay
            y         - corrected timeseries
        
        METHODS:
            detect  - detect reflection
            correct - correct for same
    """    

    def __init__(self,x):
        self.x = x
        self.iDelay = -1
        self.ratioCorr = 0.
        self.y = None

    def detect(self,options=None):
        """ detect main reflection event in a signal """
        plot = options is not None and 'plot' in options and options['plot']
        corrArray = np.correlate(self.x,self.x,'full') #auto-correlate 'x'
        corrArray = corrArray[(len(self.x)-1):] #keep zero & +ve delays only
        corrArray = corrArray/corrArray[0] #normalize by 0-delay value
        corrArray.clip(min=0.) #clip negative values
        iPks = detect_peaks(corrArray,mph=MinPeakHeight,show=plot) #detect peaks
        if len(iPks) < 1:
            return False
        jPks = np.argmax(corrArray[iPks])#index of max peak; 0-delay peak absent
        self.iDelay = iPks[jPks] #note no. of samples to peak from 0-delay
        self.ratioCorr = corrArray[iPks[jPks]] #ratio of correlations for this
        return True
    
    def correct(self,options=None):
        """ correct for main reflection (already detected) """
        plot = options is not None and 'plot' in options and options['plot']
        if self.ratioCorr <= 0. or self.ratioCorr > 0.5:
            # nothing to correct, since ratio of correlations is out of range
            self.y = self.x
            return
        # amplitude ratio of main and reflection events' peaks, obtained with
        # assumptions stated at the outset (see Braasch's paper)
        ampRatio = (1 - math.sqrt(1-4*self.ratioCorr**2))/(2.*self.ratioCorr)
        self.y = copy.deepcopy(self.x) #start by copying original signal 
        if plot:
            fig = plt.figure()
            axLeft = fig.add_subplot(1,2,1)
            axRight = fig.add_subplot(1,2,2)
            axLeft.plot(self.x)
            plt.hold(True)
            axRight.plot(self.x)
            plt.hold(True)
        for iter in range(1,MaxCorrIter+1):
            if iter*self.iDelay >= len(self.x): #no more shifts left in data
                break
            xsub = np.zeros_like(self.x) #initialize shifted & scaled data
            # shift 'x' by 'iter' times no. of delayed samples, and scale it by
            # the negative of the amplitude ratio to the power of 'iter'
            xsub[iter*self.iDelay:] = (-ampRatio)**iter \
                *self.x[:-(iter*self.iDelay)]
            self.y = self.y + xsub #add to running 'y' (modified 'x')
            if plot:
                axLeft.plot(xsub)
                axRight.plot(self.y,'--')
        if plot:
            axRight.plot(self.y,'-',linewidth=2)
            plt.show
            
refl = EventReflection(x)
refl.detect()
refl.correct({'plot':True})

#endclass EventReflection
