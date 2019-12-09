def clean_file(fname):
    '''replace all the NULLs with empty string
    change the date format to YYYY-MM-DD
    trim the time component in the last date col
    '''
    df = pd.read_csv(fname, 
                     na_values='NULL', # conv all the str NULL to nulls
                    parse_dates=['PwC_ExpensePaidDate', 'PwC_Last_Updated_date'])
    # put an _out before writing to output csv 
    fsuffix = '.csv'
    new_suffix = '_out.csv'
    fname = fname.rstrip(fsuffix) + new_suffix
    # write date to std format
    df.to_csv(fname, index=False, na_rep='', date_format='%Y-%m-%d')

def get_files_in_path(loc):
    """get all the files in this loc 
    and put an _out before the .csv
    and return the list of file names"""
    entries = os.scandir(path)
    files = []
    for entry in entries:
        fname = os.path.join(path, entry.name)
        files.append(fname)
    return files

def get_files_in_path(loc):
    """get all the files in this loc 
    and put an _out before the .csv
    and return the list of file names"""
    entries = os.scandir(path)
    files = []
    for entry in entries:
        fname = os.path.join(path, entry.name)
        files.append(fname)
    return files
    
main()            

