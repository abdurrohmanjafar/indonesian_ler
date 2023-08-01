import re
import csv
from tqdm import tqdm
import requests

with open("dataset.csv", 'r') as dataset_file:
    dataset = csv.reader(dataset_file)
    for line in tqdm(list(dataset)):
        url = line[-1]
        text = requests.get(url).text
        res = re.search(r'<a href="(.*/pdf/' + re.escape(line[0]) + r')">', text)
        pdf_url = res.group(1)
        pdf = requests.get(pdf_url)
        with open(f'pdf/{line[0]}.pdf', 'wb') as out_file:
            out_file.write(pdf.content)
