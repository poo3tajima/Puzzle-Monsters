"""
最終修正日:2025/10/12
作成者:田島清
"""

# Puzzle & Monsters

# インポート
import random
from dataclasses import dataclass, field

# 属性, 記号, 色番号
ELEMENT_STATUS = [
    ["火", "$", 1],
    ["水", "~", 6],
    ["風", "@", 2],
    ["土", "#", 3],
    ["命", "&", 5],
    ["無", " ", 7],
]

# 色つきの属性
WIND = "\033[32m風\033[0m"
WIND_SYMBOL = "\033[32m＠\033[0m"
FIRE = "\033[31m火\033[0m"
FIRE_SYMBOL = "\033[31m＄\033[0m"
EARTH = "\033[33m土\033[0m"
EARTH_SYMBOL = "\033[33m＃\033[0m"
WATER = "\033[36m水\033[0m"
WATER_SYMBOL = "\033[36m～\033[0m"
LIFE = "\033[35m命\033[0m"
LIFE_SYMBOL = "\033[35m＆\033[0m"

# 色つきのキャラクター名
SEIRYU = "\033[32m青龍\033[0m"
SUZAKU = "\033[31m朱雀\033[0m"
BYAKKO = "\033[33m白虎\033[0m"
GENBU = "\033[36m玄武\033[0m"

# ステージ(A～N 14列)
STAGE = "ABCDEFGHIJKLMN"


# プレイヤーの名前を入力
def player_name_input():
    player_name = input("＊プレイヤーの名前を入力してください ＞")

    # 空白だったら、再入力する
    while player_name == "":
        player_name = input("＊プレイヤーの名前を入力してください ＞")

    return player_name


# 味方パーティを編成する
def organize_party(player_name, friends):
    total_hp, total_MAX_HP = create_total(friends)
    party = Party(player_name, friends, total_hp, total_MAX_HP)

    return party


# 味方パーティのHPを合計する
def create_total(friends):
    total_hp = 0
    total_MAX_HP = 0

    for character in friends:
        total_hp += character.hp

    for character in friends:
        total_MAX_HP += character.MAX_HP

    return total_hp, total_MAX_HP


# ダンジョンに到着
def go_dungeon(party, monsters):
    print("")
    print(f"{party.player_name}たち(HP:{party.total_hp})はダンジョンに到着した")
    print("")
    show_party(party)

    # モンスター5体と順番にたたかう
    for monster in monsters:
        is_win = do_battle(party, monster)

        # モンスターをたおしたら
        if is_win == True:
            party.wins += 1
        # まけたら
        else:
            break

        # 5体たおしたとき
        if party.wins == 5:
            print("--------------------------------------")
            break
        else:
            print("")
            print(f"{party.player_name}(HP:{party.total_hp})")
            print(f"{party.player_name}たちはさらに奥へと進んだ")
            print("--------------------------------------")
            input("ENTER")


# 味方パーティ編成を表示
def show_party(party):
    print("--------＜パーティー編成＞------------")

    # ステータスを順番に表示
    for character in party.friends:
        print(
            f"{character.display_name} HP={character.hp} 攻撃={character.ap} 防御={character.dp}"
        )

    print("--------------------------------------")


# 1匹づつモンスターと戦う
def do_battle(party, monster):
    print("")
    print("")
    print(f"{monster.display_name} があらわれた！")

    is_continue = True
    is_win = False
    gems = []

    while is_continue:
        # プレイヤーのターン
        is_continue = on_player_turn(is_continue, party, monster, gems)

        if is_continue == False:
            print("")
            print("")
            print(f"{monster.display_name} をたおした！")
            print("")
            is_win = True
            break

        #  モンスターのターン
        is_continue = on_enemy_turn(is_continue, party, monster)

        if is_continue == False:
            print("")
            print(f"{party.player_name}たちはまけてしまった")
            break

    return is_win


# プレイヤーのターン
def on_player_turn(is_continue, party, monster, gems):
    print("")
    print("")
    print(f"★★★ {party.player_name}のターン(HP={party.total_hp}) ★★★")

    # バトルフィールドと宝石の作成と表示
    show_battle_field(party, monster, gems)

    # コマンドを入力
    command = command_input()

    # 宝石を移動する
    move_gem(command, gems)

    # 宝石を操作する
    processing_gems(party, monster, gems)

    # モンスターのHPが0ならバトル終了
    if monster.hp == 0:
        is_continue = False

    return is_continue


