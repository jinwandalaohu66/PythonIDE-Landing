# 欢迎使用 PythonIDE！如果觉得好用，请给个好评哦～
"""
骚扰电话与异常短信检测防护工具（增强版）
功能：号码识别、黑名单管理、短信内容分析、拦截记录、风险评分
"""

import re
import json
import time
from datetime import datetime
from typing import List, Dict, Tuple
import ui

# ========== 数据存储 ==========
class ProtectionData:
    """防护数据管理"""
    
    def __init__(self):
        self.blacklist_file = "spam_blacklist.json"
        self.records_file = "spam_records.json"
        
        # ========== 运营商官方号码白名单 ==========
        self.official_whitelist = [
            "10086", "10010", "10000",  # 运营商客服
            "95588", "95533", "95568", "95599", "95559",  # 银行客服
            "95555", "95566", "95577", "95588", "95599",
            "12306", "12315", "12345", "12333",  # 政府服务
            "110", "120", "119", "122",  # 紧急服务
        ]
        
        # ========== 扩展的骚扰号段列表 ==========
        # 商业服务号段（高频骚扰）
        self.spam_service_prefixes = [
            "95",    # 商业服务号段（95xxx，如95188、955xx等）
            "400",   # 企业客服号段（常被滥用）
            "800",   # 企业免费客服号段
            "950",   # 商业服务扩展号段
            "96",    # 客服号段
        ]
        
        # 短信通道号段
        self.sms_channel_prefixes = [
            "1069",  # 三网短信通道
            "1065",  # 移动短信通道
            "1066",  # 联通短信通道
            "1067",  # 电信短信通道
            "1068",  # 跨网短信通道
            "106",   # 通用短信通道
            "10690", "10691", "10692", "10693",  # 细分短信通道
        ]
        
        # 虚拟运营商号段（高频诈骗/骚扰）
        self.virtual_operator_prefixes = [
            "170",   # 虚拟运营商（1700移动、1705电信、1709联通）
            "171",   # 联通虚拟运营商（高频诈骗）
            "162",   # 移动虚拟运营商
            "165",   # 移动虚拟运营商
            "166",   # 联通虚拟运营商
            "167",   # 联通虚拟运营商
            "175",   # 联通新号段
            "176",   # 联通新号段
            "177",   # 电信新号段
            "178",   # 移动新号段
            "145",   # 移动数据卡号段
            "149",   # 电信数据卡号段
            "153",   # 电信号段
            "180", "181", "182", "183", "184",  # 电信号段
            "185", "186", "187", "188", "189",  # 联通号段
        ]
        
        # 国际来电号段（高风险诈骗）
        self.international_prefixes = [
            "+",     # 国际来电标识
            "00",    # 国际来电前缀
            "001",   # 美国/加拿大
            "008",   # 东亚地区
            "0081",  # 日本
            "0082",  # 韩国
            "0086",  # 中国（境外拨打）
            "0088",  # 国际卫星电话
            "009",   # 南亚/中东地区
            "0044",  # 英国
            "0091",  # 印度
            "0060",  # 马来西亚
            "0065",  # 新加坡
            "0066",  # 泰国
            "0085",  # 朝鲜
            "0086",  # 中国大陆
            "0087",  # 卫星电话
        ]
        
        # 新开通号段（可能被滥用）
        self.new_prefixes = [
            "190",   # 电信新号段
            "191",   # 电信新号段
            "192",   # 电信新号段
            "193",   # 电信新号段
            "195",   # 移动新号段
            "196",   # 联通新号段
            "197",   # 移动新号段
            "198",   # 移动新号段
            "199",   # 电信新号段
        ]
        
        # 特殊服务号段
        self.special_service_prefixes = [
            "110",   # 公安报警（不应收到来电）
            "120",   # 急救中心
            "122",   # 交通事故
            "123",   # 政府服务热线（12345、12315等）
            "96",    # 客服号段
        ]
        
        # ========== 高频骚扰号码特征库 ==========
        self.known_spam_patterns = [
            # 以特定数字结尾的推销号码
            r"^\d{10}8$",  # 以8结尾
            r"^\d{10}6$",  # 以6结尾
            # 连续重复数字
            r"(\d)\1{4,}",  # 5个以上相同数字
            # 顺子号码
            r"0123456|1234567|2345678|3456789",
            r"9876543|8765432|7654321|6543210",
        ]
        
        # ========== 骚扰关键词分类 ==========
        self.spam_keywords = {
            "贷款理财": [
                "贷款", "借款", "放款", "额度", "审批",
                "信用卡", "提额", "套现", "分期",
                "理财", "投资", "收益", "赚钱", "基金",
                "股票", "期货", "外汇", "比特币",
                "保险", "理赔", "退保", "续保",
                "抵押", "车贷", "房贷", "网贷",
                "借呗", "花呗", "微粒贷", "京东白条",
            ],
            "诈骗诱导": [
                "中奖", "恭喜", "领取", "红包", "奖金",
                "返利", "返现", "优惠", "折扣", "特价",
                "免费", "赠送", "礼品", "福利",
                "刷单", "兼职", "日赚", "月入",
                "转账", "汇款", "退款", "退税",
                "验证码", "密码", "账号", "异常",
                "冻结", "解冻", "安全", "风险",
                "公安局", "法院", "传票", "逮捕",
            ],
            "房产中介": [
                "房产", "售楼", "楼盘", "首付", "房贷",
                "房源", "看房", "买房", "卖房",
                "中介", "经纪人", "佣金",
                "写字楼", "商铺", "别墅", "公寓",
            ],
            "教育培训": [
                "培训", "课程", "学习", "提升",
                "学历", "考研", "考公", "考证",
                "英语", "雅思", "托福",
                "早教", "辅导", "补习", "网课",
            ],
            "医疗推销": [
                "药品", "保健品", "医疗器械",
                "美容", "整形", "减肥", "瘦身",
                "治疗", "康复", "体检",
                "医院", "门诊", "专科",
            ],
            "催收威胁": [
                "催收", "欠款", "逾期", "还款",
                "起诉", "法院", "律师", "传票",
                "征信", "黑名单", "失信",
                "上门", "通知", "最后期限",
            ],
            "退订标识": [
                "退订回T", "回复TD", "回N退订",
                "拒收请回", "退订请回",
                "回T退订", "回TD退订",
            ],
            "赌博推广": [
                "彩票", "投注", "博彩", "赌场",
                "百家乐", "牛牛", "炸金花",
                "六合彩", "时时彩", "PK10",
            ],
        }
        
        # ========== 钓鱼链接特征 ==========
        self.phishing_patterns = [
            # 可疑域名后缀
            r'http[s]?://[^\s]+\.(xyz|top|wang|win|loan|vip|club|online|site|website|space|live|pro|work|click|link|info|biz|me|pw|cc|tk|ml|ga|cf|gq|fm|am|io)',
            # 包含长数字串的链接（短链接特征）
            r'http[s]?://[^\s]*[0-9]{6,}[^\s]*',
            # 多级短横线域名
            r'http[s]?://[^\s]*-[^\s]*-[^\s]*-[^\s]*\.',
            # IP地址直连
            r'http[s]?://[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',
            # 短链接服务
            r'http[s]?://[^\s]*(bit\.ly|t\.cn|dwz\.cn|url\.cn|tinyurl|shorturl|u\.cn)',
            # 可疑参数
            r'http[s]?://[^\s]*\?(.*?&)?(phone|mobile|tel|account|pwd|pass)=',
        ]
        
        # ========== 号码归属地号段映射 ==========
        self.location_prefixes = {
            # 北京
            "130": "北京", "131": "北京", "132": "北京", "133": "北京",
            "135": "北京", "136": "北京", "137": "北京", "138": "北京",
            "139": "北京", "150": "北京", "151": "北京", "152": "北京",
            "153": "北京", "155": "北京", "156": "北京", "157": "北京",
            "158": "北京", "159": "北京", "180": "北京", "181": "北京",
            "182": "北京", "183": "北京", "184": "北京", "185": "北京",
            "186": "北京", "187": "北京", "188": "北京", "189": "北京",
            # 上海
            "134": "上海", "135": "上海", "136": "上海", "137": "上海",
            "138": "上海", "139": "上海", "150": "上海", "151": "上海",
            "152": "上海", "153": "上海", "155": "上海", "156": "上海",
            "157": "上海", "158": "上海", "159": "上海", "180": "上海",
            "181": "上海", "182": "上海", "183": "上海", "184": "上海",
            "185": "上海", "186": "上海", "187": "上海", "188": "上海",
            "189": "上海",
        }
        
        # 加载数据
        self.blacklist = self.load_blacklist()
        self.records = self.load_records()
    
    def load_blacklist(self) -> Dict:
        """加载黑名单"""
        try:
            with open(self.blacklist_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"numbers": {}, "keywords": self.spam_keywords}
    
    def save_blacklist(self):
        """保存黑名单"""
        with open(self.blacklist_file, 'w', encoding='utf-8') as f:
            json.dump(self.blacklist, f, ensure_ascii=False, indent=2)
    
    def load_records(self) -> List:
        """加载拦截记录"""
        try:
            with open(self.records_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_records(self):
        """保存拦截记录"""
        with open(self.records_file, 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)
    
    def add_to_blacklist(self, number: str, reason: str = "", spam_type: str = ""):
        """添加号码到黑名单"""
        self.blacklist["numbers"][number] = {
            "reason": reason,
            "spam_type": spam_type,
            "add_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_blacklist()
    
    def remove_from_blacklist(self, number: str):
        """从黑名单移除号码"""
        if number in self.blacklist["numbers"]:
            del self.blacklist["numbers"][number]
            self.save_blacklist()
    
    def add_record(self, number: str, content: str, spam_type: str, risk_level: str, risk_score: int = 0):
        """添加拦截记录"""
        record = {
            "number": number,
            "content": content[:100],
            "type": spam_type,
            "risk": risk_level,
            "score": risk_score,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.records.insert(0, record)
        self.records = self.records[:100]
        self.save_records()

# ========== 增强版检测引擎 ==========
class SpamDetector:
    """骚扰检测引擎（增强版）"""
    
    def __init__(self, data: ProtectionData):
        self.data = data
    
    def _check_number_pattern(self, number: str) -> Tuple[int, List[str]]:
        """
        检测号码模式异常
        返回: (风险分数, 详情列表)
        """
        score = 0
        details = []
        digits = re.sub(r'[^\d]', '', number)
        
        if len(digits) < 5:
            return score, details
        
        # 检测连续重复数字（如111111）
        for i in range(len(digits) - 4):
            if len(set(digits[i:i+5])) == 1:
                score += 25
                details.append(f"⚠ 连续重复数字: {digits[i:i+5]}...")
                break
        
        # 检测顺子号码（如123456、987654）
        shunzi_up = ["0123456", "1234567", "2345678", "3456789"]
        shunzi_down = ["9876543", "8765432", "7654321", "6543210"]
        for pattern in shunzi_up + shunzi_down:
            if pattern in digits:
                score += 20
                details.append(f"⚠ 顺子号码特征: {pattern}")
                break
        
        # 检测AABB模式（如1122、8899）
        aabb_pattern = re.compile(r'(\d)\1(\d)\2')
        if aabb_pattern.search(digits):
            score += 10
            details.append("ℹ AABB模式号码")
        
        # 检测ABAB模式（如1212、8989）
        abab_pattern = re.compile(r'(\d)(\d)\1\2')
        if abab_pattern.search(digits):
            score += 10
            details.append("ℹ ABAB模式号码")
        
        # 检测号码长度异常
        if len(digits) > 13:
            score += 15
            details.append(f"⚠ 号码长度异常: {len(digits)}位")
        elif len(digits) < 7 and len(digits) >= 5:
            score += 20
            details.append(f"⚠ 短号码: {len(digits)}位")
        
        # 检测全偶数或全奇数结尾
        tail = digits[-4:] if len(digits) >= 4 else digits
        if tail and all(int(d) % 2 == 0 for d in tail):
            score += 5
            details.append("ℹ 尾号全偶数")
        elif tail and all(int(d) % 2 == 1 for d in tail):
            score += 5
            details.append("ℹ 尾号全奇数")
        
        return score, details
    
    def _check_known_spam(self, number: str) -> Tuple[int, List[str]]:
        """
        检测已知骚扰模式
        返回: (风险分数, 详情列表)
        """
        score = 0
        details = []
        digits = re.sub(r'[^\d]', '', number)
        
        for pattern in self.data.known_spam_patterns:
            if re.search(pattern, digits):
                score += 30
                details.append(f"⚠ 匹配已知骚扰模式")
                break
        
        return score, details
    
    def analyze_number(self, number: str) -> Tuple[bool, str, str, int, List[str]]:
        """
        分析电话号码（增强版）
        返回: (是否骚扰, 类型描述, 风险等级, 风险分数, 检测详情列表)
        """
        details = []
        risk_score = 0
        spam_type = ""
        
        # 清理号码
        clean_number = re.sub(r'[^\d+]', '', number)
        digits_only = re.sub(r'[^\d]', '', clean_number)
        
        # 检查白名单
        for official in self.data.official_whitelist:
            if digits_only == official or digits_only.startswith(official):
                details.append(f"✓ 运营商/官方号码: {official}")
                return False, "官方号码", "安全", 0, details
        
        # 检查黑名单
        if clean_number in self.data.blacklist.get("numbers", {}):
            info = self.data.blacklist["numbers"][clean_number]
            details.append(f"✓ 在黑名单中: {info.get('reason', '未知原因')}")
            return True, info.get("spam_type", "黑名单号码"), "高危", 100, details
        
        # 检查国际来电
        for prefix in self.data.international_prefixes:
            if clean_number.startswith(prefix):
                risk_score += 60
                spam_type = "国际诈骗"
                details.append(f"⚠ 国际/境外来电 (前缀: {prefix})")
                break
        
        # 检查商业服务号段
        for prefix in self.data.spam_service_prefixes:
            if clean_number.startswith(prefix):
                risk_score += 40
                if not spam_type:
                    spam_type = "商业推销"
                details.append(f"⚠ 商业服务号段 (前缀: {prefix})")
                break
        
        # 检查短信通道
        for prefix in self.data.sms_channel_prefixes:
            if clean_number.startswith(prefix):
                risk_score += 30
                if not spam_type:
                    spam_type = "短信通道"
                details.append(f"⚠ 短信通道号段 (前缀: {prefix})")
                break
        
        # 检查虚拟运营商
        for prefix in self.data.virtual_operator_prefixes:
            if clean_number.startswith(prefix):
                risk_score += 35
                if not spam_type:
                    spam_type = "虚拟运营商"
                details.append(f"⚠ 虚拟运营商号段 (前缀: {prefix})")
                break
        
        # 检查新号段
        for prefix in self.data.new_prefixes:
            if clean_number.startswith(prefix):
                risk_score += 15
                details.append(f"ℹ 新开通号段 (前缀: {prefix})")
                break
        
        # 号码模式分析
        pattern_score, pattern_details = self._check_number_pattern(clean_number)
        if pattern_score > 0:
            risk_score += pattern_score
            details.extend(pattern_details)
            if not spam_type:
                spam_type = "异常号码"
        
        # 已知骚扰模式检测
        known_score, known_details = self._check_known_spam(clean_number)
        if known_score > 0:
            risk_score += known_score
            details.extend(known_details)
            if not spam_type:
                spam_type = "骚扰号码"
        
        # 判断风险等级
        if risk_score >= 70:
            risk_level = "高危"
        elif risk_score >= 45:
            risk_level = "中危"
        elif risk_score >= 25:
            risk_level = "低危"
        else:
            risk_level = "正常"
        
        is_spam = risk_score >= 30
        if not spam_type:
            spam_type = "正常号码"
        
        return is_spam, spam_type, risk_level, risk_score, details
    
    def analyze_sms(self, content: str) -> Tuple[bool, str, str, int, List[str]]:
        """
        分析短信内容
        返回: (是否骚扰, 类型描述, 风险等级, 风险分数, 检测详情列表)
        """
        details = []
        risk_score = 0
        spam_type = ""
        
        # 检查关键词
        matched_categories = []
        for category, keywords in self.data.spam_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    matched_categories.append(category)
                    risk_score += 15
                    break
        
        if matched_categories:
            spam_type = matched_categories[0]
            details.append(f"⚠ 匹配关键词分类: {', '.join(matched_categories)}")
        
        # 检查钓鱼链接
        for pattern in self.data.phishing_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                risk_score += 50
                spam_type = "钓鱼短信"
                details.append("⚠ 检测到可疑链接")
                break
        
        # 检查退订标识
        for keyword in self.data.spam_keywords.get("退订标识", []):
            if keyword in content:
                risk_score += 20
                details.append(f"ℹ 包含退订标识: {keyword}")
                break
        
        # 判断风险等级
        if risk_score >= 60:
            risk_level = "高危"
        elif risk_score >= 40:
            risk_level = "中危"
        elif risk_score >= 20:
            risk_level = "低危"
        else:
            risk_level = "正常"
        
        is_spam = risk_score >= 30
        if not spam_type:
            spam_type = "正常短信"
        
        return is_spam, spam_type, risk_level, risk_score, details

# ========== UI界面 ==========
class SpamProtectionUI:
    """骚扰防护UI"""
    
    def __init__(self):
        self.data = ProtectionData()
        self.detector = SpamDetector(self.data)
        self.build_ui()
    
    def build_ui(self):
        """构建界面"""
        self.view = ui.View(name="骚扰防护", background_color="#f5f5f5")
        self.view.flex = "WH"
        
        # 导航栏确定按钮
        done_btn = ui.ButtonItem(title="关闭", action=self.on_done)
        self.view.right_button_items = [done_btn]
        
        # 输入区域
        input_card = ui.View(background_color="white", corner_radius=10)
        input_card.frame = (10, 10, self.view.width - 20, 130)
        input_card.flex = "W"
        input_card.border_width = 1
        input_card.border_color = "#e0e0e0"
        self.view.add_subview(input_card)
        
        # 号码输入
        number_label = ui.Label(text="电话号码:", font=("<system>", 14))
        number_label.frame = (15, 15, 100, 25)
        input_card.add_subview(number_label)
        
        self.number_field = ui.TextField(placeholder="输入要检测的电话号码", font=("<system>", 14))
        self.number_field.frame = (15, 45, input_card.width - 30, 36)
        self.number_field.flex = "W"
        self.number_field.border_width = 1
        self.number_field.border_color = "#ccc"
        self.number_field.corner_radius = 8
        self.number_field.clear_button_mode = 3
        input_card.add_subview(self.number_field)
        
        # 确认查询按钮
        self.confirm_btn = ui.Button(title="确认查询", font=("<system>", 15, "bold"), background_color="#34C759", tint_color="white")
        self.confirm_btn.frame = (15, 93, input_card.width - 30, 31)
        self.confirm_btn.flex = "W"
        self.confirm_btn.corner_radius = 8
        self.confirm_btn.action = self.on_confirm_query
        input_card.add_subview(self.confirm_btn)
        
        # 按钮区域1
        btn_card1 = ui.View(background_color="white", corner_radius=10)
        btn_card1.frame = (10, 150, self.view.width - 20, 50)
        btn_card1.flex = "W"
        self.view.add_subview(btn_card1)
        
        # 检测按钮
        detect_btn = ui.Button(title="检测分析", font=("<system>", 15, "bold"), background_color="#007AFF", tint_color="white")
        detect_btn.frame = (15, 10, (btn_card1.width - 40) / 2, 36)
        detect_btn.flex = "W"
        detect_btn.corner_radius = 8
        detect_btn.action = self.on_detect
        btn_card1.add_subview(detect_btn)
        
        # 加入黑名单按钮
        blacklist_btn = ui.Button(title="加入黑名单", font=("<system>", 15, "bold"), background_color="#FF3B30", tint_color="white")
        blacklist_btn.frame = (25 + (btn_card1.width - 40) / 2, 10, (btn_card1.width - 40) / 2, 36)
        blacklist_btn.flex = "W"
        blacklist_btn.corner_radius = 8
        blacklist_btn.action = self.on_add_blacklist
        btn_card1.add_subview(blacklist_btn)
        
        # 按钮区域2
        btn_card2 = ui.View(background_color="white", corner_radius=10)
        btn_card2.frame = (10, 210, self.view.width - 20, 50)
        btn_card2.flex = "W"
        self.view.add_subview(btn_card2)
        
        # 查看黑名单按钮
        view_blacklist_btn = ui.Button(title="查看黑名单", font=("<system>", 15, "bold"), background_color="#5856D6", tint_color="white")
        view_blacklist_btn.frame = (15, 10, (btn_card2.width - 40) / 2, 36)
        view_blacklist_btn.flex = "W"
        view_blacklist_btn.corner_radius = 8
        view_blacklist_btn.action = self.on_view_blacklist
        btn_card2.add_subview(view_blacklist_btn)
        
        # 清除结果按钮
        clear_btn = ui.Button(title="清除结果", font=("<system>", 15, "bold"), background_color="#8E8E93", tint_color="white")
        clear_btn.frame = (25 + (btn_card2.width - 40) / 2, 10, (btn_card2.width - 40) / 2, 36)
        clear_btn.flex = "W"
        clear_btn.corner_radius = 8
        clear_btn.action = self.on_clear
        btn_card2.add_subview(clear_btn)
        
        # 结果区域
        result_card = ui.View(background_color="white", corner_radius=10)
        result_card.frame = (10, 270, self.view.width - 20, 180)
        result_card.flex = "WH"
        result_card.border_width = 1
        result_card.border_color = "#e0e0e0"
        self.view.add_subview(result_card)
        
        result_label = ui.Label(text="检测结果:", font=("<system>", 14))
        result_label.frame = (15, 10, 100, 25)
        result_card.add_subview(result_label)
        
        self.result_textview = ui.TextView(font=("<system>", 13), editable=False)
        self.result_textview.frame = (15, 40, result_card.width - 30, result_card.height - 100)
        self.result_textview.flex = "WH"
        self.result_textview.border_width = 1
        self.result_textview.border_color = "#e0e0e0"
        self.result_textview.corner_radius = 8
        result_card.add_subview(self.result_textview)
        
        # 底部确认按钮
        confirm_btn = ui.Button(title="确 认 关 闭", font=("<system>", 16, "bold"), background_color="#34C759", tint_color="white")
        confirm_btn.frame = (10, self.view.height - 60, self.view.width - 20, 44)
        confirm_btn.flex = "TY"
        confirm_btn.corner_radius = 10
        confirm_btn.action = self.on_done
        self.view.add_subview(confirm_btn)
    
    def on_done(self, sender):
        """确定按钮事件"""
        self.view.close()
    
    def on_confirm_query(self, sender):
        """确认查询按钮点击事件"""
        number = self.number_field.text.strip()
        if not number:
            self.result_textview.text = "请先输入电话号码"
            return
        self.on_detect(sender)
    
    def on_detect(self, sender):
        """检测按钮事件"""
        number = self.number_field.text.strip()
        
        if not number:
            self.result_textview.text = "请输入电话号码"
            return
        
        result_lines = []
        result_lines.append("=" * 40)
        result_lines.append(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        result_lines.append("=" * 40)
        
        # 号码检测
        is_spam, spam_type, risk_level, risk_score, details = self.detector.analyze_number(number)
        result_lines.append(f"\n【号码检测】")
        result_lines.append(f"号码: {number}")
        result_lines.append(f"类型: {spam_type}")
        result_lines.append(f"风险等级: {risk_level}")
        result_lines.append(f"风险分数: {risk_score}")
        result_lines.append(f"判定: {'⚠ 骚扰号码' if is_spam else '✓ 正常号码'}")
        if details:
            result_lines.append("\n检测详情:")
            for d in details:
                result_lines.append(f"  {d}")
        
        self.result_textview.text = "\n".join(result_lines)
    
    def on_add_blacklist(self, sender):
        """加入黑名单"""
        number = self.number_field.text.strip()
        if not number:
            self.result_textview.text = "请输入要加入黑名单的号码"
            return
        
        clean_number = re.sub(r'[^\d+]', '', number)
        self.data.add_to_blacklist(clean_number, "用户手动添加", "黑名单号码")
        self.result_textview.text = f"已将 {clean_number} 加入黑名单"
    
    def on_view_blacklist(self, sender):
        """查看黑名单"""
        numbers = self.data.blacklist.get("numbers", {})
        if not numbers:
            self.result_textview.text = "黑名单为空"
            return
        
        result_lines = ["=" * 40, "黑名单列表", "=" * 40]
        for num, info in numbers.items():
            result_lines.append(f"\n号码: {num}")
            result_lines.append(f"  类型: {info.get('spam_type', '未知')}")
            result_lines.append(f"  原因: {info.get('reason', '无')}")
            result_lines.append(f"  添加时间: {info.get('add_time', '未知')}")
        
        result_lines.append(f"\n共 {len(numbers)} 个号码")
        self.result_textview.text = "\n".join(result_lines)
    
    def on_clear(self, sender):
        """清除结果"""
        self.result_textview.text = ""
        self.number_field.text = ""
    
    def show(self):
        """显示界面"""
        self.view.present("sheet")

# ========== 主程序 ==========
if __name__ == "__main__":
    app = SpamProtectionUI()
    app.show()