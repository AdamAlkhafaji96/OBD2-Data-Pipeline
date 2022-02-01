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
    key = 'Diagnostic Report Honda Pilot 2017 1_21_2022.html'    
    
    pandas_response = s3.get_object(Bucket=raw_bucket, Key=key)
    soup_response = s3.get_object(Bucket=raw_bucket, Key=key)
    
    pandas_content = pandas_response['Body']
    soup_content = soup_response['Body']
    
    df_list = pd.read_html(pandas_content)
    
    soup = BeautifulSoup(soup_content, 'html.parser')

    b_list = soup.b.parent.text.split() 
    
    vals = {
        'Time': '', 
        'VIN': '',
        'Manufacturer': '',
        'Model': '',
        'Option': '',
        'Year': ''
    }

    for i in range(len(b_list) - 1):
        if b_list[i] == 'Date:':
            time_val = []
            for i in range(3):
                time_val.append(b_list[i+1]) 
                time_val.append(' ')
            date_str = ''.join(time_val).rstrip()
            date_obj = datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
            vals.update({'Time': date_obj.strftime('%Y-%m-%d %I:%M:%S %p')})
            
        elif b_list[i] == 'VIN:':
            vals.update({'VIN': b_list[i+1]})
            
        elif b_list[i] == 'Manufacturer:':
            vals.update({'Manufacturer': b_list[i+1]})
            
        elif b_list[i] == 'Model:':
            vals.update({'Model': b_list[i+1]})
            
        elif b_list[i] == 'Option:':
            vals.update({'Option': b_list[i+1]})
            
        elif b_list[i] == 'Year:':
            vals.update({'Year': b_list[i+1]})
    
    vehicle_df = pd.DataFrame(vals, 
                              columns=['Time', 'VIN', 'Manufacturer', 
                                       'Model', 'Option', 'Year'], 
                              index=[0])
    
    file_date = date_obj.strftime('%Y_%m_%d')
    
    car_name = f"{vals['Manufacturer']}_{vals['Model']}_{vals['Year']}"

    file_name = f"{car_name}/VIN: {vals['VIN']}/{'vehicle_report_info'}/{file_date}"
    
    path_1 = f"s3://obd-diagnostic-data-output/{file_name}"
    
    wr.s3.to_parquet(df=vehicle_df,
                    path=path_1,
                    compression='gzip',
                    dataset=True,
                    mode='append')
    
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
        df_list[0] = software_df
            
        check = soup.br.parent.text
        
        target = 'There are no pending, stored, or \
                permanent diagnostic trouble codes (DTCs).'
        for idx, _ in enumerate(check):
            if check[idx:idx+75] == target:
                frames.update({'trouble_codes': False})
                frames.update({'additional_info': False})
                    
        target_2 = 'Freeze Frame data is not available.'
        for idx, _ in enumerate(check):
            if check[idx:idx+35] == target_2:
                frames.update({'freeze_frame_data': False})

        if len(df_list[i]) == 0:
            frames.update({'oxygen_sensors': False})
            del df_list[i]
                
        target_3 = 'On-Board Monitoring data is not available'
        for idx, _ in enumerate(check):
            if check[idx:idx+41] == target_3:
                frames.update({'on_board_monitoring': False})
            
        target_4 = 'In-Performance Tracking'
        h3 = soup('h3')
        check_4 = [h3[element].text for element, _ in enumerate(h3)]
        if target_4 not in check_4:
            frames.update({'in_performance_tracking': False})
        
        frame_exists = [key for key, val in frames.items() if val is True]

    for index, _ in enumerate(df_list):
        
        file_names = f"{car_name}/VIN: {vals['VIN']}/{frame_exists[index]}/{file_date}"

        path_2 = f"s3://obd-diagnostic-data-output/{file_names}"

        wr.s3.to_parquet(df=df_list[index],
                         path=path_2, 
                         compression='gzip',
                         dataset=True,
                         mode='append')
        
    return f"Etl Success for {car_name} VIN: {vals['VIN']}"
