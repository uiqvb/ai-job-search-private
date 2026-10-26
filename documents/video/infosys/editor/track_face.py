"""Face track for the rough cut: [t, centre x, centre y, width] every 3 frames (1080x1920), smoothed.
OpenCV Haar (needs OpenCV 4.x). Writes src/face_track.json."""
import cv2, json, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
cap = cv2.VideoCapture(os.path.join(HERE, "public", "th", "track.mp4"))
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
rows, i, last = [], 0, None
while True:
    ok, fr = cap.read()
    if not ok: break
    if i % 3 == 0:
        g = cv2.cvtColor(cv2.resize(fr, (540, 960)), cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, 1.1, 5, minSize=(90, 90))
        if len(f):
            x, y, w, h = max(f, key=lambda r: r[2])
            last = [(x + w / 2) * 2, (y + h / 2) * 2, w * 2]
        if last: rows.append([round(i / 30, 3)] + [round(v, 1) for v in last])
    i += 1
a = np.array(rows)
for c in (1, 2, 3):  # light smoothing
    a[:, c] = np.convolve(np.pad(a[:, c], 2, mode="edge"), np.ones(5) / 5, "valid")
json.dump([[round(v, 2) for v in r] for r in a.tolist()], open(os.path.join(HERE, "src", "face_track.json"), "w"))
print(len(rows), "rows; x range", a[:, 1].min().round(), a[:, 1].max().round(), "y", a[:, 2].min().round(), a[:, 2].max().round(), "w", a[:, 3].min().round(), a[:, 3].max().round())
