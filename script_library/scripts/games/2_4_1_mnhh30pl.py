import random
import json
import hashlib
import time

# 清屏函数（彻底清空前面所有输出）
def clear():
    print("\033c", end="")  # 强力清屏，不残留任何历史字符

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
            print(f"⏰ {下机人数}人满24小时强制下机")

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

        if self.电脑损坏>0 and len(self.网管列表)>0:
            for i in range(len(self.网管列表)):
                if self.电脑损坏<=0:break
                if self.网管列表[i]>0:
                    self.电脑损坏 -=1
                    self.网管列表[i] -=1
                    if self.网管列表[i]==0:
                        print("👋 网管辞职了")
                        self.网管列表.pop(i)
                    break

    def 快进2小时(self):
        self.时间流逝()
        self.时间流逝()

    def 快进3小时(self):
        self.时间流逝()
        self.时间流逝()
        self.时间流逝()

    def 招募网管(self):
        if len(self.网管列表)>=self.最大网管数:
            print("❌ 最多5名网管")
            return
        if self.钱<200:
            print("❌ 钱不够")
            return
        self.钱 -=200
        self.网管列表.append(5)
        print("👨💻 招募成功")

    def 接待顾客(self):
        可用 = self.电脑总数 - self.电脑使用中 - self.电脑损坏
        if 可用<=0 or self.排队顾客<=0:
            print("❌ 无电脑/无顾客")
            return
        接待 = min(可用, self.排队顾客)
        self.钱 += 接待*self.上网价格
        self.今日营收 +=接待*self.上网价格
        for i in range(self.电脑使用中, self.电脑使用中+接待):
            self.顾客上机时长[i]=0
        self.电脑使用中 +=接待
        self.排队顾客 -=接待
        self.口碑 = min(self.口碑+2,150)
        print(f"✅ 接待{接待}人")

    def 买电脑(self):
        if self.钱<180:
            print("❌ 钱不够")
            return
        self.钱 -=180
        self.电脑总数 +=1
        self.顾客上机时长.append(0)
        print("🆕 电脑+1")

    def 卖饮料(self):
        if self.电脑使用中==0 or self.饮料库存<=0:
            print("❌ 无法售卖")
            return
        卖出 = min(random.randint(1,self.电脑使用中), self.饮料库存)
        利润 = 卖出*(self.饮料售价-self.饮料成本)
        self.钱 +=利润
        self.今日营收 +=利润
        self.饮料库存 -=卖出
        print(f"🥤 卖出{卖出}瓶")

    def 进货饮料(self):
        if self.钱<20:
            print("❌ 钱不够")
            return
        self.钱 -=20
        self.饮料库存 +=10
        print("📦 饮料+10")

    def 升级装修(self):
        费用 = 150*self.装修等级
        if self.钱<费用:
            print("❌ 钱不够")
            return
        self.钱 -=费用
        self.装修等级 +=1
        self.口碑 = min(self.口碑+10,150)
        print(f"🎨 装修到{self.装修等级}级")

    def 发展会员(self):
        if self.钱<80:
            print("❌ 钱不够")
            return
        self.钱 -=80
        新增 = random.randint(3,8)
        self.会员数 +=新增
        self.口碑 = min(self.口碑+5,150)
        print(f"👑 会员+{新增}")

    def 每日打卡(self):
        奖励 = random.randint(50,150)
        self.钱 +=奖励
        print(f"🎁 奖励{奖励}元")

    def 突发事件(self):
        事件 = [
            ("网红打卡🎉，排队+15", lambda: setattr(self,'排队顾客',min(self.排队顾客+15,40))),
            ("停电⚡，全部下机", lambda: setattr(self,'电脑使用中',0)),
            ("老顾客送礼💳，+200元", lambda: setattr(self,'钱',self.钱+200)),
            ("电脑蓝屏💥，损坏+2", lambda: setattr(self,'电脑损坏',min(self.电脑损坏+2,self.电脑总数))),
            ("卫生抽查🚽，口碑-12", lambda: setattr(self,'口碑',max(self.口碑-12,30))),
            ("猫咪躺椅😺，口碑+8", lambda: setattr(self,'口碑',min(self.口碑+8,150))),
            ("邻店倒闭🔥，排队+12", lambda: setattr(self,'排队顾客',min(self.排队顾客+12,40))),
            ("有人逃单💸，-50元", lambda: setattr(self,'钱',max(self.钱-50,0))),
        ]
        文字, func = random.choice(事件)
        print(f"🚨 {文字}")
        func()

    def 画地图(self):
        clear()  # 每次刷新界面都彻底清空历史
        print("🏪【网吧大亨】".center(50,"="))
        电脑行 = "  "
        for i in range(self.电脑总数):
            if i < self.电脑使用中:电脑行+="💻 "
            elif i < self.电脑使用中+self.电脑损坏:电脑行+="🔧 "
            else:电脑行+="🖥️ "
        print(电脑行)
        print("-"*50)
        print(f"👥排队：{min(self.排队顾客,40)}/40   👨💻网管：{len(self.网管列表)}/5")
        print(f"💰{self.钱}  🌟口碑{self.口碑}  🎨{self.装修等级}级  {self.天气}")
        print(f"🖥️{self.电脑使用中}/{self.电脑总数}  🥤{self.饮料库存}  💸{self.上网价格}元/时")
        print("="*50)

    def 开始游戏(self):
        while True:
            self.画地图()
            print("\n1接待 2卖饮 3进货 4买电脑 5招网管")
            print("6装修 7会员 8打卡 9事件 10改价")
            print("11快进1h 12快进2h 13快进3h")
            print("14存档 15读档 0退出")
            选择 = input("\n选择：").strip()

            # 每次操作前先清屏，只显示结果
            clear()
            if 选择=="1":self.接待顾客()
            elif 选择=="2":self.卖饮料()
            elif 选择=="3":self.进货饮料()
            elif 选择=="4":self.买电脑()
            elif 选择=="5":self.招募网管()
            elif 选择=="6":self.升级装修()
            elif 选择=="7":self.发展会员()
            elif 选择=="8":self.每日打卡()
            elif 选择=="9":self.突发事件()
            elif 选择=="10":
                try:
                    新价=int(input("新价(1-40):"))
                    if 1<=新价<=40:self.上网价格=新价
                except:pass
            elif 选择=="11":self.时间流逝()
            elif 选择=="12":self.快进2小时()
            elif 选择=="13":self.快进3小时()
            elif 选择=="14":self.生成存档码()
            elif 选择=="15":self.读取存档码()
            elif 选择=="0":
                clear()
                print("👋 再见！")
                break
            input("\n回车继续...")

if __name__ == "__main__":
    游戏 = 网吧大亨终极版()
    游戏.开始游戏()
