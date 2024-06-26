import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

df = pd.read_csv("stats.csv")
df = df.set_index("ts")

# Calculate the actual frame rate 

df = df.reset_index()
first = max(df['rcv'].min(), df['src'].min())
df['rcv'] = df['rcv'] - first
df['src'] = df['src'] - first
df['ts'] = df['ts'] - df['ts'].iloc[0]
df['latency'] = df['src'] - df['rcv']

# Just to be safe. These are probably wrong readings.
df = df[df['latency'] > 0]

#print(df)

df['elapsed_frames_rcv'] = df['rcv'].sub(df['rcv'].shift())
df['elapsed_frames_src'] = df['src'].sub(df['src'].shift())
df['elapsed_time'] = df["ts"].sub(df["ts"].shift())
df['fps_rcv'] = df['elapsed_frames_rcv']  / df['elapsed_time']
df['fps_src'] = df['elapsed_frames_src']  / df['elapsed_time']


# print(df[["fps_rcv","fps_src"]].describe())
avg_framerate = df["fps_src"].mean()
print("Average source frame rate is", avg_framerate)


# Join on the "src/recv" frame count, so that we can calcuate exact time passed.
df_join = pd.merge(df,df,left_on="src", right_on="rcv")

frames_diff = df_join["src_y"] - df_join["rcv_x"]
ts_diff = df_join["ts_y"] - df_join["ts_x"]
print("For", len(frames_diff), "matching frames, the latency was", frames_diff.mean(), "frames = ", ts_diff.mean()*1000, "ms")


# Do a curve fitting, this would predict when a frame would have been generated or received even if we missed it
def poly1d(x,a,b):
    return a + b*x

df = df.dropna()
popts, pcovs = curve_fit(poly1d, df["src"],df["ts"])
print("src = %.2f + %.2f*x" % tuple(popts))
poptr, pcovr = curve_fit(poly1d, df["rcv"],df["ts"])
print("recv = %.2f + %.2f*x" % tuple(poptr))

# Now we can estimate the actual latency (based on the fitting above)
df["predicted_ts_src"] = df["rcv"].apply(lambda x: poly1d(x, *popts))
df["predicted_latency"] = df["ts"] - df["predicted_ts_src"]
print("Predicted latency (via curve fitting):", df["predicted_latency"].mean()*1000, " ms")

# Plot it for test
fig, ax = plt.subplots()
s = df["src"].min()
e = df["src"].max()
frames = list(range(s,e))
ts_p_s = [poly1d(f, *popts) for f in frames]
ts_p_r = [poly1d(f, *poptr) for f in frames]
ax.plot(frames, ts_p_s, label="predicted src")
ax.plot(frames, ts_p_r, label="predicted recv")
#ax.plot(df["rcv"], df["ts"], label="actual recv")
ax.plot(df["src"], df["ts"], label="actual src")
ax.set_xlabel("Frame #")
ax.set_ylabel("Timestamp")


ax.legend()
fig.savefig("test.png")
