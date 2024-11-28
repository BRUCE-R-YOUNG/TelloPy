import time
import tellopy
import pygame
import cv2
import numpy as np
from ultralytics import YOLO

# YOLOモデルをロード
model = YOLO("yolov8n.pt")  # 必要に応じてモデルを変更可能

def videoFrameHandler(event, sender, data):
    """
    Telloから受信したフレームをYOLOで処理し、物体検出を行う。
    """
    global video_surface
    global drone

    # OpenCVフレームに変換
    np_frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)

    # YOLOで物体検出
    results = model(frame)
    detections = results[0].boxes.data.numpy() if results else []

    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        label = int(cls)
        if conf > 0.5:
            # バウンディングボックスとラベルの描画
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"Class: {label}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # フレームをPygameウィンドウに描画
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    video_surface.blit(frame, (0, 0))
    pygame.display.update()

def main():
    pygame.init()
    pygame.display.init()

    # Pygameウィンドウの設定
    global video_surface
    video_surface = pygame.display.set_mode((960, 720))

    # ドローンの初期化と接続
    global drone
    drone = tellopy.Tello()
    drone.connect()
    drone.start_video()
    drone.subscribe(drone.EVENT_VIDEO_FRAME, videoFrameHandler)

    try:
        print("離陸します")
        drone.takeoff()
        time.sleep(5)  # 安定するまで待機

        while True:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    key = pygame.key.name(e.key)
                    if key == "escape":
                        print("終了します")
                        drone.land()
                        drone.quit()
                        pygame.quit()
                        return
                elif e.type == pygame.QUIT:
                    print("終了します")
                    drone.land()
                    drone.quit()
                    pygame.quit()
                    return

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")
    finally:
        print("ドローンを停止します")
        drone.land()
        drone.quit()
        pygame.quit()

if __name__ == "__main__":
    main()
