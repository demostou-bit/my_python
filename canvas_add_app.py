# お絵描きアプリ
import tkinter as tk
from tkinter import colorchooser

class Oekaki(tk.Frame):
  def __init__(self, master=None):
    super().__init__(master)
    self.pack()

    # キャンバスサイズ
    self.canvas_width = 900
    self.canvas_height = 500

    # 線の色
    self.color = "black"
    # 線幅
    self.line_width = 3

    # マウスの位置
    self.px = 0
    self.py = 0
    # 最後に書いた線
    self.last_line = []
    # 全ての線
    self.all_lines = []
    # ツールバー
    self.create_toolbar()

    # キャンバス
    self.canvas = tk.Canvas(
      self, width=self.canvas_width, height=self.canvas_height, bg="white")
    self.canvas.pack()
    self.canvas.bind("<ButtonPress-1>", self.button_pressed)
    self.canvas.bind("<B1-Motion>", self.mouse_moved)
    self.canvas.bind("<ButtonRelease-1>", self.button_up)

  # ツールバーにウィジットを配置する
  def create_toolbar(self):
    # ツールバーを表示するフレーム
    self.toolbar = tk.Frame(self)
    self.toolbar.pack()
    # 線の色を選択するRadiobutton
    self.color_sel = tk.StringVar()
    self.color_sel.set(self.color)

    # 変更点1：色選択ボタンの追加
    color_btn = tk.Button(self.toolbar, text="色選択", command=self.choose_color)
    color_btn.pack(side=tk.LEFT)
    # ------------------------------------

    # 既存のRadiobutton類
    black = tk.Radiobutton(self.toolbar, text="黒 ",
                                    variable=self.color_sel, value="black")
    black.pack(side=tk.LEFT)
    red = tk.Radiobutton(self.toolbar, text="赤 ",
                                  variable=self.color_sel, value="red")
    red.pack(side=tk.LEFT)
    green = tk.Radiobutton(self.toolbar, text="緑 ",
                                    variable=self.color_sel, value="green")
    green.pack(side=tk.LEFT)
    yellow = tk.Radiobutton(self.toolbar, text="黄 ",
                              variable=self.color_sel, value="yellow")
    yellow.pack(side=tk.LEFT)

    # 線幅を設定するOptionMenu
    self.line_var = tk.IntVar()
    self.line_var.set(self.line_width)
    line_ws = (1, 2, 3, 4, 5, 6, 7, 8)
    line_menu = tk.OptionMenu(self.toolbar, self.line_var, *line_ws)
    line_menu.pack(side=tk.LEFT)

    # 取り消しボタン
    undo_btn = tk.Button(self.toolbar, text="取り消し",
                          command=self.undo)
    undo_btn.pack(side=tk.LEFT, padx=5)

    # 変更点2：すべて削除ボタンの追加
    clear_btn = tk.Button(self.toolbar, text="すべて削除", command=self.clear_canvas)
    clear_btn.pack(side=tk.LEFT, padx=5)
    # ---------------------------
  
  # 追加メソッド1：色選択ダイアログ
  def choose_color(self):
    color = colorchooser.askcolor(title="色を選択してください")
    if color[1]: # 色が選択された場合のみ更新
      # 戻り値の16進数カラーコード（color[1]）をself.color_selに適用
      self.color_sel.set(color[1])

  # 追加メソッド2：キャンバス全削除
  def clear_canvas(self):
    self.canvas.delete("all")
    self.all_lines = []
  # ----------------------------

  # マウスボタンが押された
  def button_pressed(self, event):
    self.px = event.x
    self.py = event.y
    # 線の色
    self.color = self.color_sel.get()
    # 線幅
    self.line_width = self.line_var.get()

  # マウスが動いた
  def mouse_moved(self, event):
    x = event.x
    y = event.y
    id = self.canvas.create_line(self.px, self.py, x, y,
                                  fill=self.color, width=self.line_width)
    self.px = x
    self.py = y
    self.last_line.append(id)

  # ボタンが放された
  def button_up(self, event):
    self.all_lines.append(self.last_line)
    self.last_line = []
  
  # 最後に書いた線を取り消す
  def undo(self):
    if len(self.all_lines) > 0:
      last = self.all_lines.pop()
      for l in last:
        self.canvas.delete(l)

if __name__ == '__main__':
  root = tk.Tk()
  # フォントサイズは30だとツールバーに収まらないため12に変更
  root.option_add("*font", "Courier 12")
  root.title("お絵描きアプリ")
  Oekaki(master=root)
  root.mainloop()

