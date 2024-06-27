
import os
import sys
import inspect
import datetime as dt
import pyverbs


currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils
import empty_model

times = {}
processed_frames = 0

def create_model(model_name="mosaic"):
    def reset_times():
        global times, processed_frames
        times["preprocessing"] = []
        times["model"] = []
        times["postprocessing"] = []
        processed_frames = 0

    def print_times():
        global times, processed_frames
        pre = [t.seconds*1e6+t.microseconds for t in times["preprocessing"]] 
        model= [t.seconds*1e6+t.microseconds for t in times["model"]] 
        post= [t.seconds*1e6+t.microseconds for t in times["postprocessing"]] 

        print("  PRE:", sum(pre) / processed_frames, "us")
        print("  MODEL:", sum(model) / processed_frames, "us")
        print("  POST:", sum(post) / processed_frames, "us")

    reset_times()

    def call(frame):
        global times, processed_frames


        processed_frames+=1
        if processed_frames > 300 :
            print_times()
            reset_times()



        return f

    return call


