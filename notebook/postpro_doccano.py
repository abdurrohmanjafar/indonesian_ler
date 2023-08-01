import re
import json
import spacy
from spacy import attrs
from spacy.training import offsets_to_biluo_tags
from spacy.tokenizer import Tokenizer
import tqdm

nlp = spacy.load('en_core_web_sm')
nlp.tokenizer = Tokenizer(nlp.vocab, token_match=re.compile(r'\S+').match)


def process_name(name):
    num_lines = sum(1 for line in open(f'annotated_data/{name}.jsonl', encoding="utf8"))
    with open(f'annotated_data/{name}.jsonl', 'r', encoding="utf8") as f:
        with open(f'annotated_data/{name}.res.json', 'w') as o:
            with open(f'annotated_data/{name}.meta.json', 'w') as m:
                for line in tqdm.tqdm(f, total=num_lines):
                    data = json.loads(line)
                    out = {
                        "verdict": "guilty",
                        "indictment": "NA",
                        "lawyer": False,
                        "id": data["id"],
                        "owner": name
                    }

                    indict_text = ""

                    data['text'] = data['text'].replace('\n', " ")
                    data['new-label'] = []

                    for label in data['label']:
                        tagged_word = data["text"]
                        start_index = label[0]
                        end_index = label[1]
                        len_text = len(tagged_word)

                        if tagged_word[start_index] == " ":
                            while tagged_word[start_index] == " ":
                                start_index += 1

                        elif tagged_word[start_index - 1] != " ":
                            while tagged_word[start_index - 1] != " "\
                                    and start_index != 0:
                                start_index -= 1

                        if tagged_word[end_index - 1] == " ":
                            while tagged_word[end_index - 1] == " ":
                                end_index -= 1

                        elif tagged_word[end_index] != " ":
                            while tagged_word[end_index] != " "\
                                    and end_index != len_text:
                                end_index += 1

                        data['new-label'].append((start_index, end_index, label[2]))

                        if label[2] == "Jenis Amar":
                            substr: str = tagged_word[start_index:end_index]
                            if "bebas" in substr:
                                out['verdict'] = "bebas"
                            elif "lepas" in substr:
                                out['verdict'] = "lepas"

                        if label[2] == "Nama Pengacara":
                            out['lawyer'] = True

                        if label[2] == "Jenis Dakwaan":
                            substr: str = tagged_word[start_index:end_index]
                            substr = "".join(substr.split(" "))
                            indict_text += substr + "|"
                            if "tunggal" in substr:
                                out['indictment'] = "tunggal"
                            elif "subsi" in substr:
                                out['indictment'] = "subsider"
                            elif "komul" in substr or "kumul" in substr:
                                out['indictment'] = "komul"
                            elif "alter" in substr:
                                out['indictment'] = "alternatif"
                            elif "kombin" in substr:
                                out['indictment'] = "kombinasi"
                            elif "gabung" in substr:
                                out['indictment'] = "gabungan"

                    doc = nlp(data['text'])

                    tags = offsets_to_biluo_tags(doc, data['new-label'])
                    for x in range(0, len(tags)):
                        tag = tags[x]
                        if tag[0] == "L":
                            tag = tag.replace("L-", "I-")
                        if tag[0] == "U":
                            tag = tag.replace("U-", "B-")

                        tags[x] = tag

                    if out["indictment"] == "NA" and len(indict_text) > 0:
                        out["indictment"] = f"NF - {indict_text}"

                    data_json = json.dumps(out)
                    m.write(data_json + '\n')

                    out['text-tags'] = tags
                    out['text'] = [x.text for x in nlp.tokenizer(data['text'])]

                    data_json = json.dumps(out)
                    o.write(data_json + '\n')


process_name('agree')
process_name('dhipa')
process_name('jafar')
process_name('fariz')
