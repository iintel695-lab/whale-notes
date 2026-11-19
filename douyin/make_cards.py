#!/usr/bin/env python3
"""把笔记渲染成抖音竖版图文卡片（1080x1920）。"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SC = 2

BG = (244, 248, 253)
INK = (27, 58, 92)
INK2 = (84, 104, 126)
BLUE = (47, 123, 224)
WHITE = (255, 255, 255)


def F(path, size):
    return ImageFont.truetype(path, size, index=SC)


def canvas():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # 顶部色带
    d.rectangle([0, 0, W, 12], fill=BLUE)
    return img, d


def wrap(d, text, font, maxw):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if d.textlength(cur + ch, font=font) > maxw:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def footer(d, label="#鲸鱼笔记"):
    f = F(REG, 34)
    d.text((90, H - 120), label, font=f, fill=INK2)
    d.text((W - 90 - d.textlength("github.com/iintel695-lab/whale-notes", font=f), H - 120),
           "github.com/iintel695-lab/whale-notes", font=f, fill=INK2)


def cover():
    img, d = canvas()
    d.text((90, 170), "鲸鱼笔记", font=F(BOLD, 52), fill=BLUE)
    d.text((90, 250), "刷了几百条短视频之后", font=F(REG, 44), fill=INK2)
    lines = ["90% 的短视频，", "看标题就该划走"]
    y = 400
    for ln in lines:
        d.text((90, y), ln, font=F(BOLD, 104), fill=INK)
        y += 150
    # 分隔
    d.rectangle([90, y + 40, 250, y + 50], fill=BLUE)
    body = "判断标准只有一条：\n看完之后我能不能多做一件事。"
    yy = y + 110
    for ln in wrap(d, body, F(REG, 56), W - 180):
        d.text((90, yy), ln, font=F(REG, 56), fill=INK2)
        yy += 92
    # 右下形象图
    try:
        m = Image.open("/home/ubuntu/whale-notes/assets/meme-skip.png").convert("RGBA")
        m = m.crop((10, 10, m.width - 10, m.height - 10))
        m.thumbnail((470, 470))
        img.paste(m, (W - m.width - 60, H - m.height - 230), m)
    except Exception:
        pass
    footer(d)
    return img


def card(idx, total, title, body):
    img, d = canvas()
    d.text((90, 170), f"{idx:02d} / {total:02d}", font=F(BOLD, 44), fill=BLUE)
    y = 300
    for ln in wrap(d, title, F(BOLD, 92), W - 180):
        d.text((90, y), ln, font=F(BOLD, 92), fill=INK)
        y += 130
    # 大块留白用白卡片撑住，别让整张图空掉
    d.rounded_rectangle([60, 620, W - 60, 1420], radius=36, fill=WHITE)
    d.rounded_rectangle([110, 700, 138, 890], radius=14, fill=BLUE)
    y = 700
    for ln in wrap(d, body, F(REG, 56), W - 320):
        d.text((180, y), ln, font=F(REG, 56), fill=INK2)
        y += 96
    footer(d)
    return img


def end():
    img, d = canvas()
    d.text((90, 300), "四条挑片标准", font=F(BOLD, 82), fill=INK)
    items = ["标题越猛，越要慢", "看他动没动手", "评论区比正片有用", "数字先问分母"]
    y = 520
    for i, it in enumerate(items, 1):
        d.ellipse([90, y + 8, 146, y + 64], fill=BLUE)
        d.text((104, y + 14), str(i), font=F(BOLD, 34), fill=WHITE)
        d.text((180, y), it, font=F(BOLD, 60), fill=INK)
        y += 130
    d.text((90, 1200), "完整版在这儿：", font=F(REG, 46), fill=INK2)
    d.text((90, 1280), "github.com/iintel695-lab/whale-notes", font=F(BOLD, 46), fill=BLUE)
    try:
        m = Image.open("/home/ubuntu/whale-notes/assets/meme-skip.png").convert("RGBA")
        m = m.crop((8, 8, m.width - 8, m.height - 8))
        m.thumbnail((400, 400))
        img.paste(m, (W - m.width - 70, 1380), m)
    except Exception:
        pass
    footer(d)
    return img


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path("/home/ubuntu/whale-notes/douyin/cards")
    out.mkdir(parents=True, exist_ok=True)
    imgs = [
        cover(),
        card(1, 4, "标题越猛，越要慢",
             "「震惊」「彻底改变」「99% 的人都不知道」——\n这些话是让你点进去，不是让你学会什么。\n真正有货的人，标题通常很平。"),
        card(2, 4, "看他动没动手",
             "「AI 能帮你写代码」是复述。\n「第三句必须写不要解释，不然它先讲一遍原理」是经验。\n复述谁都会，经验骗不了人。"),
        card(3, 4, "评论区比正片有用",
             "作者没讲清楚的，底下第一条评论就补上了。\n正片看一半，评论看前二十条。\n全是「来了」「打卡」的，基本是流量货。"),
        card(4, 4, "数字先问分母",
             "月入十万——投了多少换来的？\n效率提升 300%——跟谁比？\n答不上来的，当广告看。"),
        end(),
    ]
    for i, im in enumerate(imgs, 1):
        p = out / f"{i:02d}.png"
        im.save(p, quality=95)
        print(p)
