import cv2
import numpy as np
from djitellopy import Tello
from ultralytics import YOLO

# Telloドローンを初期化
tello = Tello()

def main():
    try:
        # ドローンに接続
        print("Telloに接続中...")
        tello.connect()
        print(f"バッテリー: {tello.get_battery()}%")
        
        # ストリーミングを開始
        print("ストリーミングを開始します...")
        tello.streamon()

        # YOLOモデルをロード
        print("YOLOモデルをロードします...")
        model = YOLO("yolov8n.pt")  # 必要に応じて大きなモデルを使用

        # 離陸
        print("離陸します...")
        tello.takeoff()

        while True:
            # フレームを取得
            frame = tello.get_frame_read().frame
            
            # フレームがNoneの場合スキップ
            if frame is None:
                continue
            
            # フレームをリサイズ (例: 640x480)
            frame_resized = cv2.resize(frame, (640, 480))
            
            # YOLOモデルで物体検出
            results = model(frame_resized)
            detections = results[0].boxes.data.numpy() if results else []

            # 検出結果を描画
            for det in detections:
                x1, y1, x2, y2, conf, cls = det
                label = int(cls)
                if conf > 0.5:  # 信頼度が閾値を超える場合
                    # バウンディングボックス描画
                    cv2.rectangle(frame_resized, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(frame_resized, f"Class: {label} ({conf:.2f})", 
                                (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # フレームを表示
            cv2.imshow("Tello YOLO Tracking", frame_resized)

            # "q"キーで終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    finally:
        # 着陸とストリームの終了
        print("ドローンを着陸させます...")
        tello.land()
        tello.streamoff()
        cv2.destroyAllWindows()
        print("終了しました。")

if __name__ == "__main__":
    main()
