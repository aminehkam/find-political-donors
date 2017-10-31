# Introduction
This project uses a dataset of published campaign contributions collected from [FEC (The Federal Election Commission)](http://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml). The goal in here is to identify the area, i.e. zipcodes, and time periods that can provide an insight into potential future donations by similar candidates.

# Approach: Details of the project
## Input - FEC Campaign Contributions File
Each line of the data provided by FEC entails information regarding a specific contribution received by a recipient. Each recipient is uniquely identified by an ID code, and each donation contains information including but not limited to: zip code, date and amount of the donation. The values in this input are delimited by `|` character.

In this project, we are only interested in individual contributions (made by a person) and will ignore any row which is not identified as an individual contribution. To identify such rows, we use one of the columns in the input that we refer to as `OTHER_ID`, which if empty denotes individual contributions.

The input provided by FEC has the following format with 21 fields in which we are only interested in columns [0, 10, 13, 14, 15] which are bolded in the following:

> **C00177436**|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|**300047357**|UNUM|SVP, SALES, CL|**01312017**|**384**||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337

Please note that in the above example, the `OTHER_ID`, i.e. column 15 is empty.

## Outputs
Given the information provided in the input file, we generate two output files:

1. `medianvals_by_zip.txt`: provides calculated running median, total dollar amount and total number of contributions by recipient and zip code
2. `medianvals_by_date.txt`: provides calculated median, total dollar amount and total number of contributions by recipient and date.

Similar to the input, the output is delimited by `|`.

## Implementation: Code summary
To read the input and to generate output we use python `csv` package, which allows us to simply read and write delimited files. The code consists of a single loop over input lines. We use two dictionaries for zipcode-based and date-based donation stats. In each iteration we read one line of the input we identify the unique `(recipient_id, zip_code)` and `(recipient_id, donation_date)` keys and add the new donation amount to the value pointed by each of these keys in the sorted format. To avoid resorting and to keep our algorithm efficient we use `bisect.insort` for both values. `bisect.insort` provides an efficient implementation of insertion sort which keeps our algorithm efficient and reduces the complexity of finding the median.

To generate the output, we write stats per `(recipient_id, zip_code)` to `medianvals_by_zip.txt` in each iteration and when the input is read completely, we iterate over the date-based dictionary and write its stats to `medianvals_by_date.txt`. Each of these outputs will have the following information:
```sh
# medianvals_by_zip.txt format:
recipient_id|zip_code|running_median|quantity|sum
# medianvals_by_date.txt format:
recipient_id|mmddyyyy|running_median|quantity|sum
```

The rest of the functions that are used are documented below.

### Compute Median Function
Given a list, this function computes the median. If the list has even number of elements, the median is computed as the
average of the two items in the middle of the list, otherwise the middle element is returned. If list is empty, None is returned.

### Compute Zipcode Function
Given a US zipcode text, this function returns the first 5 digits. Returns None if the given text has non-digits in it.

### Compute Date Function
Given a text, this function checks if it is in mmddyyyy format and returns the date. If the date is malformed or is not in the right format or is not exactly 8 characters, None is returned.

## Performance on Larger Inputs
To test my program on a larger input I have used [FEC data for individual contribution](http://classic.fec.gov/finance/disclosure/ftpdet.shtml). This input is around 800M after extraction, and my program analyzes this file in about 30 seconds on a Macbook Air (Core i5 and 4G of RAM).
