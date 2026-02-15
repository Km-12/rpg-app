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

        # 移動速度
        self.speed = 2
        # 移動向き
        self.direction = "down"
        # 移動状態
        self.is_moving = False

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
        self.is_moving = False
        # 右移動
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.direction = "right"
            if self.move_check(self.player_pos[0]+16, self.player_pos[1], mapmode, map_x):
                self.player_pos[0] += self.speed
                self.is_moving = True
        # 左移動            
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.direction = "left"
            if self.move_check(self.player_pos[0]-4, self.player_pos[1], mapmode, map_x):
                self.player_pos[0] -= self.speed
                self.is_moving = True
        # 上移動
        elif pyxel.btn(pyxel.KEY_UP):
            self.direction = "up"
            if self.move_check(self.player_pos[0], self.player_pos[1]-4, mapmode, map_x):
                self.player_pos[1] -= self.speed
                self.is_moving = True
        # 下移動
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direction = "down"
            if self.move_check(self.player_pos[0], self.player_pos[1]+16, mapmode, map_x):
                self.player_pos[1] += self.speed
                self.is_moving = True

    def draw(self):
        # 立ち絵
        if not self.is_moving:
            pyxel.blt(self.player_pos[0] , self.player_pos[1] , 0, 0, 48, self.w, self.h, 13)
            return
        
        # 歩行
        frame_u = 64 if (pyxel.frame_count // 8) % 2 == 0 else 80

        # 向きごとに座標を設定
        if self.direction == "down":
            v = 0
        elif self.direction == "right":
            v = 16
        elif self.direction == "left":
            v = 32
        elif self.direction == "up":
            v = 48

        pyxel.blt(self.player_pos[0], self.player_pos[1], 0, v, frame_u, self.w, self.h, 13)

class Enemy:
    # Enemyの初期化
    def __init__(self, x, y, move_type="vertical"):
        # 初期位置
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16

        self.speed = 1.2
        self.direction = 1
        self.move_range = 16
        self.start_x = x
        self.start_y = y
    
        self.move_type = move_type

    def update(self):
        # 上下移動
        if self.move_type == "vertical":
            self.y += self.speed * self.direction

            # 指定範囲の移動
            if self.y > self.start_y + self.move_range:
                self.direction = -1
            elif self.y < self.start_y - self.move_range:
                self.direction = 1

        # 左右移動
        elif self.move_type == "horizontal":
            self.x += self.speed * self.direction

            if self.x > self.start_x + self.move_range:
                self.x = self.start_x + self.move_range
                self.direction = -1
            elif self.x < self.start_x - self.move_range:
                self.x = self.start_x - self.move_range
                self.direction = 1

    def draw(self):
            pyxel.blt(self.x, self.y, 0, 0, 96, self.w, self.h, 13)

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

class FakeKey:
    # FakeKeyの初期化
    def __init__(self, x, y):
        # 初期位置
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.taken = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 48, 40, self.w, self.h, 13)

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

        self.enemies = [Enemy(172, 64, "vertical"), Enemy(182, 156, "horizontal")]

        self.key = Key(8, 8)
        self.fake_key = FakeKey(228, 98)
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
    
    def handle_stairs(self):
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

    def update(self):
        mx = pyxel.mouse_x
        my = pyxel.mouse_y

        # --- スタート画面 ---
        if self.state == "start":
            # マウスカーソルを表示する
            pyxel.mouse(True)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # はじめる
                if 40 <= mx <= 120 and 90 <= my <= 100:
                    self.state = "game"
                # おわる
                elif 170 <= mx <= 220 and 90 <= my <= 100:
                    pyxel.quit()
    
        # --- ゲーム画面 ---
        elif self.state == "game":
           # マウスカーソルを表示する
            pyxel.mouse(False)

            self.player.update(self.mapmode, self.map_x)

            # ステージ別 当たり判定処理
            if self.mapmode == "stage_one":
                for enemy in self.enemies:
                    enemy.update()

                    # 敵の当たり判定
                    if self.check_collision(self.player, enemy):
                        self.state = "over"
                        break

            elif self.mapmode == "stage_two":
                # 鍵の当たり判定
                if not self.key.taken and self.check_collision(self.player, self.key):
                    self.player.key_count += 1
                    self.key.taken = True

                # 当たり宝箱の当たり判定
                if self.player.key_count == 1 and self.check_collision(self.player, self.box):
                    self.state = "clear"

                # 偽宝箱の当たり判定
                if self.check_collision(self.player, self.fake_box):
                    self.state = "over"

                # 偽鍵の当たり判定
                if self.check_collision(self.player, self.fake_key):
                    self.state = "over"

            # ステージ別の階段移動処理
            self.handle_stairs()

        # --- クリア画面 ---
        elif self.state == "clear":
            # マウスカーソルを表示する
            pyxel.mouse(True)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # もういちど
                if 40 <= mx <= 120 and 90 <= my <= 100:
                    self.reset_game()
                # おわる
                elif 170 <= mx <= 220 and 90 <= my <= 100:
                    pyxel.quit()

        # --- ゲームオーバー画面 ---
        elif self.state == "over":
            # マウスカーソルを表示する
            pyxel.mouse(True)
            
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                # もういちど
                if 40 <= mx <= 120 and 90 <= my <= 100:
                    self.reset_game()
                # おわる
                elif 170 <= mx <= 220 and 90 <= my <= 100:
                    pyxel.quit()

    def draw(self):
        pyxel.cls(0)

        if self.state == "start":
            pyxel.text(100, 30, "宝探しゲーム", 10, self.font)  
            pyxel.text(40, 90, "はじめる", 7, self.font)
            pyxel.text(170, 90, "やめる", 7, self.font)

        elif self.state == "game":
            pyxel.bltm(0, 0, 0, self.map_x, self.map_y, 256, 224)
            self.player.draw()
            if self.mapmode == "stage_one":
              for enemy in self.enemies:
                enemy.draw()          
            elif self.mapmode == "stage_two":
              self.key.draw()
              self.box.draw()
              self.fake_key.draw()
              self.fake_box.draw()

        if self.state == "clear":
            pyxel.text(100, 30, "ゲーム クリア！", 10, self.font)
            pyxel.text(40, 90, "もういちど", 7, self.font)
            pyxel.text(170, 90, "やめる", 7, self.font)
   
        if self.state == "over":
            pyxel.text(95, 30, "ゲーム オーバー！", 10, self.font)
            pyxel.text(40, 90, "もういちど", 7, self.font)
            pyxel.text(170, 90, "やめる", 7, self.font)  
App()
