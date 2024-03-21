import csv
import json
import requests
import time
from random import uniform


def call_api(page_number):
    url = 'http://www.tcmip.cn:18124/home/browse/'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'http://www.tcmip.cn',
        'Referer': 'http://www.tcmip.cn/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }

    data = {
        'params': {},
        'type': 'target',
        'pageNo': page_number,
        'pageSize': 20,
        'orderBy': '',
        'sequential': '',
        'search_key': '',
        'language': 'en'
    }

    response = requests.post(url, headers=headers, json=data, verify=False)
    return response


def parse_response(response, csv_writer, is_first_page, header):
    if response.status_code == 200:
        response_data = response.json()
        data_list = response_data.get('data', [])[0].get('data', [])

        if is_first_page:
            # Write header for the first page
            csv_writer.writerow(['"{}"'.format(key) for key in header])

        # Write data
        for item in data_list:
            row = ['"{}"'.format(';'.join(map(str, item[key]))) if isinstance(item[key], list) else '"{}"'.format(
                item[key]) for key in header]
            csv_writer.writerow(row)

        return f"Data for Page {page_number} written to CSV"
    else:
        return f"Failed to fetch data for Page {page_number}. Status Code: {response.status_code}"


csv_file_path = 'output.csv'

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=';')
    header = None  # Initialize header outside of the loop

    for page_number in range(1, 53):
        response = call_api(page_number)

        if header is None:
            header = [key for key in response.json().get('data', [])[0].get('data', [])[0].keys() if
                      key != 'linkformat']

        result_message = parse_response(response, csv_writer, page_number == 1, header)
        print(result_message)