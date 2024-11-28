"""
必要なライブラリのインストール

1.djitellopy:
pip install djitellopy

2.ultralytics（YOLOv8）:
pip install ultralytics

3.OpenCV:
pip install opencv-python

"""

import cv2
from djitellopy import Tello
from ultralytics import YOLO

# YOLOv8モデルをロード（例: yolov8n.pt）
model = YOLO("yolov8n.pt")  # 必要に応じて他のモデルを指定

# Telloを初期化して接続
tello = Tello()
tello.connect()

# ストリーミングを開始
tello.streamon()

# キー操作の説明を表示
print("操作方法:")
print("t: 離陸, l: 着陸")
print("w: 前進, s: 後退")
print("a: 左旋回, d: 右旋回")
print("u: 上昇, j: 降下")
print("q: 終了")

# カメラフレームを取得して表示
try:
    while True:
        # フレームを取得
        frame = tello.get_frame_read().frame
        
        # BGRからRGBに変換（青っぽくなる問題を修正）
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # フレームをリサイズ (例: 640x480)
        frame_resized = cv2.resize(frame_rgb, (640, 480))
        
        # YOLOv8で物体検出
        results = model(frame_resized)
        annotated_frame = results[0].plot()  # 検出結果を描画
        
        # 検出された物体情報を出力
        for result in results[0].boxes.data:
            cls = result[5].item()  # クラスID
            conf = result[4].item()  # 信頼度
            print(f"検出: クラスID={cls}, 信頼度={conf:.2f}")
        
        # フレームを表示
        cv2.imshow("Tello Stream with YOLOv8", annotated_frame)
        
        # キー入力を取得
        key = cv2.waitKey(1) & 0xFF
        
        # "t"キーで離陸
        if key == ord('t'):
            print("離陸します...")
            tello.takeoff()
        
        # "l"キーで着陸
        elif key == ord('l'):
            print("着陸します...")
            tello.land()

        # "w"キーで前進
        elif key == ord('w'):
            print("前進します...")
            tello.move_forward(30)  # 単位: cm

        # "s"キーで後退
        elif key == ord('s'):
            print("後退します...")
            tello.move_back(30)

        # "a"キーで左旋回
        elif key == ord('a'):
            print("左旋回します...")
            tello.rotate_counter_clockwise(30)  # 単位: 度

        # "d"キーで右旋回
        elif key == ord('d'):
            print("右旋回します...")
            tello.rotate_clockwise(30)

        # "u"キーで上昇
        elif key == ord('u'):
            print("上昇します...")
            tello.move_up(30)

        # "j"キーで降下
        elif key == ord('j'):
            print("降下します...")
            tello.move_down(30)

        # "q"キーで終了
        elif key == ord('q'):
            print("終了します...")
            break
except KeyboardInterrupt:
    print("処理を中断しました。")
finally:
    # ストリーミングを停止して終了
    tello.streamoff()
    cv2.destroyAllWindows()
