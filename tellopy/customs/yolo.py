#pip install djitellopy opencv-python ultralytics numpy

import time
import cv2
import tellopy
import numpy as np
from ultralytics import YOLO  # YOLOv8を使用

# Telloを初期化して接続
tello = tellopy.Tello()
tello.connect()

# ストリーミングを開始
tello.streamon()
frame_read = tello.get_frame_read()

# YOLOv8モデルをロード
model = YOLO("yolov8n.pt")  # 必要に応じて大きなモデルに変更可能

# 離陸
tello.takeoff()

try:
    while True:
        # カメラフレームを取得
        frame = frame_read.frame
        frame_resized = cv2.resize(frame, (640, 480))  # YOLOモデルの入力サイズに合わせて調整

        # YOLOで物体検出
        results = model(frame_resized)

        # 最初の検出結果を取得
        detections = results[0].boxes.data.numpy() if results else []

        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            label = int(cls)

            # 信頼度が高い場合に描画
            if conf > 0.5:
                # バウンディングボックスを描画
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"Class: {label}", (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Telloの制御ロジック
                box_center_x = (x1 + x2) / 2
                frame_center_x = frame_resized.shape[1] / 2

                if box_center_x < frame_center_x - 50:
                    tello.move_left(20)
                elif box_center_x > frame_center_x + 50:
                    tello.move_right(20)
                else:
                    tello.move_forward(20)

        # フレームを表示
        cv2.imshow("Tello YOLO Tracking", frame)

        # "q"キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("処理を中断しました。")

finally:
    # 着陸してクリーンアップ
    tello.land()
    tello.streamoff()
    cv2.destroyAllWindows()
