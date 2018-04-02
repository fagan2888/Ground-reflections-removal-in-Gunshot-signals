# Ground-reflections-removal-in-Gunshot-signals

Given the array of acoustic signals, Function is build in both **Python** and **MATLAB** to remove the ground reflections.

**Basic concept**

An autocorrelation-based method is introduced to estimate the parameters of lag delay T and the ratio r = Direct amplitude/Reflected amplitude.

For given values of the delay between lead and lag, T and r, the filter ( function of r and T) can eliminate the lag from the total signal.This deconvolution filter converges quickly and only a few filter coefficients are needed to remove the reflected signal effectively from the total signal.

**Purpose for ground reflection**

Signals received at multiple sensors and estimate the delays between sensors using cross correlation. Ground reflectionless signal using cross correlation technique evalute much better values of delay and it help us to localise the gunshot more precisely. 

**Note** - We assume that Events is detected (using event detection repository) and save as pqfile.txt





