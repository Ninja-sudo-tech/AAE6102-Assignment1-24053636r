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

<img width="452" alt="Task 2 Correlation Plots 1" src="https://github.com/user-attachments/assets/f01cabe3-203c-447d-a6b1-f24ed4af9b71" />
<img width="452" alt="Task 2 Correlation Plots 2" src="https://github.com/user-attachments/assets/04532a42-b96c-4114-8ec3-b219851b4625" />

Discussion on the correlation peaks:

1) Characteristics of the Correlation Function in Open-Sky Conditions: the difference between peak and non-peak values is small but uniform, indicating the line-of-sight signal dominates, with minimal multipath interference. The received signal is stable, resulting in a well-defined correlation peak. The non-peak areas exhibit low and consistent power levels, suggesting a low-interference environment. In summary, the DDL can reliably lock onto the main peak, ensuring high tracking accuracy. 

2) Characteristics of the Correlation Function in Urban Conditions:	the difference between peak and non-peak values is large and non-uniform, likely due to:
Firstly, severe multipath effects, such as reflected signals interfere with the direct signal, causing peak broadening, distortion, or even multiple false peaks. Secondly, signal fading: Due to reflections and diffractions from buildings, signals arrive with varying power levels, making the correlation peak fluctuate significantly. Thirdly, dynamic obstructions such as moving objects (vehicles, pedestrians) cause time-varying signal attenuation, leading to irregular correlation patterns. Lastly, electromagnetic interference: Increases the noise floor, making the non-peak regions more unstable and exaggerating the difference between peak and non-peak values.

**Task 3 – Navigation Data Decoding
Decode the navigation message and extract key parameters, such as ephemeris data, for at least one satellite.**

The ephemeris data are as follows(for the original file, please refer to ):

<img width="552" alt="1" src="https://github.com/user-attachments/assets/c8e60017-1ddf-42e3-ba8b-86710f625949" />

<img width="548" alt="2" src="https://github.com/user-attachments/assets/b5243409-42a5-44c5-a446-736c92bfd6f6" />

<img width="464" alt="3" src="https://github.com/user-attachments/assets/c10c0026-22eb-4c1c-96a8-abb43f9c5384" />

**Task 4 – Position and Velocity Estimation
Using pseudorange measurements from tracking, implement the Weighted Least Squares (WLS) algorithm to compute the user's position and velocity.
Plot the user position and velocity.
Compare the results with the ground truth.
Discuss the impact of multipath effects on the WLS solution.**

In open-sky conditions, the positioning results from different satellites are very close to each other and also closely match the ground truth. This suggests that the signals are largely free from interference, and the Weighted Least Squares solution provides accurate positioning with minimal error.

However, in urban conditions, the positioning results from different satellites show significant discrepancies for the same location. This deviation from the ground truth indicates that urban interference, particularly multipath effects, is impacting the accuracy of the WLS solution.

**For the multipath effects on the WLS solution:**

Satellite-Specific Positioning Variability: In urban environments, multipath causes some satellite signals to be delayed or distorted, leading to inconsistent position estimates from different satellites. Since WLS assigns weights based on signal quality, erroneous measurements from multipath-contaminated signals can degrade the overall solution.

Bias in Estimated Position: If multipath-affected measurements are not properly mitigated, they introduce systematic errors in the WLS estimation, causing the final position to deviate from the actual ground truth.

Solution Instability: The large variations in satellite-derived positions result in higher residuals in WLS, potentially reducing the robustness of the solution and increasing positioning uncertainty.

Error Amplification in Urban Areas: As multipath effects are more severe in dense urban environments, they introduce significant biases in range measurements, making WLS solutions much less reliable compared to open-sky conditions.

<img width="1549" alt="urban_position" src="https://github.com/user-attachments/assets/d2bb48c5-ea83-4bb6-b969-d12210a57252" />
<img width="1280" alt="Opensky_Position" src="https://github.com/user-attachments/assets/e4ab2616-b5ea-4456-89c9-f006a0466cc6" />


**Task 5 – Kalman Filter-Based Positioning
Develop an Extended Kalman Filter (EKF) using pseudorange and Doppler measurements to estimate user position and velocity.**

By the time submitting this assignment I was still debugging the algorithm for Kalman Filter-based Positioning. The code are in the repository，it hasn't generate ideal results yet. 
