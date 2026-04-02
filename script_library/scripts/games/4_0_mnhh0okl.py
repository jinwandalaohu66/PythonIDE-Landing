# 欢迎使用 PythonIDE！如果觉得好用，请给个好评哦～
import random
import json
import hashlib
import time

def clear():
    print("\033c", end="")

class 网吧大亨终极版:
    def __init__(self):
        self.钱 = 1500
        self.天数 = 1
        self.小时 = 10
        self.排队顾客 = 0
        self.口碑 = 100
        self.今日营收 = 0
        self.天气 = random.choice(["☀️晴天", "🌧️小雨", "⛈️大雨", "❄️雪天"])

        # 电脑
        self.电脑 = []
        for _ in range(6):
            self.电脑.append({"等级":1, "状态":0, "计时":0})

        # 街机
        self.街机 = []

        # 网管
        self.网管列表 = []
        self.最大网管数 = 5

        # 垃圾 & 保洁
        self.垃圾 = 0
        self.最大垃圾 = 15
        self.保洁列表 = []
        self.最大保洁 = 3

        # 管理员（防逃票，只能1个，探索时自动工作，回来就辞职）
        self.管理员 = False

        # 探索
        self.正在探索 = False

        # 100条提示
        self.all_tips = [
            "高级电脑收益更高。","配件必须同等级一套。","街机有等级会坏。","电脑街机都会坏。",
            "网管修5次辞职。","排队最多40人。","24小时强制下机。","晴天客人更多。",
            "口碑高客人多。","先买1级电脑最稳。","街机是第二收入。","坏设备要修。",
            "商城直接买高级电脑。","6级电脑收益翻倍。","电脑街机一起开最赚。",
            "网管要多招。","口碑低影响生意。","每天收益很重要。","等级不影响故障率。",
            "一次多接待最赚。","商城高级电脑性价比高。","街机吸引学生。",
            "晚上客流稳。","多招网管效率高。","等级高单价高。","排队满40人就上限。",
            "损坏率低才顺畅。","每天先修设备。","口碑上限150。","大雨客人少。",
            "下雪天客流中等。","新电脑默认空闲。","全套配件同等级。","街机坏了也要修。",
            "想快赚升高级电脑。","多招网管比手动修强。","上机中不会坏。","0点清今日营收。",
            "快进容易坏设备。","商城只卖成套设备。","9级电脑最高。","街机最高6级。",
            "接待前看空闲。","网管最多5人。","网管200元。","逃单会扣钱。",
            "网红打卡爆排队。","猫咪加口碑。","停电全下机。","卫生抽查降口碑。",
            "邻店倒闭送客人。","会员日加口碑。","蓝屏坏多台。","留空闲应对高峰。",
            "快进3小时最爽。","坏设备堆着会炸。","等级越高图标越帅。","每台电脑独立等级。",
            "街机独立等级。","空闲多更灵活。","上机显示计时。","坏设备不影响其他。",
            "商城买电脑送全套。","每次操作都清屏。","菜单简洁。","数值平衡。",
            "高级设备回本快。","优先升电脑。","中等级电脑稳。","支持挂机。",
            "提示都是真实规则。","顾客越多扔垃圾概率越高。","垃圾多降口碑。",
            "保洁80元，清3次辞职。","保洁最多3人。","保洁只管垃圾。","探索能得钱。",
            "探索会遇店铺、怪物。","怪物要扣钱打跑。","离开网吧可能逃票。",
            "管理员超级贵，只能1个。","探索时管理员自动看守。","管理员在绝对不逃票。",
            "回来管理员立刻辞职。","城市探索能发大财。","遇到怪物必须花钱摆平。",
            "探索越久越危险。","店铺能捡小钱。","管理员是防逃票神器。",
            "网管修设备，管理员防逃票。","保洁清垃圾，三者不冲突。",
            "没钱别乱探索。","高级设备配管理员才稳。","这是第95条。",
            "第96条：保洁、网管、管理员各司其职。","第97条：探索有风险。",
            "第98条：管理员只在你离开时工作。","第99条：祝你游戏愉快！",
            "第100条：你已看完所有提示！"
        ]
        self.shown_tips = set()

    # ===================== 提示 =====================
    def show_tip(self):
        clear()
        if len(self.shown_tips) >= len(self.all_tips):
            print("💡 已看完100条提示！")
        else:
            tip = random.choice(self.all_tips)
            while tip in self.shown_tips:
                tip = random.choice(self.all_tips)
            self.shown_tips.add(tip)
            print("💡", tip)
        input("\n回车…")

    # ===================== 保洁 =====================
    def 招募保洁(self):
        clear()
        if len(self.保洁列表) >= self.最大保洁:
            print("❌ 最多3名保洁工")
        elif self.钱 < 80:
            print("❌ 80元")
        else:
            self.钱 -= 80
            self.保洁列表.append(3)
            print("✅ 保洁工到岗")
        input("\n回车…")

    def 清理垃圾(self):
        while self.垃圾 > 0 and self.保洁列表:
            self.垃圾 -= 1
            self.保洁列表[0] -= 1
            if self.保洁列表[0] <= 0:
                self.保洁列表.pop(0)

    # ===================== 网管 =====================
    def 招募网管(self):
        clear()
        if len(self.网管列表) >= self.最大网管数:
            print("❌ 最多5名")
        elif self.钱 < 200:
            print("❌ 200元")
        else:
            self.钱 -= 200
            self.网管列表.append(5)
            print("✅ 网管到岗")
        input("\n回车…")

    # ===================== 管理员（防逃票） =====================
    def 雇佣管理员(self):
        clear()
        if self.管理员:
            print("❌ 已存在管理员")
        elif self.钱 < 1000:
            print("❌ 管理员费用 1000元（超级贵）")
        else:
            self.钱 -= 1000
            self.管理员 = True
            print("✅ 管理员雇佣成功！")
            print("👮 你离开期间自动工作，回来就辞职！")
        input("\n回车…")

    # ===================== 商城 =====================
    def 商城(self):
        while True:
            clear()
            print("🏬商城".center(60,"="))
            print(f"💰{self.钱}")
            print("1:1级电脑200  2:3级500  3:6级1000  4:9级1800")
            print("5:1级街机300 6:3级700 7:6级1300  0:返回")
            print("="*60)
            c = input("选：")
            clear()
            if c == "1" and self.钱 >=200:
                self.钱-=200; self.电脑.append({"等级":1,"状态":0,"计时":0})
                print("✅ 1级电脑")
            elif c == "2" and self.钱>=500:
                self.钱-=500; self.电脑.append({"等级":3,"状态":0,"计时":0})
                print("✅3级")
            elif c == "3" and self.钱>=1000:
                self.钱-=1000; self.电脑.append({"等级":6,"状态":0,"计时":0})
                print("✅6级")
            elif c == "4" and self.钱>=1800:
                self.钱-=1800; self.电脑.append({"等级":9,"状态":0,"计时":0})
                print("✅9级")
            elif c == "5" and self.钱>=300:
                self.钱-=300; self.街机.append({"等级":1,"状态":0})
                print("✅1级街机")
            elif c == "6" and self.钱>=700:
                self.钱-=700; self.街机.append({"等级":3,"状态":0})
                print("✅3级街机")
            elif c == "7" and self.钱>=1300:
                self.钱-=1300; self.街机.append({"等级":6,"状态":0})
                print("✅6级街机")
            elif c == "0":
                break
            input("\n回车…")

    # ===================== 城市探索 =====================
    def 城市探索(self):
        clear()
        print("🚪 你离开网吧，进入城市探索！")
        self.正在探索 = True
        time.sleep(0.3)

        # 探索事件
        r = random.random()
        if r < 0.4:
            钱 = random.randint(50,200)
            self.钱 += 钱
            print(f"🏪 你发现一家小店，捡到 {钱} 元！")
        elif r < 0.75:
            钱 = random.randint(100,350)
            self.钱 += 钱
            print(f"🧧 街头活动获得奖励：{钱} 元！")
        else:
            罚款 = random.randint(150,400)
            if self.钱 >= 罚款:
                self.钱 -= 罚款
                print(f"👹 遇到闹事怪物！花 {罚款} 元摆平！")
            else:
                print("👹 遇到怪物，但你没钱摆平，狼狈逃回！")
        print("🌉 探索结束，返回网吧。")
        self.正在探索 = False

        # 回来管理员直接辞职
        if self.管理员:
            print("👮 管理员任务结束，自动辞职。")
            self.管理员 = False
        input("\n回车…")

    # ===================== 时间核心 =====================
    def 时间流逝(self):
        # 24小时下机
        for 电脑 in self.电脑:
            if 电脑["状态"] == 1:
                电脑["计时"] +=1
                if 电脑["计时"]>=24:
                    电脑["状态"]=0;电脑["计时"]=0

        self.小时 +=1
        if self.小时>=24:
            self.小时=9; self.天数+=1; self.今日营收=0
            self.天气=random.choice(["☀️晴天","🌧️小雨","⛈️大雨","❄️雪天"])

        # 顾客
        在用 = sum(1 for d in self.电脑 if d["状态"]==1) + sum(1 for j in self.街机 if j["状态"]==1)
        来客 = random.randint(1,4)
        if self.天气 == "☀️晴天":来客 +=2
        if self.口碑>120:来客 +=2
        self.排队顾客 = min(self.排队顾客 +来客,40)

        # 垃圾
        概率 = 0.04 + 在用*0.022
        if random.random()<概率 and self.垃圾 < self.最大垃圾:
            self.垃圾 +=1

        # 垃圾影响口碑
        if self.垃圾 >=12:
            self.口碑 = max(self.口碑-1,40)

        # 设备损坏
        if random.random()<0.12:
            空闲 = [d for d in self.电脑 if d["状态"]==0]
            if 空闲: random.choice(空闲)["状态"]=2

        if len(self.街机)>0 and random.random()<0.1:
            空闲 = [j for j in self.街机 if j["状态"]==0]
            if 空闲: random.choice(空闲)["状态"]=2

        # 网管修理
        坏电脑 = [d for d in self.电脑 if d["状态"]==2]
        坏街机 = [j for j in self.街机 if j["状态"]==2]
        while (坏电脑 or 坏街机) and self.网管列表:
            if 坏电脑: 坏电脑.pop(0)["状态"]=0
            else: 坏街机.pop(0)["状态"]=0
            self.网管列表[0] -=1
            if self.网管列表[0]==0:
                self.网管列表.pop(0)

        # 保洁清垃圾
        self.清理垃圾()

        # 逃票（不在且无管理员才逃票）
        if self.正在探索 and not self.管理员:
            if random.random()<0.35:
                损失 = random.randint(40,180)
                if self.钱 >=损失:
                    self.钱 -=损失
                    print(f"💸 你不在，有顾客逃票！损失 {损失} 元！")

    def 快进2h(self):
        print("\n⏩ 快进2小时")
        self.时间流逝(); self.时间流逝()
    def 快进3h(self):
        print("\n⏩ 快进3小时")
        self.时间流逝(); self.时间流逝(); self.时间流逝()

    # ===================== 接待 =====================
    def 接待电脑(self):
        空闲 = [d for d in self.电脑 if d["状态"]==0]
        if not 空闲 or self.排队顾客<=0:
            print("❌ 无法接待")
            return
        台数 = min(len(空闲), self.排队顾客)
        收入 = 0
        for i in range(台数):
            空闲[i]["状态"]=1
            收入 += 6 + (空闲[i]["等级"]-1)*4
        self.钱 +=收入
        self.今日营收 +=收入
        self.排队顾客 -=台数
        print(f"✅ 接待{台数}台，收入{收入}")

    def 接待街机(self):
        空闲 = [j for j in self.街机 if j["状态"]==0]
        if not 空闲:
            print("❌ 无空闲")
            return
        台数 = min(len(空闲),3)
        收入 =0
        for i in range(台数):
            空闲[i]["状态"]=1
            收入 += 10 + (空闲[i]["等级"]-1)*5
        self.钱 +=收入
        self.今日营收 +=收入
        print(f"✅ 街机收入{收入}")

    # ===================== 界面 =====================
    def 画界面(self):
        clear()
        print("🏪【网吧大亨·终极完整版】".center(68,"="))
        print()
        print("🖥️电脑：",end="")
        for d in self.电脑:
            if d["状态"]==0:print(f"🖥️Lv{d['等级']}",end=" ")
            elif d["状态"]==1:print(f"💻Lv{d['等级']}",end=" ")
            else:print(f"🔧Lv{d['等级']}",end=" ")
        print()
        print("🎮街机：",end="")
        if not self.街机:print("无",end="")
        for j in self.街机:
            if j["状态"]==0:print(f"🕹️Lv{j['等级']}",end=" ")
            elif j["状态"]==1:print(f"🎮Lv{j['等级']}",end=" ")
            else:print(f"⚠️Lv{j['等级']}",end=" ")
        print()
        print(f"🗑️垃圾：{'🧻'*self.垃圾} {self.垃圾}/{self.最大垃圾}")
        print("-"*68)
        顾客图标 = "👤"*min(self.排队顾客,12)
        if self.排队顾客>12:顾客图标+=f"+{self.排队顾客-12}"
        print(f"👥排队：{顾客图标}  💰金钱：{self.钱}")
        print(f"🌟口碑：{self.口碑} {self.天气} 📊今日：{self.今日营收}")
        print(f"👨💻网管：{len(self.网管列表)}/5 🧹保洁：{len(self.保洁列表)}/3 👮管理员：{'在岗' if self.管理员 else '无'}")
        print("="*68)

    # ===================== 主菜单 =====================
    def 开始游戏(self):
        while True:
            self.画界面()
            print("\n【主菜单】")
            print(" 1.👥接待电脑  2.🎮接待街机  3.🏬商城      4.👨💻招网管")
            print(" 5.🧹招保洁    6.👮雇管理员  7.🌆城市探索  8.🕒快进1h")
            print(" 9.⏩快进2h   10.⏩快进3h  11.💡提示     12.💾存档")
            print("13.📂读档     0.🚪退出")
            选 = input("\n选择：").strip()
            clear()

            if 选=="1": self.接待电脑()
            elif 选=="2": self.接待街机()
            elif 选=="3": self.商城()
            elif 选=="4": self.招募网管()
            elif 选=="5": self.招募保洁()
            elif 选=="6": self.雇佣管理员()
            elif 选=="7": self.城市探索()
            elif 选=="8": self.时间流逝()
            elif 选=="9": self.快进2h()
            elif 选=="10": self.快进3h()
            elif 选=="11": self.show_tip()
            elif 选=="12":
                data = json.dumps(self.__dict__, ensure_ascii=False)
                print("存档数据：\n",data)
                input("回车…")
            elif 选=="13":
                s=input("读档数据：")
                self.__dict__.update(json.loads(s))
                input("成功…")
            elif 选=="0":
                clear()
                print("👋 再见！")
                break
            input("\n回车继续…")

if __name__ == "__main__":
    game = 网吧大亨终极版()
    game.开始游戏()