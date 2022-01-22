# Purpose
Monitor the health of vehicles remotely. 
 
# ETL Design 
![image](https://user-images.githubusercontent.com/76083769/148834719-e6a579a5-0aac-4478-b291-30272760181e.png)

# Pre-ETL Data Retrieval
1. Start the vehicle engine.
2. Plug the OBDLink MX+ bluetooth adapter to the OBD2 port in the vehicle.
3. Pair the OBDLink MX+ bluetooth adapter to a computer or microcontroller.
4. Open the OBDWiz software and run a diagnostics test 
5. Save diagnostic report as text file to local disk
6. Upload data from local folder to S3 input bucket - s3://obd-diagnostic-input/

# ETL
- "Processor Lambda" reads data from S3, processes that data using Spark, and writes processed data as a set of dimensional tables back to S3

# Data Model
![OBD_erd](https://user-images.githubusercontent.com/76083769/150624827-f35bf4f9-446c-4672-9455-c903e7916505.JPG)

# Data Sources 
 - Honda Odyssey 2008
 - Honda Pilot 2017
 
 # Hardware Specs 
 - [OBDLink MX+](https://www.obdlink.com/products/obdlink-mxp/)
 - [OBDLink MX+ Specs](https://www.obdlink.com/wp-content/uploads/2019/01/app_support.pdf)

# Software
 - [OBDwiz](https://www.obdlink.com/software/)

# Set up
- [OBDLink MX+ support and set-up](https://www.obdlink.com/support/mxp/#win-mxp)

# Background info
- [Controller Area Network (CAN bus) simple intro](https://www.csselectronics.com/pages/can-bus-simple-intro-tutorial)
- [On Board Diagnostics](https://en.wikipedia.org/wiki/On-board_diagnostics)
- [On Board Diagnostics (OBD2) explained simple intro](https://www.csselectronics.com/pages/obd2-explained-simple-intro)
- [Parameter IDs (PID)](https://en.wikipedia.org/wiki/OBD-II_PIDs)

![image](https://user-images.githubusercontent.com/76083769/149011965-7d9670ee-1549-4838-8745-8b0c0b6768de.png)

- [Diagnostic Trouble Codes (DTC)](https://www.dmv.de.gov/VehicleServices/inspections/pdfs/dtc_list.pdf)

![image](https://user-images.githubusercontent.com/76083769/148725136-97df9337-a5a8-4445-9896-a6a814261287.png)

![image](https://user-images.githubusercontent.com/76083769/149032586-7ebc24ec-5ea5-4d52-b9a6-f0d393a6c68f.png)

