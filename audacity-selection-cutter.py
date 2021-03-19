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

def run_for_all_files(extension):
    os.chdir(".")
    for file in glob.glob("*.aup"):
        parsed = parse_aup(file)
        command = f'ffmpeg -ss {parsed["ss"]} -t {parsed["t"]} -i "{parsed["file"] + "." + extension}" -acodec copy "{parsed["file"] + "-cut" + "." + extension}"'
        print(command)
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
    args = parser.parse_args()

    run_for_all_files(args.extension)

if __name__ == "__main__":
    main()