# バトルフィールドを表示
def show_battle_field(party, monster, gems):
    print("")
    print("///// バトルフィールド/////")
    print("")
    # モンスターの名前を表示
    print(f"{monster.display_name} HP={monster.hp}/{monster.MAX_HP}")
    print("         VS")

    # キャラクターの名前とHPを表示
    for character in party.friends:
        print(f"{character.display_name} ", end="")
        print(f"HP={character.hp}", end="")
        print(f"/{character.MAX_HP}", end="")
        print("")

    # 生命力を表示
    print(f"  ( 生命力:{party.revive_power} )")

    print("")
    print("--------------------------------------")

    # ステージ(A～N 14列)を作成
    for char in STAGE:
        print(char, end="")
        print(" ", end="")

    print("")

    # 宝石を表示
    if not gems:  # 宝石がないなら、作成する
        gems = fill_gems(gems)
        print_gems(gems)
    else:  # あるなら、表示
        print_gems(gems)

    print("")
    print("--------------------------------------")


# 宝石を作成
def fill_gems(gems):
    for i in range(len(STAGE)):
        num = random.randint(0, 4)  # 0火～4命
        symbol = ELEMENT_STATUS[num][1]  # 記号
        gems.append(symbol)
    return gems


# 宝石を表示
def print_gems(gems):
    for symbol in gems:
        for ELE in ELEMENT_STATUS:
            if symbol == ELE[1]:
                color = ELE[2]
        print(f"\033[3{color}m{symbol}\033[0m", end="")
        print(" ", end="")


# プレイヤーの名前を入力
def command_input():
    command = input("コマンド？ ＞").upper()
    is_passed = check_valid_command(command)

    while not is_passed:
        command = input("コマンド？ ＞").upper()
        is_passed = check_valid_command(command)

    return command


# コマンド入力チェック
def check_valid_command(command):
    allowed_char = 0
    is_passed = False

    if (
        len(command) == 2  # 2文字か
        and command[0] != command[1]  # 2つが違う文字か
        and command.isupper()  # 大文字か
    ):

        for char in command:  # AB
            if char in STAGE:  # A～Nか
                allowed_char += 1

        if allowed_char == 2:
            is_passed = True

    return is_passed


# AからBまで宝石を移動する  例 ADとして
def move_gem(command, gems):
    left_position = STAGE.index(command[0])  # 例 index0
    right_position = STAGE.index(command[1])  # 例 index3

    # 左右どちらにいくか
    if left_position < right_position:  # 右の値が大きいなら
        move = right_position - left_position

        for i in range(move):  # move=3 右へ移動
            gem_start = left_position + i  # i=0～2
            gem_goll = left_position + i + 1
            swap_gem(gems, gem_start, gem_goll)

    else:  # 右の値が小さいなら
        move = left_position - right_position

        for i in range(move):  # move=3 左へ移動
            gem_start = left_position - i  # i=0～2
            gem_goll = left_position - i - 1
            swap_gem(gems, gem_start, gem_goll)


# 隣の宝石と交換する
def swap_gem(gems, gem_start, gem_goll):
    temp = gems[gem_goll]
    gems[gem_goll] = gems[gem_start]
    gems[gem_start] = temp
    temp = None
    print_gems(gems)
    print("")


# 移動後の宝石を操作する  ★ここからつづき
def processing_gems(party, monster, gems):
    # リセット
    party.combo_count = 0
    party.sum_same_count = 0
    is_check_gems = True

    while is_check_gems:
        # 宝石がそろったかチェック
        is_check_gems = check_banishable(party, monster, gems, is_check_gems)

        # 宝石を補充するか
        if not is_check_gems:
            blank_gems = len(STAGE) - len(gems)

            # 空きがあれば、補充する
            if blank_gems != 0:
                spawn_gems(gems, blank_gems)
                print_gems(gems)
                print("")
                # 補充後、再び宝石チェックへ戻る
                is_check_gems = True
                # 空きが0なら操作終了

            else:
                break


