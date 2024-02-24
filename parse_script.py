import json
import os
import argparse
from tqdm import tqdm
import csv
import re


def parse(input_file, trans_language, audio_format):
    results = []
    with open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    scn_length = len(data['scenes'])
    pattern = re.compile(r'[「」『』（）"]|(\[.*])|(\\n)')
    for i in range(scn_length):
        texts = data['scenes'][i].get('texts')
        if texts:
            for text in texts:
                character = ""

                try:
                    character = text[0] or ""
                except TypeError:
                    pass

                try:
                    sentence_ori = text[2][0][1] or ""
                    sentence_ori = pattern.sub('', sentence_ori)
                    sentence_trans = text[2][trans_language][1] or ""
                    sentence_trans = pattern.sub('', sentence_trans)
                except TypeError:
                    continue

                try:
                    voice = text[3][0].get("voice") or ""
                    if voice:
                        voice += f".{audio_format}"
                except TypeError:
                    voice = ""

                results.append([character, sentence_ori, sentence_trans, voice])
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default=os.getcwd(), help='Path to the input directory.')
    parser.add_argument('-o', '--output', type=str, default=os.path.join(os.getcwd(), "parsed"), help='Path to the output directory.')
    parser.add_argument('-l', '--language', type=int, default=2, help='Language of translation, 0: JP; 1:EN; 2:ZHS; 3:ZHT, default is 2.')
    parser.add_argument('-d', '--delimiter', type=str, default="\t",
                        help='Delimiter of input data file, default is \\t')
    parser.add_argument('-af', '--audio_format', type=str, default="mp3",
                        help='Audio file name suffix, default is mp3')
    parser.add_argument('-s', '--single_file', action='store_true', default=False,
                        help='Merge all text into a single file.')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    if args.single_file:
        results = []
        for f in tqdm(os.listdir(args.input)):
            file = os.path.join(args.input, f)
            if os.path.isfile(f) and (f.split('.')[-1].upper() == "JSON"):
                results += parse(f, args.language, args.audio_format)
        with open(os.path.join(args.output, "all_in_one_parsed.txt"), "w", encoding="utf8", newline="") as tsvfile:
            writer = csv.writer(tsvfile, delimiter=args.delimiter)
            writer.writerows(results)

    else:
        for f in tqdm(os.listdir(args.input)):
            file = os.path.join(args.input, f)
            if os.path.isfile(f) and (f.split('.')[-1].upper() == "JSON"):
                results = parse(f, args.language, args.audio_format)
                with open(os.path.join(args.output, f + "_parsed.txt"), "w", encoding="utf8", newline="") as tsvfile:
                    writer = csv.writer(tsvfile, delimiter=args.delimiter)
                    writer.writerows(results)
