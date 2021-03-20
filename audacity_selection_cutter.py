import glob
import re
import xml.etree.ElementTree as ET
import argparse
import os
import subprocess

def parse_aup(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    parsed = dict()

    sel0 = root.attrib['sel0']
    sel0 = sel0.split(".")
    sel0 = int(sel0[0]) * 1000 + int(sel0[1][:3])
    sel1 = root.attrib['sel1']
    sel1 = sel1.split(".")
    sel1 = int(sel1[0]) * 1000 + int(sel1[1][:3])
    duration = sel1 - sel0

    ss = ".".join([str(sel0//1000), str(sel0%1000)])
    t = ".".join([str(duration//1000), str(duration%1000)])

    parsed["ss"] = ss
    parsed["t"] = t
    parsed["file"] = root[1].attrib["name"]

    return parsed

def run_for_all_files(extension, input_folder, output_folder):
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    os.chdir(input_folder)
    for file in glob.glob("*.aup"):
        parsed = parse_aup(file)
        input_file = f'{input_folder}/{parsed["file"]}.{extension}'
        output_file = f'{output_folder}/{parsed["file"]}-cut.{extension}'
        command = f'ffmpeg -ss {parsed["ss"]} -t {parsed["t"]} -i "{input_file}" -acodec copy "{output_file}"'
        print(command, end="\n\n")
        subprocess.call(command, shell=True)

def main():
    parser = argparse.ArgumentParser(
            description='Audicity selection cutter. For all audicity projects in current directory cuts audio files by audacity selection. \
                Audio file must be in the same directory with filename as in project. Requires extension as its not saved anywhere. \
                But why do I even need it??? - you say. \
                Well Im glad you asked. The thing is I want to cut those files without recoding them (and possibly lose quality) with nice GUI. \
                And it was simpler to write stupid script than look for proper program online so...                      \
                Also this way tags are also copied :).                 \
                Basically runs:     \
                ffmpeg -ss SELECTIONS_START -t SELECTION_DURATION -i FILENAME.EXTENSION -acodec copy FILENAME-cut.EXTENSION '
        )

    parser.add_argument('extension', type=str, help='Audio files extension')
    parser.add_argument('--input-folder', type=str, help='Folder where to look for .aup and audio files', default=".")
    parser.add_argument('--output-folder', type=str, help='Folder where save all cutted audio files', default=".")
    args = parser.parse_args()

    run_for_all_files(args.extension, args.input_folder, args.output_folder)

if __name__ == "__main__":
    main()
