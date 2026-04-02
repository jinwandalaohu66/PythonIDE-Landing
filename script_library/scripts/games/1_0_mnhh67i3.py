import random

# 安全清屏（只打印换行，不调用os.system）
def clear():
    print("\n" * 50)

class InternetCafeSimulator:
    def __init__(self):
        self.money = 200
        self.computers = 5
        self.occupied = 0
        self.hour = 8
        self.day = 1
        self.repair_cost = 30
        self.broken = 0
        self.queue = 0
        self.price_per_hour = 5

    def print_status(self):
        clear()
        print("=" * 40)
        print("🎮 终端网吧模拟器")
        print("=" * 40)
        print(f"第 {self.day} 天 | 当前时间: {self.hour}:00")
        print(f"金钱: {self.money} 元")
        available = self.computers - self.occupied - self.broken
        print(f"电脑总数: {self.computers} 台 | 可用: {available} 台")
        print(f"正在使用: {self.occupied} 台 | 损坏: {self.broken} 台")
        print(f"排队顾客: {self.queue} 人")
        print(f"上网单价: {self.price_per_hour} 元/小时")
        print("=" * 40)

    def time_pass(self):
        self.hour += 1
        if self.hour >= 24:
            self.hour = 0
            self.day += 1

        if random.randint(1, 3) == 1:
            add = random.randint(0, 3)
            self.queue += add

        if random.randint(1, 8) == 1:
            available = self.computers - self.occupied - self.broken
            if available > 0 and self.broken < self.computers // 3 + 1:
                self.broken += 1
                print("\n⚠️  有一台电脑突然坏了！")

    def use_computer(self):
        available = self.computers - self.occupied - self.broken
        if available <= 0:
            print("\n❌ 没有可用电脑！")
            input("按回车继续...")
            return

        use = min(available, self.queue)
        if use == 0:
            print("\n❌ 没人来上网！")
            input("按回车继续...")
            return

        self.occupied += use
        self.queue -= use
        earn = use * self.price_per_hour
        self.money += earn
        print(f"\n✅ {use} 人开始上网！收入 {earn} 元")
        input("按回车继续...")

    def kick_customers(self):
        if self.occupied == 0:
            print("\n❌ 没人在上网！")
            input("按回车继续...")
            return
        kick_num = random.randint(1, self.occupied)
        self.occupied -= kick_num
        self.queue += kick_num // 2
        print(f"\n⚠️  你踢走了 {kick_num} 人，口碑变差了！")
        input("按回车继续...")

    def repair_computer(self):
        if self.broken == 0:
            print("\n✅ 没有坏电脑！")
            input("按回车继续...")
            return
        if self.money < self.repair_cost:
            print("\n❌ 钱不够修电脑！")
            input("按回车继续...")
            return
        self.money -= self.repair_cost
        self.broken -= 1
        print("\n✅ 修好一台电脑！")
        input("按回车继续...")

    def buy_computer(self):
        cost = 150
        if self.money < cost:
            print("\n❌ 钱不够买新电脑！")
            input("按回车继续...")
            return
        self.money -= cost
        self.computers += 1
        print("\n✅ 购买了一台新电脑！")
        input("按回车继续...")

    def change_price(self):
        try:
            new_price = int(input("\n输入新的每小时价格: "))
            if 1 <= new_price <= 50:
                self.price_per_hour = new_price
                print("✅ 价格已修改！")
            else:
                print("价格必须在1~50之间")
        except:
            print("输入无效！")
        input("按回车继续...")

    def close_cafe(self):
        self.occupied = 0
        self.queue = 0
        print("\n✅ 网吧打烊，所有人清场！")
        input("按回车继续...")

    def main(self):
        while True:
            self.print_status()
            print("\n【菜单】")
            print("1. 接待顾客（开始上网）")
            print("2. 踢走顾客")
            print("3. 维修电脑")
            print("4. 购买新电脑")
            print("5. 修改上网价格")
            print("6. 打烊清场")
            print("7. 时间快进1小时")
            print("0. 退出游戏")
            choice = input("\n请选择操作: ")

            if choice == "1":
                self.use_computer()
            elif choice == "2":
                self.kick_customers()
            elif choice == "3":
                self.repair_computer()
            elif choice == "4":
                self.buy_computer()
            elif choice == "5":
                self.change_price()
            elif choice == "6":
                self.close_cafe()
            elif choice == "7":
                self.time_pass()
            elif choice == "0":
                print("\n感谢游玩网吧模拟器！")
                break
            else:
                input("输入无效，按回车重试...")

if __name__ == "__main__":
    game = InternetCafeSimulator()
    game.main()