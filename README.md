**Task 1 – Acquisition  
Process the IF data using a GNSS SDR and generate the initial acquisition results.**
Below the acquisition results from the data:

Urban Environment - Visible Satellites:

PRN 1: Code Phase = 22799938, Doppler Shift = -4286.22 Hz

PRN 2: Code Phase = 2301966, Doppler Shift = -2661.62 Hz

PRN 5: Code Phase = 20143767, Doppler Shift = -4286.22 Hz

PRN 7: Code Phase = 24079234, Doppler Shift = -1208.19 Hz

PRN 9: Code Phase = 25078741, Doppler Shift = -2661.62 Hz

PRN 10: Code Phase = 18797973, Doppler Shift = -4286.22 Hz

PRN 11: Code Phase = 15066074, Doppler Shift = -4286.22 Hz

PRN 12: Code Phase = 22034282, Doppler Shift = -2661.62 Hz

PRN 13: Code Phase = 18460791, Doppler Shift = -2661.62 Hz

PRN 15: Code Phase = 10556665, Doppler Shift = -2661.62 Hz

PRN 17: Code Phase = 612710, Doppler Shift = -4286.22 Hz

PRN 20: Code Phase = 7748971, Doppler Shift = -4286.22 Hz

PRN 21: Code Phase = 12931563, Doppler Shift = -2661.62 Hz

PRN 24: Code Phase = 11203562, Doppler Shift = -2661.62 Hz

PRN 26: Code Phase = 16085403, Doppler Shift = -2661.62 Hz

PRN 29: Code Phase = 8278011, Doppler Shift = -4286.22 Hz

PRN 30: Code Phase = 15435516, Doppler Shift = -4286.22 Hz

PRN 32: Code Phase = 22562705, Doppler Shift = -2661.62 Hz

**Task 2 – Tracking
Adapt the tracking loop (DLL) to generate correlation plots and analyze the tracking performance. Discuss the impact of urban interference on the correlation peaks. (Multiple correlators must be implemented for plotting the correlation function.)**

Correlation plots are as follows:



**Task 3 – Navigation Data Decoding
Decode the navigation message and extract key parameters, such as ephemeris data, for at least one satellite.**


**Task 4 – Position and Velocity Estimation
Using pseudorange measurements from tracking, implement the Weighted Least Squares (WLS) algorithm to compute the user's position and velocity.
Plot the user position and velocity.
Compare the results with the ground truth.
Discuss the impact of multipath effects on the WLS solution.**


**Task 5 – Kalman Filter-Based Positioning
Develop an Extended Kalman Filter (EKF) using pseudorange and Doppler measurements to estimate user position and velocity.**

