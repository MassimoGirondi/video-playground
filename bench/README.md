This is a benchmark to see how "slow" is a generic backend.

This would call the same "transformer" that is called in the WebRTC server, and then measures the FPS and how much time it takes to process every frame, from the "application" perspective.
We could consider as an "application" the actual backend server, so the time the actual webrtc socket (i.e. the Python process) experiences when processing each single frame. 

