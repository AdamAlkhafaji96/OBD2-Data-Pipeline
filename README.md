# Purpose
Monitor the health of vehicles remotely. 
 
# ETL Design 
![image](https://user-images.githubusercontent.com/76083769/155837691-7faa2c4e-601f-4ecf-8813-8ac03b1c547c.png)

# 18 Data Sources 
 - 2007 Honda Accord
 - 2008 Ford Fusion
 - 2008 Honda Odyssey
 - 2009 Honda Accord
 - 2011 Nissan Versa 
 - 2013 Infiniti M37
 - 2014 Ford Escape
 - 2014 Hyundai Veloster
 - 2015 Honda Accord
 - 2016 Honda Accord 
 - 2017 Acura RDX
 - 2017 Honda Pilot
 - 2017 Toyota Camry
 - 2018 Ram 1500 
 - 2018 Toyota Camry
 - 2020 Volkswagen Jetta
 - 2021 Toyota Camry 
 - 2022 Kia k5

# Pre-ETL and Data Ingestion
 1. Start the vehicle engine.
 2. Plug the OBDLink MX+ bluetooth adapter into the OBD2 port in the vehicle.
 3. Pair the OBDLink MX+ bluetooth adapter to a computer or microcontroller.
 4. Open the OBDWiz software and run a "diagnostics test".
 5. Save diagnostic report as html file to local disk. 

![image](https://user-images.githubusercontent.com/76083769/161366031-0290638a-b687-4a16-9a52-9358d2b7589a.png)

# ETL
 6. Sync data from local folder to AWS S3 input bucket --> _s3://obd-diagnostic-data-input/_

![image](https://user-images.githubusercontent.com/76083769/161366051-3326165a-f097-4bc9-88c3-0dcf3f0bd28a.png)

7. S3 sync triggers _processor_lambda.py_ which processes the html diagnostic data as a set of parquet tables to AWS S3 output bucket --> _s3://obd-diagnostic-data-output/_

![image](https://user-images.githubusercontent.com/76083769/156135451-898681c2-7d5b-4ec0-bcfb-fea39c98788e.png)

![image](https://user-images.githubusercontent.com/76083769/156138229-ffab6cea-b570-48e9-af69-db259a2b1ee9.png)

# AWS Glue
- Crawlers 
![image](https://user-images.githubusercontent.com/76083769/156142316-2d5606c6-6ba2-4ebf-98f2-86ed212d0662.png)
- Data Catalog
![image](https://user-images.githubusercontent.com/76083769/156147871-5fa2286d-e01e-42ab-9663-9c3eeabf8ef9.png)
- Partitions (vehicle, vehicle_id, occurred_at)
![image](https://user-images.githubusercontent.com/76083769/156148405-8faf6b12-a960-4dfa-ac69-19b4445653e5.png)


# AWS Athena 
![image](https://user-images.githubusercontent.com/76083769/156147708-b84db3e8-a594-4e91-a05a-4788b86fe691.png) 

![image](https://user-images.githubusercontent.com/76083769/161365656-241103b6-119d-4db8-8f40-c0568a65d38a.png)

 # Hardware Specs 
 - [OBDLink MX+](https://www.obdlink.com/products/obdlink-mxp/)
 - [OBDLink MX+ Specs](https://www.obdlink.com/wp-content/uploads/2019/01/app_support.pdf)

# Software
 - [OBDwiz](https://www.obdlink.com/software/)

# Set up
- [OBDLink MX+ support and set-up](https://www.obdlink.com/support/mxp/#win-mxp)

# Coverage and Compatibility

![image](https://user-images.githubusercontent.com/76083769/156130747-bf3cd1b7-522d-4fae-8f23-c6438ef4499a.png)
![image](https://user-images.githubusercontent.com/76083769/156130873-99054a4e-0a36-4987-89e1-91f0a335f635.png)


# Background info
- [Controller Area Network (CAN bus) simple intro](https://www.csselectronics.com/pages/can-bus-simple-intro-tutorial)
- [On Board Diagnostics](https://en.wikipedia.org/wiki/On-board_diagnostics)
- [On Board Diagnostics (OBD2) explained simple intro](https://www.csselectronics.com/pages/obd2-explained-simple-intro)
- [Parameter IDs (PID)](https://en.wikipedia.org/wiki/OBD-II_PIDs)

![image](https://user-images.githubusercontent.com/76083769/149011965-7d9670ee-1549-4838-8745-8b0c0b6768de.png)

- [Diagnostic Trouble Codes (DTC)](https://www.dmv.de.gov/VehicleServices/inspections/pdfs/dtc_list.pdf)

![image](https://user-images.githubusercontent.com/76083769/148725136-97df9337-a5a8-4445-9896-a6a814261287.png)

![image](https://user-images.githubusercontent.com/76083769/149032586-7ebc24ec-5ea5-4d52-b9a6-f0d393a6c68f.png)

