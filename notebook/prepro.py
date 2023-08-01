import re
from copy import copy

notices_footer = r"Disclaimer\s*Kepaniteraan\s*Mahkamah\s*Agung\s*Republik\s*Indonesia\s*berusaha\s*untuk\s*selalu\s*mencantumkan\s*informasi\s*paling\s*kini\s*dan\s*akurat\s*sebagai\s*bentuk\s*komitmen\s*Mahkamah\s*Agung\s*untuk\s*pelayanan\s*publik,\s*transparansi\s*dan\s*akuntabilitas\s*pelaksanaan\s*fungsi\s*peradilan\.\s*Namun\s*dalam\s*hal-hal\s*tertentu\s*masih\s*dimungkinkan\s*terjadi\s*permasalahan\s*teknis\s*terkait\s*dengan\s*akurasi\s*dan\s*keterkinian\s*informasi\s*yang\s*kami\s*sajikan,\s*hal\s*mana\s*akan\s*terus\s*kami\s*perbaiki\s*dari\s*waktu\s*kewaktu\.\s*Dalam\s*hal\s*Anda\s*menemukan\s*inakurasi\s*informasi\s*yang\s*termuat\s*pada\s*situs\s*ini\s*atau\s*informasi\s*yang\s*seharusnya\s*ada,\s*namun\s*belum\s*tersedia,\s*maka\s*harap\s*segera\s*hubungi\s*Kepaniteraan\s*Mahkamah\s*Agung\s*RI\s*melalui\s*:\s*Email\s*:\s*kepaniteraan@mahkamahagung\.go\.id\s*Telp\s*:\s*021-384\s*3348\s*\(ext\.318\)\s*Halaman\s*\d+"

notices_header = r'Direktori Putusan Mahkamah Agung Republik Indonesia\s*putusan.mahkamahagung.go.id\s*'
notices_header_s1 = r'Direktori Putusan Mahkamah Agung Republik Indonesia\s*'
notices_header_s2 = r'putusan.mahkamahagung.go.id\s*'


def merge_single_letter(source):
    res = copy(source)
    while True:
        match = re.search(r'\s+[A-z](\s+[A-z])+\s+', res)
        if match is None:
            break
        replacement = re.sub('\s', '', match.group())
        res = res[:match.start() + 1] + replacement + res[match.end() - 1:]
    return res


def combine_case_no(source):
    res = []
    for line in source.split('\n'):
        match = re.search(r'\d+\/[A-z\.]*', line)
        if match is not None:
            line = line[:match.start()] + re.sub('\s', '', line[match.start():])
        res.append(line)
    return '\n'.join(res)


def pipeline(x):
    x = re.sub(r"\s\s+", " ", x)
    x = re.sub(r"--+", " ", x)
    x = re.sub(r"__+", " ", x)
    x = merge_single_letter(x)
    x = re.sub(notices_footer, "", x, flags=re.MULTILINE)
    x = re.sub(notices_header, "", x, flags=re.MULTILINE)
    x = re.sub(notices_header_s1, "", x, flags=re.MULTILINE)
    x = re.sub(notices_header_s2, "", x, flags=re.MULTILINE)
    x = re.sub(r'- \d+ -', "", x)
    x = re.sub(r'^Mahkamah Agung Republik Indonesia$', r'', x, flags=re.IGNORECASE | re.MULTILINE)
    x = re.sub(r'•', '-', x)
    x = re.sub(r',-', ' ', x)
    x = re.sub(r'Rp\.', 'Rp', x)
    x = re.sub(r'(?<=\d)[\.](?=\d{3})', r'', x)
    x = re.sub(r'^[\t ]*(?=([^\s]))', r'', x, flags=re.MULTILINE)
    x = re.sub(r'(?<=([sm]))\.(?=(\w{1,3}))', '', x, flags=re.IGNORECASE)
    x = re.sub(r"  +", r" ", x)
    x = re.sub(r'^Halaman.*$', r'', x, flags=(re.MULTILINE | re.IGNORECASE))
    x = re.sub(r"\n\n+", r"\n", x, flags=re.MULTILINE)
    x = re.sub(r'^\n', r'', x)
    return x.lower()

from os import listdir
from os.path import isfile, join

def process_file(fpath):
    with open(join('./rawtext/', fpath), 'r', encoding="utf8") as fin:
        with open(join('./processtexr2/', fpath), 'w', encoding="utf8") as fout:
            intextarr = fin.readlines()
            intext = ''.join(intextarr)
            fout.write(pipeline(intext).encode('utf-8', errors='ignore').decode('utf-8'))

files = [f for f in listdir('./rawtext/') if isfile(join('./rawtext/', f))]

import tqdm
for f in tqdm.tqdm(files):
    process_file(f)
