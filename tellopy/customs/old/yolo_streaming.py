# YOLO物体追跡 + ストリーミング表示

import time
import cv2
from djitellopy import Tello
import numpy as np
from ultralytics import YOLO  # YOLOv8を使用

# Telloを初期化して接続
tello = Tello()
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
        
        # フレームをリサイズ (パフォーマンス向上)
        frame_resized = cv2.resize(frame, (640, 480))  # YOLOモデルの入力サイズに合わせて調整

        # YOLOで物体検出
        results = model(frame_resized)

        # 最初の検出結果を取得
        detections = results[0].boxes.data.numpy() if results else []

        # バウンディングボックスとラベルの描画
        for det in detections:
            x1, y1, x2, y2, conf, cls = det
            label = int(cls)

            if conf > 0.5:  # 信頼度が閾値を超える場合
                # バウンディングボックス描画
                cv2.rectangle(frame_resized, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame_resized, f"Class: {label} ({conf:.2f})", 
                            (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # ストリーミングビューを表示
        cv2.imshow("Tello YOLO Tracking", frame_resized)

        # キー操作で終了 (例: "q"で終了)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("処理を中断しました。")

finally:
    # 着陸してストリームを停止
    tello.land()
    tello.streamoff()
    cv2.destroyAllWindows()
