# WebRTC server

This is a demo of WebRTC streaming and latency measurement.






# Profiling

Running "dummy" model would copy the frames to the GPU, and back to the CPU, similarly to pre/post processing of a torch model.
This can then be profiled with `cProfile`:
  python3 -m cProfile -o ./profile server.py --cert-file cert.pem --key cert.key

And read with snakeviz:
  snakeviz -H 192.168.3.27 -s ./profile

Without much optimization, the `preprocessing` function takes a comulative time of 11 ms per call, and `postprocessing` 14ms. This is out of 200 frames with a FullHD stream.

For post processing, the type conversion is the most expensive operation.

In general, such workload (without profiling) uses around 10 cores (nslrack27+T4).

# Source

Code from https://github.com/aiortc/aiortc/blob/main/examples/server/server.py

transformers: https://blog.mozilla.org/webrtc/end-to-end-encrypt-webrtc-in-all-browsers/
