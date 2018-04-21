# -*- coding: utf-8 -*-
# largely from here
# http://russeng.hatenablog.jp/entry/2015/06/16/004704

import numpy
import cv2
# get file name efficiently
from glob import glob
import os

def main():

    square_size = 1.0      # 正方形のサイズ
    pattern_size = (10, 7)  # 模様のサイズ
    pattern_points = numpy.zeros( (numpy.prod(pattern_size), 3), numpy.float32 ) #チェスボード（X,Y,Z）座標の指定 (Z=0)
    pattern_points[:,:2] = numpy.indices(pattern_size).T.reshape(-1, 2)
    pattern_points *= square_size
    obj_points = []
    img_points = []
    images = []
    path = "D:/レポート(2018)/CG応用/images/"

    for fn in os.listdir(path):
        # 画像の取得
        img = cv2.imread(fn, 0)
        #cv2.imshow("test",img)
        images.append(img)
        print ("loading..." + fn)
        cv2.imshow(img)
        # チェスボードのコーナーを検出
        #found, corner = cv2.findChessboardCorners(img, pattern_size)
        # コーナーがあれば
        #if found:
        #    term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
        #    cv2.cornerSubPix(img, corner, (5,5), (-1,-1), term)
        # コーナーがない場合のエラー処理
        #if not found:
        #    print ('chessboard not found')
        #    continue
        #img_points.append(corner.reshape(-1, 2))   #appendメソッド：リストの最後に因数のオブジェクトを追加
        #obj_points.append(pattern_points)
        #corner.reshape(-1, 2) : 検出したコーナーの画像内座標値(x, y)

    # 内部パラメータを計算 rms,CameraMatrix,Distorition,rotate vec,translate vec
    #rms, K, d, r, t = cv2.calibrateCamera(obj_points,img_points,(images[1].shape[1],images[1].shape[0]),None,None)
    # 計算結果を表示
#    print ("RMS = ", rms)
#    print ("K = \n", K)
#    print ("d = ", d.ravel())
    # 計算結果を保存
#    numpy.savetxt("rms.csv", numpy.array([rms]), delimiter =',',fmt="%0.14f")
#    numpy.savetxt("K.csv", K, delimiter =',',fmt="%0.14f")
#    numpy.savetxt("Dist.csv", d, delimiter =',',fmt="%0.14f")

if __name__ == '__main__':
    main()