# ３つ以上そろった宝石をチェックする
def check_banishable(party, monster, gems, is_check_gems):
    # リセット
    same_count = 0
    key_symbol = ""

    # 左端Aから右端Nまでチェックして、そろわなければ終了
    for position in range(len(gems) - 1):  # position(0～12) 1つ前まで
        # O
        if gems[position] == gems[position + 1]:
            same_count += 1

            # O 最後のpositionで３つ以上そろっていたら
            if position == len(gems) - 2 and same_count >= 2:
                key_symbol = gems[position + 1]
                position = len(gems) - 1
                party.combo_count += 1  # コンボ数追加
                party.sum_same_count += same_count
                banish_gems(
                    party,
                    monster,
                    gems,
                    same_count,
                    position,
                    key_symbol,
                )
                is_check_gems = False

                return is_check_gems

            # O 最後のpositionならチェック終了
            elif position == len(gems) - 2:
                is_check_gems = False

                return is_check_gems

        # X 途中3つ以上そろっていたら、宝石操作
        elif gems[position] != gems[position + 1] and same_count >= 2:
            key_symbol = gems[position]
            party.combo_count += 1  # コンボ数追加
            party.sum_same_count += same_count
            banish_gems(
                party,
                monster,
                gems,
                same_count,
                position,
                key_symbol,
            )

            return is_check_gems

        # X
        elif gems[position] != gems[position + 1]:
            same_count = 0

            # X 最後のpositionならチェック終了
            if position == len(gems) - 2:
                is_check_gems = False

                return is_check_gems


# 同じ宝石を消す
def banish_gems(party, monster, gems, same_count, position, key_symbol):
    # そろった宝石を無属性へ変更
    change_gems(gems, same_count, position)
    print_gems(gems)

    # そろえた宝石を判定する
    check_select_symbol(party, monster, same_count, key_symbol)

    # 無属性を消し左につめる
    print_gems(gems)
    shift_gems(gems, same_count, position)


# そろった宝石を無属性に変える
def change_gems(gems, same_count, position):
    for i in range(same_count + 1):
        gems[position - same_count + i] = ELEMENT_STATUS[5][1]


# そろった宝石を判定する
def check_select_symbol(party, monster, same_count, key_symbol):
    # コンボ増幅値を算出(float)
    combo_power = 1.5 ** ((same_count + 1) - 3 + party.combo_count)

    # & は回復、それ以外はこうげき
    if key_symbol == "&":
        print("")
        print("")
        print("")
        do_heal(party, combo_power)
    else:
        # 宝石にあわせて、こうげきするキャラクターをえらぶ
        # キャラクターの index を取得
        for character in party.friends:
            if key_symbol == character.symbol:
                attack_index = party.friends.index(character)
                break

        # キャラクターが死んでいるか
        is_dead = check_is_dead(party, attack_index)

        # 死んでしまったキャラクターは何もできない
        if is_dead:
            print("")
            print("")
            print("")
            print("宝石はかがやいて消えてしまった...")
            print(f"しかし、{party.player_name}たちに力をあたえた")
            party.revive_power += 1
            print("生命力が１ふえた")
            print(f"  ( 生命力:{party.revive_power} )")
            input("ENTER")
            print("")
            print("")

            # 生命力が３以上なら死んだキャラクターをランダムで復活させる
            if party.revive_power >= 3:
                dead_list = []

                # targetの中の"dead"を調べる  indexをdead_listへ追加
                for index in range(len(party.target)):
                    if party.target[index] == "dead":
                        dead_list.append(index)

                # 例 死んだキャラクターをdead_list[2, 3]から選ぶ
                revive_index = random.choice(dead_list)

                # 選んだキャラクターを復活させる
                do_revive(party, revive_index)

                party.revive_power -= 3
                print("生命力が３へった")
                print(f"  ( 生命力:{party.revive_power} )")
                input("ENTER")
                print("")
                print("")

        # キャラクターが生きていたら、こうげき
        else:
            print("")
            print("")
            # 属性相性判定
            superiority = attribute_check(monster, key_symbol)
            do_attack(party, monster, key_symbol, superiority, combo_power)


# HPを回復する
def do_heal(party, combo_power):
    # 回復量を算出
    heal = int(20 * combo_power)
    random_value = round(heal / 10)
    random_heal = random.randrange(-random_value, random_value)
    heal_power = heal + random_heal

    # HPが一番低いキャラクターを選ぶ
    min_hp_index = check_min_hp(party)
    heal_character = party.friends[min_hp_index]

    # 回復すると最大値をこえてしまうとき
    if heal_character.MAX_HP - heal_character.hp <= heal_power:
        heal_power = heal_character.MAX_HP - heal_character.hp

    # コンボがあるとき
    if party.combo_count >= 2:
        print(
            f"{heal_character.display_name} はHPが{heal_power}回復した！ {party.combo_count}コンボ！！"
        )
    else:
        print(f"{heal_character.display_name} はHPが{heal_power}回復した！")

    heal_character.hp += heal_power
    party.total_hp, party.total_MAX_HP = create_total(party.friends)
    input("ENTER")
    print("")


