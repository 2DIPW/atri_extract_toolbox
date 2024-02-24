import os
import subprocess
import threading
import argparse
from tqdm import tqdm


def convert(input_file, output_dir, format):
    output_file = os.path.join(output_dir, os.path.splitext(input_file)[0] + '.' + format)
    subprocess.call(['ffmpeg', '-i', input_file, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    max_threads.release()


def batch_convert(input_files, output_dir, format):
    threads = []
    for input_file in tqdm(input_files):
        max_threads.acquire()

        thread = threading.Thread(target=convert_to_mp3, args=(input_file, output_dir, format))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, default=os.getcwd(), help='Path to the input directory.')
    parser.add_argument('-o', '--output', type=str, default=os.path.join(os.getcwd(), "converted"), help='Path to the output directory.')
    parser.add_argument('-f', '--format', type=str, default='mp3', help='Format you want to convert to.')
    parser.add_argument('-t', '--thread', type=int, default=16, help='How many files to be processed at the same time.')
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    max_threads = threading.Semaphore(args.thread)

    input_files = []
    for f in os.listdir(args.input):
        file = os.path.join(args.input, f)
        if os.path.isfile(f) and (f.split('.')[-1].upper() in ["OPUS", "OGG"]):
            input_files.append(f)

    batch_convert(input_files, args.output, args.format)
