# Purpose
Monitor the health of vehicles remotely. 
 
# ETL Design 
![image](https://user-images.githubusercontent.com/76083769/150627514-a00b7339-031f-49c5-88ae-15577e40fd32.png)

# Pre-ETL Data Retrieval
1. Start the vehicle engine.
2. Plug the OBDLink MX+ bluetooth adapter to the OBD2 port in the vehicle.
3. Pair the OBDLink MX+ bluetooth adapter to a computer or microcontroller.
4. Open the OBDWiz software and run a "diagnostics test".
5. Save diagnostic report as text file to local disk. 
6. Sync data from local folder to AWS S3 input bucket --> _s3://obd-diagnostic-data-input/_

![image](https://user-images.githubusercontent.com/76083769/155813294-114cc19c-e392-48bc-ac44-c3abc8123374.png)

![image](https://user-images.githubusercontent.com/76083769/155813379-bd3f3beb-c3d2-4e5f-9f2b-73aafa1369c3.png)

# ETL
- Invoke _processor_lambda.py_ to process the raw html diagnostic data
- Write processed data as a set of parquet tables to AWS S3 output bucket --> _s3://obd-diagnostic-data-output/_

![image](https://user-images.githubusercontent.com/76083769/155813461-8f31dfe8-7ac7-436b-89a0-60868a582975.png)

![image](https://user-images.githubusercontent.com/76083769/155813521-50a63dd2-930a-41e9-8266-e36f6775a9df.png)

![image](https://user-images.githubusercontent.com/76083769/155813589-7003d716-c3fc-491b-b0b5-9eca20458cd3.png)

# Data Model
![image](https://user-images.githubusercontent.com/76083769/155823228-68e36451-79ca-408a-ab94-c1ee74fc946d.png)
![image](https://user-images.githubusercontent.com/76083769/155823160-b4abb5b3-7f06-4274-8024-862fee279551.png)


# Data Sources 
 - Honda Accord 2015
 - Honda Odyssey 2008
 - Honda Pilot 2017
 - Toyota Camry 2018
 - Volkswagen Jetta 2020
 
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

