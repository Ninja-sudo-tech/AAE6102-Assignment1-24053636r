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

The ephemeris data are as follows:

[Uploading gps_ephemeris.xml…]()<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<!DOCTYPE boost_serialization>
<boost_serialization signature="serialization::archive" version="19">
<GNSS-SDR_ephemeris_map class_id="0" tracking_level="0" version="0">
	<count>4</count>
	<item_version>0</item_version>
	<item class_id="1" tracking_level="0" version="0">
		<first>4</first>
		<second class_id="2" tracking_level="0" version="0">
			<PRN>4</PRN>
			<M_0>-5.69467665939790368e-01</M_0>
			<delta_n>4.36946772015489038e-09</delta_n>
			<ecc>1.45191792398691156e-03</ecc>
			<sqrtA>5.15369046783447266e+03</sqrtA>
			<OMEGA_0>2.45848997315267237e+00</OMEGA_0>
			<i_0>9.60892029581390972e-01</i_0>
			<omega>-3.09959920683989321e+00</omega>
			<OMEGAdot>-7.80961101593156993e-09</OMEGAdot>
			<idot>1.55363614375296496e-10</idot>
			<Cuc>-2.18488276004791260e-06</Cuc>
			<Cus>1.07884407043457031e-05</Cus>
			<Crc>1.71781250000000000e+02</Crc>
			<Crs>-4.03125000000000000e+01</Crs>
			<Cic>3.72529029846191406e-08</Cic>
			<Cis>2.04890966415405273e-08</Cis>
			<toe>396000</toe>
			<toc>396000</toc>
			<af0>-2.03651376068592072e-04</af0>
			<af1>4.54747350886464018e-13</af1>
			<af2>0.00000000000000000e+00</af2>
			<WN>131</WN>
			<tow>390288</tow>
			<satClkDrift>0.00000000000000000e+00</satClkDrift>
			<dtr>0.00000000000000000e+00</dtr>
			<IODE_SF2>167</IODE_SF2>
			<IODE_SF3>167</IODE_SF3>
			<code_on_L2>1</code_on_L2>
			<L2_P_data_flag>0</L2_P_data_flag>
			<SV_accuracy>0</SV_accuracy>
			<SV_health>0</SV_health>
			<TGD>-4.19095158576965332e-09</TGD>
			<IODC>935</IODC>
			<AODO>21600</AODO>
			<fit_interval_flag>0</fit_interval_flag>
			<spare1>0.00000000000000000e+00</spare1>
			<spare2>0.00000000000000000e+00</spare2>
			<integrity_status_flag>0</integrity_status_flag>
			<alert_flag>0</alert_flag>
			<antispoofing_flag>1</antispoofing_flag>
		</second>
	</item>
	<item>
		<first>16</first>
		<second>
			<PRN>16</PRN>
			<M_0>7.18116855169471435e-01</M_0>
			<delta_n>4.24660545959143784e-09</delta_n>
			<ecc>1.22962790774181468e-02</ecc>
			<sqrtA>5.15377132225036621e+03</sqrtA>
			<OMEGA_0>-1.67426142885169682e+00</OMEGA_0>
			<i_0>9.71603403113093012e-01</i_0>
			<omega>6.79609496852004002e-01</omega>
			<OMEGAdot>-8.01283376668914257e-09</OMEGAdot>
			<idot>-4.89306095848634901e-10</idot>
			<Cuc>1.38953328132629395e-06</Cuc>
			<Cus>7.68713653087615967e-06</Cus>
			<Crc>2.37687500000000000e+02</Crc>
			<Crs>2.33437500000000000e+01</Crs>
			<Cic>-1.00582838058471680e-07</Cic>
			<Cis>1.35973095893859863e-07</Cis>
			<toe>396000</toe>
			<toc>396000</toc>
			<af0>-4.06925100833177567e-04</af0>
			<af1>-6.36646291241049605e-12</af1>
			<af2>0.00000000000000000e+00</af2>
			<WN>131</WN>
			<tow>390288</tow>
			<satClkDrift>0.00000000000000000e+00</satClkDrift>
			<dtr>0.00000000000000000e+00</dtr>
			<IODE_SF2>9</IODE_SF2>
			<IODE_SF3>9</IODE_SF3>
			<code_on_L2>1</code_on_L2>
			<L2_P_data_flag>0</L2_P_data_flag>
			<SV_accuracy>0</SV_accuracy>
			<SV_health>0</SV_health>
			<TGD>-1.02445483207702637e-08</TGD>
			<IODC>9</IODC>
			<AODO>21600</AODO>
			<fit_interval_flag>0</fit_interval_flag>
			<spare1>0.00000000000000000e+00</spare1>
			<spare2>0.00000000000000000e+00</spare2>
			<integrity_status_flag>0</integrity_status_flag>
			<alert_flag>0</alert_flag>
			<antispoofing_flag>1</antispoofing_flag>
		</second>
	</item>
	<item>
		<first>27</first>
		<second>
			<PRN>27</PRN>
			<M_0>-1.73022280718201388e-01</M_0>
			<delta_n>4.03016787266861098e-09</delta_n>
			<ecc>9.57410689443349665e-03</ecc>
			<sqrtA>5.15365202140808105e+03</sqrtA>
			<OMEGA_0>-7.17474660465198477e-01</OMEGA_0>
			<i_0>9.74727542206026198e-01</i_0>
			<omega>6.30881664719349589e-01</omega>
			<OMEGAdot>-8.02426281418341680e-09</OMEGAdot>
			<idot>-7.14315468392167785e-13</idot>
			<Cuc>3.73087823390960693e-06</Cuc>
			<Cus>8.24220478534698486e-06</Cus>
			<Crc>2.30343750000000000e+02</Crc>
			<Crs>7.04375000000000000e+01</Crs>
			<Cic>1.08033418655395508e-07</Cic>
			<Cis>1.15483999252319336e-07</Cis>
			<toe>396000</toe>
			<toc>396000</toc>
			<af0>-2.06120777875185013e-04</af0>
			<af1>-5.00222085975110450e-12</af1>
			<af2>0.00000000000000000e+00</af2>
			<WN>131</WN>
			<tow>390288</tow>
			<satClkDrift>0.00000000000000000e+00</satClkDrift>
			<dtr>0.00000000000000000e+00</dtr>
			<IODE_SF2>30</IODE_SF2>
			<IODE_SF3>30</IODE_SF3>
			<code_on_L2>1</code_on_L2>
			<L2_P_data_flag>0</L2_P_data_flag>
			<SV_accuracy>0</SV_accuracy>
			<SV_health>0</SV_health>
			<TGD>1.86264514923095703e-09</TGD>
			<IODC>30</IODC>
			<AODO>21600</AODO>
			<fit_interval_flag>0</fit_interval_flag>
			<spare1>0.00000000000000000e+00</spare1>
			<spare2>0.00000000000000000e+00</spare2>
			<integrity_status_flag>0</integrity_status_flag>
			<alert_flag>0</alert_flag>
			<antispoofing_flag>1</antispoofing_flag>
		</second>
	</item>
	<item>
		<first>31</first>
		<second>
			<PRN>31</PRN>
			<M_0>2.82452321963232578e+00</M_0>
			<delta_n>4.80734310227928938e-09</delta_n>
			<ecc>1.02715539978817088e-02</ecc>
			<sqrtA>5.15362238883972168e+03</sqrtA>
			<OMEGA_0>-2.78727290293283003e+00</OMEGA_0>
			<i_0>9.55882550425047883e-01</i_0>
			<omega>3.11626182035605714e-01</omega>
			<OMEGAdot>-7.99497587997933773e-09</OMEGAdot>
			<idot>3.21441960776475511e-11</idot>
			<Cuc>1.46031379699707031e-06</Cuc>
			<Cus>7.22892582416534424e-06</Cus>
			<Crc>2.40156250000000000e+02</Crc>
			<Crs>3.07187500000000000e+01</Crs>
			<Cic>-1.13621354103088379e-07</Cic>
			<Cis>-5.02914190292358398e-08</Cis>
			<toe>396000</toe>
			<toc>396000</toc>
			<af0>-1.44899822771549225e-04</af0>
			<af1>-1.93267624126747210e-12</af1>
			<af2>0.00000000000000000e+00</af2>
			<WN>131</WN>
			<tow>390288</tow>
			<satClkDrift>0.00000000000000000e+00</satClkDrift>
			<dtr>0.00000000000000000e+00</dtr>
			<IODE_SF2>83</IODE_SF2>
			<IODE_SF3>83</IODE_SF3>
			<code_on_L2>1</code_on_L2>
			<L2_P_data_flag>0</L2_P_data_flag>
			<SV_accuracy>0</SV_accuracy>
			<SV_health>0</SV_health>
			<TGD>-1.30385160446166992e-08</TGD>
			<IODC>83</IODC>
			<AODO>21600</AODO>
			<fit_interval_flag>0</fit_interval_flag>
			<spare1>0.00000000000000000e+00</spare1>
			<spare2>0.00000000000000000e+00</spare2>
			<integrity_status_flag>0</integrity_status_flag>
			<alert_flag>0</alert_flag>
			<antispoofing_flag>1</antispoofing_flag>
		</second>
	</item>
</GNSS-SDR_ephemeris_map>
</boost_serialization>





**Task 4 – Position and Velocity Estimation
Using pseudorange measurements from tracking, implement the Weighted Least Squares (WLS) algorithm to compute the user's position and velocity.
Plot the user position and velocity.
Compare the results with the ground truth.
Discuss the impact of multipath effects on the WLS solution.**


**Task 5 – Kalman Filter-Based Positioning
Develop an Extended Kalman Filter (EKF) using pseudorange and Doppler measurements to estimate user position and velocity.**

