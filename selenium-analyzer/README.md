This is a "simple" latency measurement toolkit.

It would launch a Firefox window, connect to the webserver, and ask for camera permissions.
Once that is done, press "Enter" in the terminal, the script would take a screenshot to the video every 500ms, and analyze the time difference between them.
You may want to use `--no-analysis` and  `--analysis-only` to not affect the screenshot interval (which is likely < 10 fps).

`report.py` would read the csv file and calculate the latency



