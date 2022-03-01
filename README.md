# Purpose
Monitor the health of vehicles remotely. 
 
# ETL Design 
![image](https://user-images.githubusercontent.com/76083769/155837691-7faa2c4e-601f-4ecf-8813-8ac03b1c547c.png)

# Pre-ETL and Data Ingestion
 1. Start the vehicle engine.
 2. Plug the OBDLink MX+ bluetooth adapter to the OBD2 port in the vehicle.
 3. Pair the OBDLink MX+ bluetooth adapter to a computer or microcontroller.
 4. Open the OBDWiz software and run a "diagnostics test".
 5. Save diagnostic report as text file to local disk. 

![image](https://user-images.githubusercontent.com/76083769/156122181-69638b3f-a950-485c-95e6-ba0bcc20d886.png)

# ETL
 6. Sync data from local folder to AWS S3 input bucket --> _s3://obd-diagnostic-data-input/_

![image](https://user-images.githubusercontent.com/76083769/156122285-1c7c8450-b95a-4adb-9e5c-29b14c8fdb0c.png)

7. S3 sync triggers _processor_lambda.py_ which processes the html diagnostic data as a set of parquet tables to AWS S3 output bucket --> _s3://obd-diagnostic-data-output/_

![image](https://user-images.githubusercontent.com/76083769/155828172-75d98463-3941-47c4-a441-f4e966637b79.png)

![image](https://user-images.githubusercontent.com/76083769/155828238-4be7aea0-fce0-4a6d-b603-0bd8d096c71f.png)

![image](https://user-images.githubusercontent.com/76083769/155828273-4fea0ed7-80de-4431-9697-3ae50d7660d0.png)

# AWS Glue
- Crawlers 
![image](https://user-images.githubusercontent.com/76083769/155834706-b7875bbf-2f76-4781-8406-d4541b4f0307.png)
- Data Catalog
![image](https://user-images.githubusercontent.com/76083769/155834467-542ec8f3-3f90-4635-a2fe-3cbf1033ebd2.png)

# AWS Athena 
![image](https://user-images.githubusercontent.com/76083769/155836089-49f78521-af51-4f70-ba00-f423bb03abe5.png)

# Data Sources 
 - 2008 Honda Odyssey
 - 2013 Infiniti M37
 - 2015 Honda Accord
 - 2017 Acura RDX
 - 2017 Honda Pilot
 - 2017 Toyota Camry
 - 2018 Toyota Camry
 - 2020 Volkswagen Jetta
 - 2022 Kia k5
 
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

