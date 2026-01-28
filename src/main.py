import pyxel      

class Player:
    # Playerの初期化
    def __init__(self, x, y):
        # 初期位置
        self.player_pos = [x, y]
        self.w = 16
        self.h = 16
        # 移動不可なタイルの一覧
        self.movable_tiles_one = [(2, 0), (2, 1), (4, 0), (5, 0), (4, 1), (5, 1), (3, 1)]
        self.movable_tiles_two = [(6, 2), (2, 0)]
        # 下り階段
        self.target_tiles_down = [(2, 2), (2, 3), (3, 2), (3, 3)]
        # 上り階段
        self.target_tiles_up = [(2, 6), (3, 6), (2, 7), (3, 7)]

        # 鍵を取得数
        self.key_count = 0

        # 速度
        self.speed = 2

    def move_check(self, x, y, mapmode, map_x):
        # 移動不可なタイルは移動できないように判定
        tile_x = (x + map_x) // 8
        tile_y = y // 8

        tile = pyxel.tilemaps[0].pget(tile_x, tile_y)

        if mapmode == "stage_one":
            return tile not in self.movable_tiles_one
        elif mapmode == "stage_two":
            return tile not in self.movable_tiles_two    
    
    def on_target_tile_one(self, map_x):
        # 下り階段の判定
        tile_x = (self.player_pos[0] + map_x) // 8
        tile_y = self.player_pos[1] // 8
        return pyxel.tilemaps[0].pget(tile_x, tile_y) in self.target_tiles_down
    
    def on_target_tile_two(self, map_x):
        # 上り階段の判定
        tile_x = (self.player_pos[0] + map_x) // 8
        tile_y = self.player_pos[1] // 8
        return pyxel.tilemaps[0].pget(tile_x, tile_y) in self.target_tiles_up

    def update(self, mapmode, map_x):
        # 移動
        if pyxel.btn(pyxel.KEY_RIGHT):
            if self.move_check(self.player_pos[0]+16, self.player_pos[1], mapmode, map_x):
                self.player_pos[0] += self.speed
            
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.move_check(self.player_pos[0]-4, self.player_pos[1], mapmode, map_x):
                self.player_pos[0] -= self.speed

        elif pyxel.btn(pyxel.KEY_UP):
            if self.move_check(self.player_pos[0], self.player_pos[1]-4, mapmode, map_x):
                self.player_pos[1] -= self.speed

        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.move_check(self.player_pos[0], self.player_pos[1]+16, mapmode, map_x):
                self.player_pos[1] += self.speed

    def draw(self):
            pyxel.blt(self.player_pos[0] , self.player_pos[1] , 0, 0, 48, self.w, self.h, 13)

class Key:
    # Keyの初期化
    def __init__(self, x, y):
        # 初期位置
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.taken = False

    def draw(self):
        if not self.taken:
            pyxel.blt(self.x, self.y, 0, 48, 24, self.w, self.h, 13)

class Box:
    # Boxの初期化
    def __init__(self, x, y):
        # 初期位置
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16

    def draw(self):
            pyxel.blt(self.x, self.y, 0, 32, 32, self.w, self.h, 13)

class FakeBox:
    # FakeBoxの初期化
    def __init__(self, x, y):
        # 初期位置
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16

    def draw(self):
            pyxel.blt(self.x, self.y, 0, 32, 48, self.w, self.h, 13)

class App:
    def __init__(self):
        pyxel.init(256, 224, title="RPG")

        pyxel.load("../assets/my_resource.pyxres")

        # ビットマップフォントの読み込み
        self.font = pyxel.Font("umplus_j10r.bdf")

        # 初期モード
        self.state = "start"

        self.player = Player(8, 32)

        self.key = Key(8, 8)
        self.box = Box(8, 200)
        self.fake_box = FakeBox(8, 136)

        self.mapmode = "stage_one"
        self.map_x = 0
        self.map_y = 0

        self.on_stairs = False

        pyxel.run(self.update, self.draw)

    def reset_game(self):
        # ゲームを初期状態に戻す
        self.state = "start"
        self.player = Player(8, 32)
    
        self.key = Key(8, 8)

        self.mapmode = "stage_one"
        self.map_x = 0
        self.map_y = 0

        self.on_stairs = False

    def check_collision(self, a, b):
        """矩形同士の当たり判定"""
        return (
            a.player_pos[0] < b.x + b.w and
            a.player_pos[0] + a.w > b.x and
            a.player_pos[1] < b.y + b.h and
            a.player_pos[1] + a.h > b.y
        )

    def update(self):
        mx = pyxel.mouse_x
        my = pyxel.mouse_y

        # --- スタート画面 ---
        if self.state == "start":
            # マウスカーソルを表示する
            pyxel.mouse(True)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # はじめる
                if 30 <= mx <= 68 and 80 <= my <= 88:
                    self.state = "game"
                # おわる
                elif 105 <= mx <=132 and 80 <= my <= 88:
                    pyxel.quit()
    
        # --- ゲーム画面 ---
        elif self.state == "game":
           # マウスカーソルを表示する
            pyxel.mouse(False)

            self.player.update(self.mapmode, self.map_x)

            # 鍵の当たり判定
            if not self.key.taken and self.check_collision(self.player, self.key):
                self.player.key_count += 1
                self.key.taken = True

            # 宝箱の当たり判定
            if self.player.key_count == 1 and self.check_collision(self.player, self.box):
                self.state = "clear"

            # ステージ１、ステージ２で階段に乗った場合
            if self.mapmode == "stage_one":
                if self.player.on_target_tile_one(self.map_x) and not self.on_stairs:
                    # マップ切り替え
                    self.mapmode = "stage_two"
                    self.map_x = 256
                    self.map_y = 0
                    self.player.player_pos = [232, 16]
                    self.on_stairs = True

            elif self.mapmode == "stage_two":
                if self.player.on_target_tile_two(self.map_x) and not self.on_stairs:
                    # マップ切り替え
                    self.mapmode = "stage_one"
                    self.map_x = 0
                    self.map_y = 0
                    self.player.player_pos = [232, 200]
                    self.on_stairs = True

            # 階段から降りたらリセット
            if not (self.player.on_target_tile_one(self.map_x)
                    or self.player.on_target_tile_two(self.map_x)):
                self.on_stairs = False

        # --- クリア画面 ---
        elif self.state == "clear":
            # マウスカーソルを表示する
            pyxel.mouse(True)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # もういちど
                if 30 <= mx <= 68 and 80 <= my <= 88:
                    self.reset_game()
                # おわる
                elif 105 <= mx <=132 and 80 <= my <= 88:
                    pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        if self.state == "start":
            pyxel.text(100, 40, "宝探しゲーム", 10, self.font)
            pyxel.text(30, 80, "はじめる", 7, self.font)
            pyxel.text(105, 80, "やめる", 7, self.font)

        elif self.state == "game":
            pyxel.bltm(0, 0, 0, self.map_x, self.map_y, 256, 224)
            self.player.draw()
            if self.mapmode == "stage_two":
              self.key.draw()
              self.box.draw()
              self.fake_box.draw()

        if self.state == "clear":
            pyxel.text(100, 40, "ゲーム クリア！", 10, self.font)
            pyxel.text(30, 80, "もういちど", 7, self.font)
            pyxel.text(105, 80, "やめる", 7, self.font)
        
App()
