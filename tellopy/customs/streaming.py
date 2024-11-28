import cv2
from djitellopy import Tello

# Telloを初期化して接続
tello = Tello()
tello.connect()

# ストリーミングを開始
tello.streamon()

# カメラフレームを取得して表示
try:
    while True:
        # フレームを取得
        frame = tello.get_frame_read().frame
        
        # フレームをリサイズ (例: 640x480)
        frame_resized = cv2.resize(frame, (640, 480))
        
        # フレームを表示
        cv2.imshow("Tello Stream", frame_resized)
        
        # "q"キーで終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    print("処理を中断しました。")
finally:
    # ストリーミングを停止して終了
    tello.streamoff()
    cv2.destroyAllWindows()