# HPが一番低いキャラクターのindexを取得
def check_min_hp(party):
    # hp_listを作成する
    hp_list = [character.hp for character in party.friends]

    # hp_listから HP=0 を含まないリストを作成する
    non_zero_hp_list = [hp for hp in hp_list if hp != 0]

    # 一番低いHPのindexを取得
    min_hp_index = hp_list.index(min(non_zero_hp_list))

    return min_hp_index


# キャラクターが死んでいるか
def check_is_dead(party, attack_index):
    is_dead = False

    if party.target[attack_index] == "dead":
        is_dead = True

    return is_dead


# キャラクターを生き返らせる
def do_revive(party, revive_index):
    revive_character = party.friends[revive_index]

    # HPを最大値にする
    revive_character.hp = revive_character.MAX_HP

    # targetのindexを戻す
    party.target[revive_index] = revive_index

    # 名前の色を元に戻す
    revive_character.added_display_name(ELEMENT_STATUS)
    print(
        f"{revive_character.display_name}(HP={revive_character.hp}/{revive_character.MAX_HP}) は生きかえった！"
    )


# プレイヤーのこうげき
def do_attack(party, monster, key_symbol, superiority, combo_power):
    # 記号にあわせて、こうげきするキャラクターを決める
    for character in party.friends:
        if key_symbol == character.symbol:
            attack_char = character
            break

    # ダメージを算出
    power = int(attack_char.ap * superiority * combo_power - monster.dp)

    # power 0以下は1に変更
    if power <= 0:
        power = 1

    random_value = round(power / 10)

    # value 0は1に変更
    if random_value == 0:
        random_value = 1

    random_power = random.randrange(-random_value, random_value)
    attack_power = power + random_power

    # コンボがあるとき
    if party.combo_count >= 2:
        print(f"{attack_char.display_name} のこうげき！ {party.combo_count}コンボ！！")
    else:
        print(f"{attack_char.display_name} のこうげき！")

    print(f"{monster.display_name} に{attack_power}のダメージをあたえた")
    input("ENTER")
    print("")
    print("")

    # 敵のHPを減らす
    if monster.hp <= attack_power:
        attack_power = monster.hp

    monster.hp -= attack_power


# 属性の相性判定
def attribute_check(monster, select_symbol):
    superiority = 1.0
    defence_symbol = monster.symbol
    print("")

    if select_symbol == "@":
        if defence_symbol == "#":
            superiority = 2.0
            print("  (★ 聖獣 @:# 強)")
        elif defence_symbol == "$":
            superiority = 0.5
            print("  (★ 聖獣 @:$ 弱)")
        else:
            print("  (★ 相性補正なし)")

    if select_symbol == "$":
        if defence_symbol == "@":
            superiority = 2.0
            print("  (★ 聖獣 $:@ 強)")
        elif defence_symbol == "~":
            superiority = 0.5
            print("  (★ 聖獣 $:~ 弱)")
        else:
            print("  (★ 相性補正なし)")

    if select_symbol == "#":
        if defence_symbol == "~":
            superiority = 2.0
            print("  (★ 聖獣 #:~ 強)")
        elif defence_symbol == "@":
            superiority = 0.5
            print("  (★ 聖獣 #:@ 弱)")
        else:
            print("  (★ 相性補正なし)")

    if select_symbol == "~":
        if defence_symbol == "$":
            superiority = 2.0
            print("  (★ 聖獣 ~:$ 強)")
        elif defence_symbol == "#":
            superiority = 0.5
            print("  (★ 聖獣 ~:# 弱)")
        else:
            print("  (★ 相性補正なし)")

    return superiority


# 宝石を左に寄せる
def shift_gems(gems, same_symbols, position):
    print("")
    for _ in range(same_symbols + 1):  # 例 3回
        gems.pop(position - same_symbols)
        print_gems(gems)
        print("")


# 新しい宝石を補充する
def spawn_gems(gems, blank_gems):
    for _ in range(blank_gems):
        num = random.randint(0, 4)  # 0火～4命
        symbol = ELEMENT_STATUS[num][1]  # 記号
        gems.append(symbol)


