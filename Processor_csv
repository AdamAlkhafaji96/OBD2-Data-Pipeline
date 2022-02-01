from datetime import datetime
import awswrangler as wr
import boto3
from bs4 import BeautifulSoup
import pandas as pd

def html_to_parquet():
    """
    Args: raw html files read from s3 -> 'obd-diagnostic-data-input'
    Using: bs4, pandas, boto3, awswrangler
    Returns: .parquet files to s3 ->'obd-diagnostic-data-output'
    """
    boto3.setup_default_session(profile_name='default')

    s3 = boto3.client('s3')
    
    raw_bucket = 'obd-diagnostic-data-input'
    key = 'Diagnostic Report Honda Pilot 2017 1_29_2022.html'    
    
    pandas_response = s3.get_object(Bucket=raw_bucket, Key=key)
    soup_response = s3.get_object(Bucket=raw_bucket, Key=key)
    
    pandas_content = pandas_response['Body']
    soup_content = soup_response['Body']
    
    df_list = pd.read_html(pandas_content)
    
    soup = BeautifulSoup(soup_content, 'html.parser')

    b = soup.b.parent.text.split() 
    
    vals = {
        'Time': '', 
        'VIN': '',
        'Manufacturer': '',
        'Model': '',
        'Option': '',
        'Year': ''}

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
                              columns=['Time', 'VIN', 'Manufacturer', 
                                       'Model', 'Option', 'Year'], 
                              index=[0])
    
    vehicle_df.to_csv(path_or_buf='vehicle_df', header=True)
    
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
        'in_performance_tracking': True}
    
    for i in range(len(df_list) - 1):
        
        software_df = df_list[0]
        software_df.rename(columns={0: "Name", 1: "Website"}, inplace=True)
        df_list[0] = software_df
            
        check = soup.br.parent.text
        
        target = 'There are no pending, stored, or \
                permanent diagnostic trouble codes (DTCs).'
        for idx, _ in enumerate(check):
            if check[idx:idx+75] == target:
                frames['trouble_codes'] = False
                frames['additional_info'] = False
                    
        target_2 = 'Freeze Frame data is not available.'
        for idx, _ in enumerate(check):
            if check[idx:idx+35] == target_2:
                frames['freeze_frame_data'] = False

        if len(df_list[i]) == 0:
            frames['oxygen_sensors'] = False
            del df_list[i]
                
        target_3 = 'On-Board Monitoring data is not available'
        for idx, _ in enumerate(check):
            if check[idx:idx+41] == target_3:
                frames['on_board_monitoring'] = False
            
        target_4 = 'In-Performance Tracking'
        h3 = soup('h3')
        check_4 = [h3[idx].text for idx, _ in enumerate(h3)]
        if target_4 not in check_4:
            frames['in_performance_tracking'] = False
        
        frame_exists = [key for key, val in frames.items() if val is True]

    for index, _ in enumerate(df_list):
        
        df_list[index].to_csv(path_or_buf=frame_exists[index], header=True)
        
    return f"Etl Success for {vals['Manufacturer']} {vals['Model']} {vals['Year']}"
