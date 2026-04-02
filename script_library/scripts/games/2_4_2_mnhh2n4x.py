# 欢迎使用 PythonIDE！如果觉得好用，请给个好评哦～
import random
import json
import hashlib
import time

# 强力清屏，不占字符上限
def clear():
    print("\033c", end="")

class 网吧大亨终极版:
    def __init__(self):
        self.钱 = 500
        self.天数 = 1
        self.小时 = 10
        self.电脑总数 = 6
        self.电脑使用中 = 0
        self.电脑损坏 = 0
        self.排队顾客 = 0
        self.上网价格 = 6

        self.顾客上机时长 = [0] * self.电脑总数

        self.网管列表 = []
        self.最大网管数 = 5

        self.口碑 = 100
        self.会员数 = 0
        self.饮料库存 = 20
        self.饮料成本 = 2
        self.饮料售价 = 5
        self.装修等级 = 1
        self.天气 = ["☀️晴天", "🌧️小雨", "⛈️大雨", "❄️雪天"][random.randint(0,3)]
        self.今日营收 = 0

    def 生成存档码(self):
        clear()
        数据 = {
            "钱": self.钱, "天数": self.天数, "小时": self.小时,
            "电脑总数": self.电脑总数, "电脑使用中": self.电脑使用中, "电脑损坏": self.电脑损坏,
            "排队顾客": self.排队顾客, "上网价格": self.上网价格, "顾客上机时长": self.顾客上机时长,
            "网管列表": self.网管列表, "口碑": self.口碑, "会员数": self.会员数,
            "饮料库存": self.饮料库存, "饮料成本": self.饮料成本, "饮料售价": self.饮料售价,
            "装修等级": self.装修等级, "天气": self.天气, "今日营收": self.今日营收
        }
        字符串 = json.dumps(数据, ensure_ascii=False)
        唯一码 = hashlib.sha256((字符串 + str(time.time())).encode('utf-8')).hexdigest()[:16]
        print("🏪 存档信息".center(40, "="))
        print(f"✅ 存档码：{唯一码}")
        print("💾 存档数据：")
        print(字符串)
        input("\n回车返回菜单...")

    def 读取存档码(self):
        clear()
        try:
            数据字符串 = input("请粘贴存档数据：\n")
            数据 = json.loads(数据字符串)
            for 键, 值 in 数据.items():
                setattr(self, 键, 值)
            print("✅ 读档成功！")
        except:
            print("❌ 存档错误！")
        input("回车返回...")

    def 时间流逝(self):
        for i in range(self.电脑使用中):
            self.顾客上机时长[i] += 1

        下机人数 = 0
        for i in range(self.电脑使用中):
            if self.顾客上机时长[i] >= 24:
                下机人数 += 1

        if 下机人数 > 0:
            print(f"\n⏰ 有{下机人数}位顾客上网满24小时，已强制下机！")

        self.电脑使用中 -= 下机人数
        self.顾客上机时长 = self.顾客上机时长[下机人数:] + [0]*下机人数

        self.小时 += 1
        if self.小时 >= 24:
            self.小时 = 9
            self.天数 += 1
            self.今日营收 = 0
            self.天气 = ["☀️晴天","🌧️小雨","⛈️大雨","❄️雪天"][random.randint(0,3)]

        来客数 = random.randint(1,4)
        if self.天气 == "☀️晴天": 来客数 +=2
        if self.天气 == "⛈️大雨": 来客数 -=2
        if self.口碑>120:来客数+=2
        if self.口碑<60:来客数-=1
        self.排队顾客 = min(self.排队顾客 + max(来客数,0), 40)

        if random.randint(1,10)==1 and self.电脑损坏 < self.电脑总数//2:
            self.电脑损坏 +=1
            print("\n⚠️ 一台电脑坏了！")

        if self.电脑损坏>0 and len(self.网管列表)>0:
            for i in range(len(self.网管列表)):
                if self.电脑损坏<=0:break
                if self.网管列表[i]>0:
                    self.电脑损坏 -=1
                    self.网管列表[i] -=1
                    print(f"\n✅ 网管修好1台！还能修{self.网管列表[i]}次")
                    if self.网管列表[i]==0:
                        print("\n👋 一位网管修满5次，辞职了！")
                        self.网管列表.pop(i)
                    break

    def 快进2小时(self):
        print("\n⏩ 快进2小时...")
        self.时间流逝()
        self.时间流逝()

    def 快进3小时(self):
        print("\n⏩ 快进3小时...")
        self.时间流逝()
        self.时间流逝()
        self.时间流逝()

    def 招募网管(self):
        if len(self.网管列表)>=self.最大网管数:
            print(f"\n❌ 最多只能雇 {self.最大网管数} 个网管！")
            return
        if self.钱<200:
            print("\n❌ 招募网管需要200元！")
            return
        self.钱 -=200
        self.网管列表.append(5)
        print(f"\n👨💻 招募成功！当前网管：{len(self.网管列表)}/{self.最大网管数}")

    def 接待顾客(self):
        可用 = self.电脑总数 - self.电脑使用中 - self.电脑损坏
        if 可用<=0 or self.排队顾客<=0:
            print("\n❌ 没电脑/没顾客！")
            return
        接待 = min(可用, self.排队顾客)
        收入 = 接待 * self.上网价格
        self.钱 +=收入
        self.今日营收 +=收入
        for i in range(self.电脑使用中, self.电脑使用中+接待):
            self.顾客上机时长[i]=0
        self.电脑使用中 +=接待
        self.排队顾客 -=接待
        self.口碑 = min(self.口碑+2,150)
        print(f"\n✅ 接待{接待}人！赚{收入}元 🌟口碑+2")

    def 买电脑(self):
        价格 = 180
        if self.钱<价格:
            print(f"\n❌ 买电脑需要{价格}元！")
            return
        self.钱 -=价格
        self.电脑总数 +=1
        self.顾客上机时长.append(0)
        print("\n🆕 新增电脑一台！")

    def 卖饮料(self):
        if self.电脑使用中==0 or self.饮料库存<=0:
            print("\n❌ 没人上网，卖不出去！")
            return
        卖出 = min(random.randint(1,self.电脑使用中), self.饮料库存)
        利润 = 卖出*(self.饮料售价-self.饮料成本)
        self.钱 +=利润
        self.今日营收 +=利润
        self.饮料库存 -=卖出
        print(f"\n🥤 卖出{卖出}瓶饮料！赚{利润}元")

    def 进货饮料(self):
        进价 = self.饮料成本*10
        if self.钱<进价:
            print("\n❌ 钱不够进货！")
            return
        self.钱 -=进价
        self.饮料库存 +=10
        print(f"\n📦 饮料进货+10瓶！花费{进价}元")

    def 升级装修(self):
        费用 = 150*self.装修等级
        if self.钱<费用:
            print(f"\n❌ 升级需要{费用}元！")
            return
        self.钱 -=费用
        self.装修等级 +=1
        self.口碑 = min(self.口碑+10,150)
        print(f"\n🎨 装修升到{self.装修等级}级！口碑+10")

    def 发展会员(self):
        费用 = 80
        if self.钱<费用:
            print("\n❌ 发展会员需要80元！")
            return
        self.钱 -=费用
        新增 = random.randint(3,8)
        self.会员数 +=新增
        self.口碑 = min(self.口碑+5,150)
        print(f"\n👑 会员+{新增}人！口碑+5")

    def 每日打卡(self):
        奖励 = random.randint(50,150)
        self.钱 +=奖励
        print(f"\n🎁 打卡成功！获得{奖励}元")

    def 突发事件(self):
        事件列表 = [
            ("网红打卡🎉，顾客暴涨！", lambda: setattr(self,'排队顾客',min(self.排队顾客+15,40)) or setattr(self,'口碑',self.口碑+15)),
            ("突然停电⚡，所有顾客下机！", lambda: setattr(self,'电脑使用中',0) or setattr(self,'口碑',max(self.口碑-15,30))),
            ("老顾客送礼🎁，直接给你200元！", lambda: setattr(self,'钱',self.钱+200)),
            ("电脑集体蓝屏💥，损坏+2！", lambda: setattr(self,'电脑损坏',min(self.电脑损坏+2,self.电脑总数))),
            ("卫生抽查🚽，口碑下降！", lambda: setattr(self,'口碑',max(self.口碑-12,30))),
            ("猫咪躺键盘😺，顾客觉得超可爱！", lambda: setattr(self,'口碑',min(self.口碑+8,150))),
            ("邻店倒闭🔥，分流来一批顾客！", lambda: setattr(self,'排队顾客',min(self.排队顾客+12,40))),
            ("有人逃单💸，损失50元！", lambda: setattr(self,'钱',max(self.钱-50,0))),
            ("饮料过期🥤，库存清空！", lambda: setattr(self,'饮料库存',0)),
            ("会员日👑，会员额外增加！", lambda: setattr(self,'会员数',self.会员数+random.randint(5,12))),
        ]
        文字, func = random.choice(事件列表)
        print(f"\n🚨 突发事件：{文字}")
        func()

    def 画地图(self):
        clear()
        print("🏪【网吧大亨·终极版】🏪".center(58, "="))
        print()
        
        电脑行 = "  "
        for i in range(self.电脑总数):
            if i < self.电脑使用中:
                电脑行 += "💻  "
            elif i < self.电脑使用中 + self.电脑损坏:
                电脑行 += "🔧  "
            else:
                电脑行 += "🖥️  "
        print(电脑行)
        print("-"*58)

        顾客显示 = "👤" * min(self.排队顾客, 12)
        if self.排队顾客 >12:
            顾客显示 += f"+{self.排队顾客-12}人"
        print(f"  👥排队：{顾客显示}")
        
        print(f"  👑会员：{self.会员数}  |  👨💻网管：{len(self.网管列表)}/{self.最大网管数}  |  🎨装修：{self.装修等级}级")
        print(f"  🌟口碑：{self.口碑}  |  {self.天气}  |  📊今日营收：{self.今日营收}元")
        print(f"  💰金钱：{self.钱}  |  🥤饮料库存：{self.饮料库存}  |  💸网费：{self.上网价格}元/时")
        print("="*58)

    def 开始游戏(self):
        while True:
            self.画地图()
            print("\n【🎮 超级操作菜单】")
            print(" 1.👥接待顾客   2.🥤卖饮料    3.📦进货饮料   4.🆕买电脑")
            print(" 5.👨💻招募网管  6.🎨升级装修 7.👑发展会员  8.💰每日打卡")
            print(" 9.🚨突发事件 10.💸改网价 11.🕒快进1h 12.⏩快进2h 13.⏩快进3h")
            print("14.💾生成存档码 15.📂读取存档码 0.🚪退出游戏")
            
            选择 = input("\n请输入操作(1-15或0)：").strip()

            clear()
            if 选择 == "1": self.接待顾客()
            elif 选择 == "2": self.卖饮料()
            elif 选择 == "3": self.进货饮料()
            elif 选择 == "4": self.买电脑()
            elif 选择 == "5": self.招募网管()
            elif 选择 == "6": self.升级装修()
            elif 选择 == "7": self.发展会员()
            elif 选择 == "8": self.每日打卡()
            elif 选择 == "9": self.突发事件()
            elif 选择 == "10":
                try:
                    新价 = int(input("输入新价格(1-40)："))
                    if 1<=新价<=40:
                        self.上网价格 = 新价
                        print("✅ 价格已改！")
                except: pass
            elif 选择 == "11": self.时间流逝()
            elif 选择 == "12": self.快进2小时()
            elif 选择 == "13": self.快进3小时()
            elif 选择 == "14": self.生成存档码()
            elif 选择 == "15": self.读取存档码()
            elif 选择 == "0":
                clear()
                print("👋 感谢玩《网吧大亨·终极版》！")
                break
            
            input("\n回车继续...")

if __name__ == "__main__":
    游戏 = 网吧大亨终极版()
    游戏.开始游戏()