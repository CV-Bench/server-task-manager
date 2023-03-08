import json
import glob

def get_stats(path->str)->tuple:
    """prints the first, last and current mAP of a log file

    Args:
        path (str): the path to the log file

    Returns:
        tuple: (first mAP, last mAP, current mAP) as floats. If the log file is empty, all values are 0. If the log file contains only one line, all values are the last value, if the log file contains only two lines, the first and last value are the same, and the current value is the second value.
    """
    
    # first line contains the header
    # last line is empty
    lines = open(path, 'r').read().split('\n')[1:-1]
    logs = [json.loads(line) for line in lines]
    val_mAP = [log for log in logs if log['mode'] == 'val']
    

    if len(val_mAP) == 0:
       first, last, current =  0, 0, 0
    
    elif len(val_mAP) == 1:
        first, last, current = val_mAP[0], val_mAP[0], val_mAP[0]    
        
    elif len(val_mAP) == 2:
        return val_mAP[0], val_mAP[0], val_mAP[1]
    
    else:
        first, last, current = val_mAP[0], val_mAP[-2], val_mAP[-1]
    
    return first, last, current

def get_logs():
    log_files = glob.glob('./data/networks/*/*.log.json')
    for log_file in log_files:
        id = log_file.split('networks/')[1]
        id = id.split('/')[0]
        print(id)
        print(get_stats(log_file))

get_logs()
