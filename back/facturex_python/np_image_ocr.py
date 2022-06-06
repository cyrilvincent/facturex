import cv2
import time
import argparse
import keras_ocr

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class NpImageOcr:
    pipeline = keras_ocr.pipeline.Pipeline()

    def predict(self, path):
        try:
            images = [keras_ocr.tools.read(url) for url in [path]]
            prediction_groups = NpImageOcr.pipeline.recognize(images)
            res = [p[0] for p in prediction_groups[0]]
            return list(dict.fromkeys(res))
        except Exception as ex:
            print(f"Warning: OCR {ex}")
            return []

    def predict_string(self, path, limit=10, min=3):
        res = self.predict(path)
        s = ""
        for r in res[:limit]:
            if len(r) >= min:
                s = s + " " + r
        s = s.strip()
        if len(s) == 0:
            return None
        return s

# capture_csv.png 0.035s
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="OCR reader")
    # parser.add_argument("path", help="Image path")
    args = parser.parse_args()
    np = NpImageOcr()
    t = time.perf_counter()
    res = np.predict("capture_csv.png") #args.path)
    print(res)
    print(" ".join(res))
    print(f"Found in {time.perf_counter() - t:.1f}s")
