# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """
    Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001.
    """
    return [datetime.strptime(d, "%Y-%m-%d").strftime("%d %b %Y") for d in old_dates]


def date_range(start, n):
    """
    For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous.
    """
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError("Invalid input types")

    return [datetime.strptime(start, "%Y-%m-%d") + timedelta(days=y) for y in range(n)]


def add_date_range(values, start_date):
    """
   Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list.
    """
    result = []
    for idx, value in enumerate(values):
        date = datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=idx)
        result.append((date, value))
    return result


def fees_report(infile, outfile):
    """
    Calculates late fees per patron id and writes a summary report to
    outfile.
    """
    # Open the input CSV file
    with open(infile) as f:
        # Initialize a list to store late fees data
        late_fees_data = []
        
        # Read the CSV file
        obj = DictReader(f)
        
        # Iterate through each row in the CSV
        for row in obj:
            # Calculate the difference between return date and due date
            days_late = (datetime.strptime(row['date_returned'], '%m/%d/%Y') - 
                          datetime.strptime(row['date_due'], '%m/%d/%Y')).days
            
            # Calculate late fee
            late_fee = max(days_late, 0) * 0.25
            
            # Store late fees data for each patron
            late_fees_data.append({'patron_id': row['patron_id'], 'late_fees': round(late_fee, 2)})
    
    # Aggregate late fees per patron
    aggregated_data = defaultdict(float)
    for data in late_fees_data:
        aggregated_data[data['patron_id']] += data['late_fees']
    
    # Format aggregated data for writing to outfile
    formatted_data = [{'patron_id': key, 'late_fees': '{:.2f}'.format(value)} for key, value in aggregated_data.items()]
    
    # Write the summary report to the output CSV file
    with open(outfile, "w", newline="") as file:
        writer = DictWriter(file, fieldnames=['patron_id', 'late_fees'])
        writer.writeheader()
        writer.writerows(formatted_data)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')
    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