# モンスターのターン
def on_enemy_turn(is_continue, party, monster):
    print("")
    print("")
    print(f"★★★ {monster.display_name} のターン(HP={monster.hp}) ★★★")

    do_enemy_attack(party, monster)

    # パーティーのHPが全員0になったら
    if party.total_hp == 0:
        is_continue = False

    return is_continue


# モンスターのこうげき
def do_enemy_attack(party, monster):
    # こうげきするキャラクターをランダムに選択し、indexを取得
    receive_index = random.choice(party.target)

    # 選んだキャラクターが死んでいたら、選びなおす
    while receive_index == "dead":
        receive_index = random.choice(party.target)

    # ダメージを受けるキャラクターを確定
    receive_character = party.friends[receive_index]
    receive_symbol = receive_character.symbol  # 属性判定用

    # 属性相性を判定
    superiority = attribute_check(monster, receive_symbol)

    # モンスター用に相性値を反転する
    if superiority == 2.0:
        superiority = 0.5
        print("  (★ モンスター 弱)")
    elif superiority == 0.5:
        superiority = 2.0
        print("  (★ モンスター 強)")

    # ダメージ計算
    power = int(monster.ap * superiority) - receive_character.dp

    # power 0以下は1に変更
    if power <= 0:
        power = 1

    random_value = round(power / 10)

    # value 0は1に変更
    if random_value == 0:
        random_value = 1

    random_power = random.randrange(-random_value, random_value)
    attack_power = power + random_power

    # こうげきの表示
    print(f"{monster.display_name} のこうげき！")
    print(f"{receive_character.display_name} に{attack_power}のダメージをあたえた")
    input("ENTER")

    # ダメージを受けて、キャラクターのHPが0になるか
    if receive_character.hp <= attack_power:
        attack_power = receive_character.hp
        print(f"{receive_character.display_name} はたおれた")  # 色付き表示名で表示
        change_dead(party, receive_index)

    # 残りHPがあるなら
    receive_character.hp -= attack_power
    party.total_hp, party.total_MAX_HP = create_total(party.friends)


# "dead" 状態にする
def change_dead(party, receive_index):
    dead_character = party.friends[receive_index]

    # targetを "dead" にする
    party.target[receive_index] = "dead"

    # 色付き表示名を黒にして見えなくする
    color = 0  # 黒
    symbol_plus_name = (
        dead_character.symbol + dead_character.name + dead_character.symbol
    )
    dead_character.display_name = f"\033[3{color}m{symbol_plus_name}\033[0m"


@dataclass
class Character:
    name: str
    hp: int
    MAX_HP: int
    element: str
    symbol: str
    ap: int
    dp: int
    display_name: str = ""

    # 色付き表示名を追加する
    def added_display_name(self, ELEMENT_STATUS):
        for ELE in ELEMENT_STATUS:
            if self.symbol == ELE[1]:
                color = ELE[2]

        symbol_plus_name = self.symbol + self.name + self.symbol
        display_name = f"\033[3{color}m{symbol_plus_name}\033[0m"
        self.display_name = display_name


@dataclass
class Party:
    player_name: str
    friends: list
    total_hp: int
    total_MAX_HP: int
    target: list[str | int] = field(
        default_factory=lambda: [0, 1, 2, 3]
    )  # こうげき対象の状態 (indexか"dead")
    sum_same_count: int = 0  # 消した宝石の合計
    combo_count: int = 0  # コンボ数
    revive_power: int = 0  # 生命力数
    wins: int = 0  # モンスターをたおした数


