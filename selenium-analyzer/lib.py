import cv2
import numpy as np
import pytesseract
import re
import traceback


pattern_digits = re.compile("(?P<frame>\d+)")
#pattern = re.compile("^.*?(?P<frame>\d*?):.*?(?P<time>[\d:.]*)$")


def extract_frame(i):
    try:
      img = cv2.imread(i)
      img = img[20:40, 40:290]
      candidate = pytesseract.image_to_string(img, config="--psm 7")
      print("Found text:", candidate)
      m = pattern_digits.findall(candidate)
      return int(m[0])
    except:
        return -1
        traceback.print_exc()




def analyze(src, recv):
    s = extract_frame(src)
    r = extract_frame(recv)
    print("SRC:",s, "RECV:", r)
    if s > 0 and r > 0:
        return r - s


if __name__ == "__main__":
  #analyze("/tmp/screenshot-rcv.png")
  analyze("/tmp/selenium_screenshots/rcv-2024-06-26 11:19:41.157275.png")
