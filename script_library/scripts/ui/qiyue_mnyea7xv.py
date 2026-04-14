import webbrowser
import ui
import base64

# 这里存放8ca58e770b78c0e7a7063c279ae0a11dd45962953fae4c2130add25a3d172020ce94c002b2b6e62a47d3
ENCODED_CARD = "cWl5dWU="   # 如果你卡密不同，把引号里的换成你上一步得到的码

def open_iqy(sender):
    webbrowser.open('https://www.iqiyi.com')

def open_tx(sender):
    webbrowser.open('https://v.qq.com')

def open_yq(sender):
    webbrowser.open('https://www.youku.com/')

def play_vip(sender):
    url = 'https://jx.xmflv.cc/?url='
    video = sender.superview['entry'].text
    webbrowser.open(url + video)

def clear_text(sender):
    sender.superview['entry'].text = ''

def verify_card(sender):
    card_entry = sender.superview['card_entry']
    input_card = card_entry.text.strip()
    # 解码存储的 Base64，得到真实卡密
    correct_card = base64.b64decode(ENCODED_CARD).decode()
    if input_card == correct_card:
        play_btn = sender.superview['play_btn']
        play_btn.enabled = True
        ui.alert('验证成功', '卡密正确，现在可以使用VIP播放功能了！', '好的')
        card_entry.text = ''
    else:
        ui.alert('验证失败', '卡密错误，无法使用VIP播放功能。', '重试')

if __name__ == '__main__':
    v = ui.View()
    v.name = 'VIP视频破解软件'
    v.background_color = 'white'
    v.frame = (0, 0, 480, 260)

    # 视频链接行
    label_movie_link = ui.Label()
    label_movie_link.text = '网页视频链接：'
    label_movie_link.frame = (20, 20, 100, 30)
    v.add_subview(label_movie_link)

    entry_movie_link = ui.TextField()
    entry_movie_link.frame = (125, 20, 260, 30)
    entry_movie_link.border_width = 1
    entry_movie_link.border_color = (0.8, 0.8, 0.8)
    entry_movie_link.corner_radius = 5
    entry_movie_link.name = 'entry'
    v.add_subview(entry_movie_link)

    btn_clear = ui.Button()
    btn_clear.title = '清空'
    btn_clear.frame = (400, 20, 50, 30)
    btn_clear.background_color = (0.9, 0.9, 0.9)
    btn_clear.corner_radius = 5
    btn_clear.action = clear_text
    v.add_subview(btn_clear)

    # 平台按钮行
    btn_iqy = ui.Button()
    btn_iqy.title = '爱奇艺'
    btn_iqy.frame = (25, 70, 80, 40)
    btn_iqy.background_color = (0.2, 0.6, 1.0)
    btn_iqy.tint_color = 'white'
    btn_iqy.corner_radius = 8
    btn_iqy.action = open_iqy
    v.add_subview(btn_iqy)

    btn_tx = ui.Button()
    btn_tx.title = '腾讯视频'
    btn_tx.frame = (125, 70, 80, 40)
    btn_tx.background_color = (0.0, 0.8, 0.4)
    btn_tx.tint_color = 'white'
    btn_tx.corner_radius = 8
    btn_tx.action = open_tx
    v.add_subview(btn_tx)

    btn_youku = ui.Button()
    btn_youku.title = '优酷视频'
    btn_youku.frame = (225, 70, 80, 40)
    btn_youku.background_color = (1.0, 0.3, 0.2)
    btn_youku.tint_color = 'white'
    btn_youku.corner_radius = 8
    btn_youku.action = open_yq
    v.add_subview(btn_youku)

    btn_play = ui.Button()
    btn_play.title = '播放VIP视频'
    btn_play.frame = (325, 70, 125, 40)
    btn_play.background_color = (0.6, 0.2, 0.8)
    btn_play.tint_color = 'white'
    btn_play.corner_radius = 8
    btn_play.action = play_vip
    btn_play.enabled = False
    btn_play.name = 'play_btn'
    v.add_subview(btn_play)

    # 提示标签
    lab_remind = ui.Label()
    lab_remind.text = '提示：将视频链接复制到框内，点击播放VIP视频'
    lab_remind.frame = (50, 125, 400, 20)
    lab_remind.text_color = (0.4, 0.4, 0.4)
    lab_remind.alignment = ui.ALIGN_CENTER
    v.add_subview(lab_remind)

    # 卡密验证行
    label_card = ui.Label()
    label_card.text = '卡密：'
    label_card.frame = (50, 155, 50, 30)
    v.add_subview(label_card)

    entry_card = ui.TextField()
    entry_card.frame = (100, 155, 200, 30)
    entry_card.border_width = 1
    entry_card.border_color = (0.8, 0.8, 0.8)
    entry_card.corner_radius = 5
    entry_card.placeholder = '输入卡密以解锁VIP播放'
    entry_card.name = 'card_entry'
    v.add_subview(entry_card)

    btn_verify = ui.Button()
    btn_verify.title = '验证卡密'
    btn_verify.frame = (320, 155, 100, 30)
    btn_verify.background_color = (0.9, 0.5, 0.2)
    btn_verify.tint_color = 'white'
    btn_verify.corner_radius = 5
    btn_verify.action = verify_card
    v.add_subview(btn_verify)

    # 作者标签
    author_label = ui.Label()
    author_label.text = '作者：七月'
    author_label.frame = (0, 205, 480, 25)
    author_label.text_color = (0.5, 0.5, 0.5)
    author_label.alignment = ui.ALIGN_CENTER
    author_label.font = ('<system>', 12)
    v.add_subview(author_label)

    v.present('sheet')