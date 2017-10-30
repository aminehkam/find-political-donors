import bisect
import csv
import datetime
import math
import pprint
import sys


def compute_median(a):
    """Given a list computes the median.

    If the list has even number of elements, the media is computed as the
    average of the two items in the middle of the list, otherwise the middle
    element is returned.

    If a is empty None is returned.
    """
    if len(a) > 0:
        if len(a) % 2 == 0:
            return math.trunc(math.ceil((a[len(a) / 2 - 1] + a[len(a) / 2]) / 2.0))
        else:
            return a[len(a) / 2]
    else:
        return None


def compute_zip_code(zip_code_text):
    """Given a US zipcode text, returns the first 5 digits.

    Returns None if the given text has non-digits in it.
    """
    zip_code = None
    if zip_code_text and len(zip_code_text) >= 5 and zip_code_text.isdigit():
        zip_code = zip_code_text[:5]
    return zip_code


def compute_date(date_text):
    """Given a text, checks if it is in mmddyyyy format and returns the date.

    If the date is malformed or is not in the right format and is not exactly
    8 characters returns the date.
    """
    dt = None
    if date_text and len(date_text) == 8:
        try:
            dt = datetime.datetime.strptime(date_text, '%m%d%Y')
        except ValueError:
            pass
    return dt


def compute_stats(input_filename, output_zipcode_filename, output_dt_filename):
    """Given a donors list in FEC (Federal Election Commission) format extracts
    zip-code and date based info.

    The outpus of this function are the running median of donors based on their
    recepient ID and zip-code and donation date. The two outputs are in CSV format
    delimited with |.
    """
    headers = {
        'CMTE_ID': 0,
        'ZIP_CODE': 10,
        'TRANSACTION_DT': 13,
        'TRANSACTION_AMT': 14,
        'OTHER_ID': 15}
    d_zip = dict()
    d_date = dict()

    zip_file = open(output_zipcode_filename, 'w+')
    zip_writer = csv.writer(zip_file, delimiter='|')
    with open(input_filename, "r") as donors_file:
        file_reader = csv.reader(donors_file, delimiter='|')
        for line in file_reader:
            if not line[headers['OTHER_ID']]:
                customer_id = line[headers['CMTE_ID']]
                zip_code = compute_zip_code(line[headers['ZIP_CODE']])
                dt = compute_date(line[headers['TRANSACTION_DT']])
                transaction_amount = int(line[headers['TRANSACTION_AMT']])

                if zip_code:
                    key = (customer_id, zip_code)
                    if not key in d_zip:
                        d_zip[key] = []
                    zip_list = d_zip[key]
                    bisect.insort(zip_list, transaction_amount)
                    zip_writer.writerow([customer_id, zip_code, compute_median(
                        zip_list), len(zip_list), sum(zip_list)])
                if dt:
                    key = (customer_id, dt)
                    if not key in d_date:
                        d_date[key] = []
                    date_list = d_date[key]
                    bisect.insort(date_list, transaction_amount)
    zip_file.close()
    with open(output_dt_filename, 'w+') as csvfile:
        date_writer = csv.writer(csvfile, delimiter='|')
        for (customer_id, dt) in sorted(d_date):
            date_list = d_date[(customer_id, dt)]
            date_writer.writerow([customer_id, dt.strftime('%m%d%Y'), compute_median(
                date_list), len(date_list), sum(date_list)])


def main():
    """ This program expects a donors input file in FEC format, and two file paths
    for date and zip-code based stats.
    For example: python data-eng.py 'itcont.txt' 'medianvals_by_zip.txt' 'medianvals_by_date.txt'
    """
    if len(sys.argv) != 4:
        sys.exit('Please run with : python data-eng.py donors_file.txt zipcode_output_filename date_output_filename')
    compute_stats(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == '__main__':
    main()
