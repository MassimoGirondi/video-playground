from selenium import webdriver
import time
from lib import *
import datetime as dt
import argparse
import os
import sys, signal
import glob
import pandas as pd
from tqdm import tqdm

def run(args):
    stats = []

    driver = webdriver.Firefox()
    driver.get(args.url)

    driver.find_element('id','start').click()
    print("Select your camera in the browser, and press enter!")
    input()

    src =  driver.find_element('id','video-src')
    rcv =  driver.find_element('id','video')

    os.makedirs(args.output, exist_ok=True)


    def signal_handler(signal, frame):
        if not args.no_analysis:
            print("\n\n Saving stats: got", len(stats), "metrics")
            df = pd.DataFrame(stats)
            df.columns = ["ts", "src", "rcv"]
            df.to_csv(args.output_csv, index=False)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    print("Starting to take screenshots... Stop with CTRL+C")

    while True:
        now = dt.datetime.now()
        now_iso = now.isoformat()
        now_ts = now.timestamp()
        src_file = f'{args.output}/src-{now_ts}.png'
        rcv_file = f'{args.output}/rcv-{now_ts}.png'
        src.screenshot(src_file)
        rcv.screenshot(rcv_file)
        if not args.no_analysis:
            s = extract_frame(src_file)
            r = extract_frame(rcv_file)
            stats.append([now_ts, s, r])
        print("Took another screenshot!")

        print("Screenshotting took", dt.datetime.now() - now)
        time.sleep(int(args.interval)/1000)


def analysis(args):
    files_src = glob.glob(args.output+"/src*.png")
    files_rcv = glob.glob(args.output+"/rcv*.png")
    files_src.sort()
    files_rcv.sort()

    # Check that we read only matching files
    src_ts = set([re.sub(r'(.*?)-(.*?).png$', r'\2', f) for f in files_src])
    rcv_ts = set([re.sub(r'(.*?)-(.*?).png$', r'\2', f) for f in files_rcv])
    matching = src_ts.intersection(rcv_ts)
    print("src has", len(src_ts), "rcv has", len(rcv_ts))
    print("Matching: ", len(matching))
    files_src = list(filter( lambda f: re.sub(r'(.*?)-(.*?).png$', r'\2', f) in matching, files_src))
    files_rcv = list(filter( lambda f: re.sub(r'(.*?)-(.*?).png$', r'\2', f) in matching, files_rcv))
    print("After curing, src has", len(files_src), "rcv has", len(files_rcv))
    # Just to be sure
    files_src.sort()
    files_rcv.sort()
    ts = list(matching)
    ts.sort()

    stats = []
    for t,s,r in zip(ts,files_src, files_rcv):
        s = extract_frame(s)
        r = extract_frame(r)
        stats.append([t, s, r])
        if len(stats) > 100:
            break

    print("Saving stats: got", len(stats), "metrics")
    df = pd.DataFrame(stats)
    df.columns = ["ts", "src", "rcv"]
    df.to_csv(args.output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video stream from the command line")
    parser.add_argument("--url", help="The webpage URL", default ="https://localhost:8080")
    parser.add_argument("--output", help="Output path to save the screenshots", default ="/tmp/selenium_screenshots")
    parser.add_argument("--output-csv", help="Output file for csv stats", default ="./stats.csv")
    parser.add_argument("--interval", help="Waiting time between screenshots, in ms", default = 500)
    #parser.add_argument("--insecure", help="Accept broken HTTPS", action="count")
    parser.add_argument("--no-analysis", help="Do not analyse screenshots, just save them", action="store_true")
    parser.add_argument("--analysis-only", help="Read screenshots already saved, don't take them", action="store_true")

    args = parser.parse_args()
    if args.analysis_only:
        analysis(args)
    else:
        run(args)