# メイン
def main():
    print("")
    # プレイヤー名入力
    player_name = player_name_input()
    print("")

    # プロローグ
    print("～～～～～～～～～～～～～～～～～～～～～～")
    print("～                                        ～")
    print("～          ///////////////////           ～")
    print("～     ////////////////       //////      ～")
    print("～   ///////////////// ///////////////    ～")
    print("～     ///   Puzzle & Monsters   ///      ～")
    print("～   /////////////// /////////////////    ～")
    print("～     //////       ////////////////      ～")
    print("～          ///////////////////           ～")
    print("～                                        ～")
    print("～～～～～～～～～～～～～～～～～～～～～～")
    print("")
    print("")
    print(" ウインドウをタテにひろげて表示してください")
    print("")
    input("ENTER")

    print("")
    print("ドラゴンを討伐するため")
    print(f"{player_name}たちは大陸のはて")
    print("けわしい山のふもとにあるダンジョンへたどりついた")
    print("")
    print(f"{player_name}につき従うのは四方守護聖獣")
    print(f"  東 {WIND}の精霊  {SEIRYU}")
    print(f"  南 {FIRE}の精霊  {SUZAKU}")
    print(f"  西 {EARTH}の精霊  {BYAKKO}")
    print(f"  北 {WATER}の精霊  {GENBU}")
    print("")
    input("ENTER")

    print("")
    print("ゲームルール")
    print("  ・ダンジョンには５体のモンスターがいます")
    print("  ・１体づつ戦い、順番にたおし進みます")
    print("  ・バトルは宝石を操作しておこないます")
    print("  ・ステージにA～Nまで14個の宝石がならびます")
    print("  ・A～N (小文字でも可) の文字を２つ入力して、コマンドで宝石を操作します")
    print("  ・（[AN] AをNの場所まで移動する 逆方向も可能 ）")
    print(
        f"  ・宝石の属性  {WIND}{WIND_SYMBOL}  {FIRE}{FIRE_SYMBOL}  {EARTH}{EARTH_SYMBOL}  {WATER}{WATER_SYMBOL}  {LIFE}{LIFE_SYMBOL}"
    )
    print("  ・宝石が３つ以上そろうと宝石のパワーが発揮します")
    print(
        f"  ・{WIND_SYMBOL}{FIRE_SYMBOL}{EARTH_SYMBOL}{WATER_SYMBOL}はその属性の聖獣がモンスターをこうげきします"
    )
    print(f"  ・{LIFE_SYMBOL}は一番少ないHPの聖獣を回復します")
    print(
        f"  ・属性には相性があります  {WIND}＞{EARTH}  {FIRE}＞{WIND}  {EARTH}＞{WATER}  {WATER}＞{FIRE}"
    )
    print("  ・相性が強いと効果が２倍  弱いと１／２倍になります")
    print("  ・宝石を一度に多く消すと、パワーが増します")
    print("  ・一度の操作で連続して消すと、コンボ技によりパワーが何倍にも増します")
    print("  ・たおれた聖獣の宝石を消したときは、生命力が１増えます")
    print("  ・生命力が３つたまると、たおれた聖獣をランダムで復活できます(HP最大)")
    print("  ・ドラゴンをたおしたら、ゲームクリア")
    print("  ・聖獣が全員たおれてしまったら、ゲームオーバー")
    print("")
    print("～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～～")
    print("")
    input("ENTER")

    # 味方フレンズを定義 (名前, hp, MAX_HP, 属性, 記号, ap, dp)
    seiryu = Character("青龍", 150, 150, "風", "@", 15, 10)
    suzaku = Character("朱雀", 150, 150, "火", "$", 25, 10)
    byakko = Character("白虎", 150, 150, "土", "#", 20, 5)
    genbu = Character("玄武", 150, 150, "水", "~", 20, 15)

    friends = [seiryu, suzaku, byakko, genbu]

    # フレンズに色付き表示名を追加する
    for character in friends:
        character.added_display_name(ELEMENT_STATUS)

    # 味方パーティーを編成する
    party = organize_party(player_name, friends)

    # 敵モンスターを定義 (名前, hp, MAX_HP, 属性, 記号, ap, dp)
    slime = Character("スライム", 100, 100, "水", "~", 10, 1)
    goblin = Character("ゴブリン", 200, 200, "土", "#", 20, 5)
    megabat = Character("オオコウモリ", 300, 300, "風", "@", 30, 10)
    werewolf = Character("ウェアウルフ", 400, 400, "土", "#", 40, 15)
    dragon = Character("ドラゴン", 600, 600, "火", "$", 50, 20)

    monsters = [slime, goblin, megabat, werewolf, dragon]

    # モンスターズに色付き表示名を追加する
    for monster in monsters:
        monster.added_display_name(ELEMENT_STATUS)

    # ダンジョンへ入る
    go_dungeon(party, monsters)

    # エンディング
    print("")
    if party.wins != 5:
        print(f"{party.player_name}たちはダンジョンから逃げ出した")
        print("")
        print("＊＊＊ GAME OVER ＊＊＊")
    else:
        print(f"{party.player_name}たちはモンスターを全員たおした")
        print("長い旅が終わった...")
        print("")
        print("＊＊＊ GAME CLEARED!! ＊＊＊")

    print(f"倒したモンスターの数 = {party.wins}")


# 実行
main()
print("")
print("")
input("ウインドウをとじる ＞ ENTER")
