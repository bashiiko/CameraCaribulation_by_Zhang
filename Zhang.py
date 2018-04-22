# -*- coding: utf-8 -*-
# largely from here
# http://russeng.hatenablog.jp/entry/2015/06/16/004704
# (caution) Japanese path fails!

import numpy
import cv2
# get file name efficiently
import os

def main():

    # 現在のスクリプトのフォルダの絶対パス取得
    base = os.path.dirname(os.path.abspath(__file__)).replace("\\","/")
    # チェスボード画像を格納するフォルダ
    train_path = base + "/trainimages/"
    # 歪み修正用画像，修正後の画像を保存するフォルダ
    test_path = base + "/resultimages/"

    # 歪み修正をする画像ファイル名
    no_dist_img = "chess_16.jpg"

    square_size = 1.0      # 正方形のサイズ
    pattern_size = (10, 7)  # 模様のサイズ
    pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []

    for fn in os.listdir(train_path):
        img = cv2.imread(train_path + fn, 0)
        print ("loading..." + fn)
        # チェスボードのコーナーを検出
        found, corner = cv2.findChessboardCorners(img, pattern_size)
        # コーナーがあれば
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corner, (5,5), (-1,-1), term)
        # コーナーがない場合のエラー処理
        if not found:
            print ('chessboard not found')
            continue
        img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        obj_points.append(pattern_points)
        #corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)

    # 内部パラメータを計算 rms,CameraMatrix,Distorition,rotate vec,translate vec
    rms, K, d, r, t = cv2.calibrateCamera(obj_points,img_points,(img.shape[1],img.shape[0]),None,None)
    # 計算結果を表示
    print ("RMS = ", rms)
    print ("CameraMatrix = \n", K)
    print ("Distortion = ", d.ravel())
    print ("rotate vec = \n", r)
    print ("translate vec = \n", t)
    # 計算結果を保存
    numpy.savetxt("rms.csv", numpy.array([rms]), delimiter =',',fmt="%0.14f")
    numpy.savetxt("K.csv", K, delimiter =',',fmt="%0.14f")
    numpy.savetxt("Dist.csv", d, delimiter =',',fmt="%0.14f")

    # カメラパラメータの修正
    img = cv2.imread(test_path+no_dist_img)
    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(K,d,(w,h),1,(w,h))

    # undistort
    dst = cv2.undistort(img, K, d, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(test_path+'calibresult.jpg',dst)

if __name__ == '__main__':
    main()
