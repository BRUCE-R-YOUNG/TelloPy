import time
import cv2
import tellopy

# テロを初期化し、接続します
tello = Tello()
tello.connect()

# 離陸します
tello.takeoff()

time.sleep(5)
# 上昇します
tello.move_up(50)

time.sleep(5)
# 下降します
tello.move_down(50)

time.sleep(5)
# 前方に移動します
tello.move_forward(100)

time.sleep(5)
# 後方に移動します
tello.move_back(100)

time.sleep(5)
# 左に移動します
tello.move_left(100)

time.sleep(5)
# 右に移動します
tello.move_right(100)

time.sleep(5)
# 反時計回りに90度回転します
tello.rotate_counter_clockwise(90)

time.sleep(5)
# 時計回りに90度回転します
tello.rotate_clockwwise(90)

time.sleep(5)
# 後方宙返りを行います
tello.flip_back()

time.sleep(5)
# ストリームを開始し、画像を取得して保存します
tello.streamon()
frame_read = tello.get_frame_read()
cv2.imwrite("picture1.png", frame_read.frame)

time.sleep(5)
# ストリームを再度開始し、画像を取得して保存します
tello.streamon()
frame_read = tello.get_frame_read()
cv2.imwrite("picture2.png", frame_read.frame)

time.sleep(5)
# 着陸します
tello.land()