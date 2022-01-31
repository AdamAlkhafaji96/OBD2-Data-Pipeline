import awswrangler as wr
import boto3
import bs4
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def html_to_parquet():
    """
    Args: raw html files read from s3 -> 'obd-diagnostic-data-input'
    Using: bs4, pandas, boto3, awswrangler
    Returns: .parquet files to s3 ->'obd-diagnostic-data-output'
    """
    boto3.setup_default_session(profile_name='default')

    s3 = boto3.client('s3')
    
    raw_bucket = 'obd-diagnostic-data-input'
    key = 'Diagnostic Report Toyota Camry 2018 1_30_2022.html'
    
    pandas_response = s3.get_object(Bucket=raw_bucket, Key=key)
    soup_response = s3.get_object(Bucket=raw_bucket, Key=key)
    
    pandas_content = pandas_response['Body']
    soup_content = soup_response['Body']
    
    df_list = pd.read_html(pandas_content)
    
    soup = BeautifulSoup(soup_content, 'html.parser')

    b = soup.b.parent.text.split() 
    
    vals = {
        'Time': 'NULL', 
        'VIN': 'NULL',
        'Manufacturer': 'NULL',
        'Model': 'NULL',
        'Option': 'NULL',
        'Year': 'NULL'
    }

    for i in range(len(b) - 1):
        if b[i] == 'Date:':
            time_val = []
            for i in range(3):
                time_val += b[i+1] 
                time_val += ' '
            date_str = ''.join(time_val).rstrip()
            date_obj = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
            vals['Time'] = date_obj.strftime('%Y-%m-%d %I:%M:%S %p')
            
        elif b[i] == 'VIN:':
            vals['VIN'] = b[i+1]
            
        elif b[i] == 'Manufacturer:':
            vals['Manufacturer'] = b[i+1]
            
        elif b[i] == 'Model:':
            vals['Model'] = b[i+1]
            
        elif b[i] == 'Option:':
            vals['Option'] = b[i+1]
            
        elif b[i] == 'Year:':
            vals['Year'] = b[i+1]
    
    vehicle_df = pd.DataFrame(vals, 
                              columns=['Time', 
                                       'VIN', 
                                       'Manufacturer', 
                                       'Model', 
                                       'Option', 
                                       'Year'], 
                              index=[0]
    )
    
    file_date = date_obj.strftime('%Y_%m_%d')

    file_name = '{}_{}_{}/VIN: {}/{}/{}'.format(vals['Manufacturer'],
                                                vals['Model'], 
                                                vals['Year'],
                                                vals['VIN'], 
                                                'vehicle_report_info',
                                                file_date
    )  
    
    path_1 = 's3://obd-diagnostic-data-output/{}'.format(file_name)
    
    wr.s3.to_parquet(df=vehicle_df,
                    path=path_1,
                    compression='gzip',
                    dataset=True,
                    mode='append'
    )
    
    frames = {
        'software_info': True,
        'monitor_status': True, 
        'trouble_codes': True,
        'additional_info': True, 
        'powertrain_data': True, 
        'freeze_frame_data': True,
        'oxygen_sensors': True,
        'on_board_monitoring': True,
        'general_info': True,
        'in_performance_tracking': True
    }
    
    for i in range(len(df_list) - 1):
        
        software_df = df_list[0]
        software_df.rename(columns={0: "Name", 1: "Website"}, inplace=True)
            
        check = soup.br.parent.text
        
        target = 'There are no pending, stored, or permanent diagnostic trouble codes (DTCs).'
        for t in range(len(check)):
            if check[t:t+75] == target:
                frames['trouble_codes'] = False
                frames['additional_info'] = False
                    
        target_2 = 'Freeze Frame data is not available.'
        for f in range(len(check)):
            if check[f:f+35] == target_2:
                frames['freeze_frame_data'] = False

        if len(df_list[i]) == 0:
            frames['oxygen_sensors'] = False
            del(df_list[i])
                
        target_3 = 'On-Board Monitoring data is not available'
        for o in range(len(check)):
            if check[o:o+41] == target_3:
                frames['on_board_monitoring'] = False
            
        target_4 = 'In-Performance Tracking'
        h3 = soup('h3')
        check_4 = [h3[element].text for element in range(len(h3))]
        if target_4 not in check_4:
            frames['in_performance_tracking'] = False
        
        frame_exists = [key for key, val in frames.items() if val == True]

    for index in range(len(df_list)):
            
        file_names = '{}_{}_{}/VIN: {}/{}/{}'.format(vals['Manufacturer'],
                                                     vals['Model'], 
                                                     vals['Year'], 
                                                     vals['VIN'],
                                                     frame_exists[index], 
                                                     file_date
        )

        path_2 = 's3://obd-diagnostic-data-output/{}'.format(file_names)

        wr.s3.to_parquet(df=df_list[index],
                         path=path_2,
                         compression='gzip',
                         dataset=True,
                         mode='append'
        )
        
    return 'Etl Success for {} {} {}'.format(vals['Manufacturer'], vals['Model'], vals['Year'])
