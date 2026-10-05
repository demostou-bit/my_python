# 実行前にpip install Pillowをターミナルで実行し、Pillowをインストールする
import os
from PIL import Image # PillowからImageモジュールをインポート

# -------------------------------------------------------------------
# 1. ディレクトリ（フォルダ）の準備
# -------------------------------------------------------------------
# スクリプトファイル（split_all.py）が存在する絶対パスを取得
base_dir = os.path.dirname(os.path.abspath(__file__))

# 入力用フォルダ（input）と出力用フォルダ（output）のパスを作成
input_dir = os.path.join(base_dir, "input")
output_dir = os.path.join(base_dir, "output")

# 出力用フォルダが存在しない場合は作成する（存在する場合は何もしない）
os.makedirs(output_dir, exist_ok=True)

# -------------------------------------------------------------------
# 2. 設定値の指定（切り抜き領域の比率・余白サイズ）
# -------------------------------------------------------------------
# 左ページ・右ページのクロップ（切り抜き）領域を割合（0.0〜1.0）で指定
# 形式: (左端の位置, 上端の位置, 右端の位置, 下端の位置) 見切れる個所は第1～第4引数で調節
LEFT_PAGE_CROP = (0.05, 0.04, 0.49, 0.96)   # 上下も含めてコンテンツ部分のみ切り出す
RIGHT_PAGE_CROP = (0.51, 0.04, 0.97, 0.96)

# 画像の周囲に均等に追加する余白（マージン）のサイズ（ピクセル単位） 仕上がりによってはPADDINGも調節
PADDING = 20  # 上下左右に20pxの余白を追加

# -------------------------------------------------------------------
# 3. 余白を追加する関数の定義
# -------------------------------------------------------------------
def add_margin(img, margin, bg_color=(255, 255, 255)):
    """
    画像を指定した背景色（デフォルトは白: 255, 255, 255）で
    上下左右に均等に拡張・余白追加する関数
    """
    # 余白を追加した後の新しい幅と高さを計算
    new_w = img.width + (margin * 2)
    new_h = img.height + (margin * 2)
    
    # 新しいサイズのキャンバス（画像バッファ）を指定の背景色で作成
    new_img = Image.new(img.mode, (new_w, new_h), bg_color)
    
    # 中央（余白分だけずらした位置）に元の画像を貼り付け
    new_img.paste(img, (margin, margin))
    
    return new_img

# -------------------------------------------------------------------
# 4. 画像ファイルのループ処理と分割・保存
# -------------------------------------------------------------------
# inputフォルダ内の全ファイルを1つずつ順に処理
for filename in os.listdir(input_dir):
    # 拡張子が .png, .jpg, .jpeg の画像ファイルのみを対象にする
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        img_path = os.path.join(input_dir, filename)
        
        # 画像ファイルを開く
        with Image.open(img_path) as img:
            # 画像の元の幅(w)と高さ(h)を取得
            w, h = img.size
            
            # 比率（0.0〜1.0）から実際のピクセル座標（整数値）へ変換計算
            # 形式: (left, upper, right, lower)
            left_box = (
                int(w * LEFT_PAGE_CROP[0]), 
                int(h * LEFT_PAGE_CROP[1]), 
                int(w * LEFT_PAGE_CROP[2]), 
                int(h * LEFT_PAGE_CROP[3])
            )
            right_box = (
                int(w * RIGHT_PAGE_CROP[0]), 
                int(h * RIGHT_PAGE_CROP[1]), 
                int(w * RIGHT_PAGE_CROP[2]), 
                int(h * RIGHT_PAGE_CROP[3])
            )
            
            # ① 指定領域で切り抜き (img.crop)
            # ② 周囲に余白を追加 (add_margin)
            left_img = add_margin(img.crop(left_box), PADDING)
            right_img = add_margin(img.crop(right_box), PADDING)
            
            # 元のファイル名から「ファイル名本体」と「拡張子」を取り出す
            name, ext = os.path.splitext(filename)
            
            # 分割後の画像を output フォルダへ保存（例: xxx_left.png / xxx_right.png）
            left_img.save(os.path.join(output_dir, f"{name}_left{ext}"))
            right_img.save(os.path.join(output_dir, f"{name}_right{ext}"))

# -------------------------------------------------------------------
# 5. 完了メッセージを表示
# -------------------------------------------------------------------
print("余白調整を含めた分割処理が完了しました！")