# 欢迎使用 PythonIDE！如果觉得好用，请给个好评哦～
# -*- coding: utf-8 -*-
"""汇率转换器 — major currencies with flags and trend arrows."""

from widget import Widget, family, SMALL, MEDIUM, LARGE
import time

currencies = [
    ("🇺🇸", "USD", 1.0000,  "up"),
    ("🇪🇺", "EUR", 0.9182,  "down"),
    ("🇯🇵", "JPY", 149.85,  "up"),
    ("🇬🇧", "GBP", 0.7923,  "down"),
    ("🇨🇳", "CNY", 7.2450,  "up"),
]

now = time.strftime("%H:%M")

bg       = ("#F8FAFC", "#0F172A")
card_bg  = ("#F1F5F9", "#1E293B")
txt_main = ("#0F172A", "#F8FAFC")
txt_sub  = ("#64748B", "#94A3B8")
up_clr   = ("#10B981", "#34D399")
down_clr = ("#EF4444", "#F87171")
accent   = "#3B82F6"

w = Widget(background=bg, padding=14)

if family == SMALL:
    with w.vstack(spacing=0, align="center"):
        w.spacer()
        w.icon("dollarsign.circle.fill", size=18, color=accent)
        w.spacer(6)
        w.text("1 USD", size=22, weight="bold", design="rounded", color=txt_main)
        w.spacer(4)
        with w.hstack(spacing=4):
            w.text("🇺🇸", size=14)
            w.text("USD", size=12, weight="semibold", color=txt_main)
            w.spacer()
            w.text("基准", size=10, color=txt_sub)
        w.spacer()
        with w.hstack(spacing=6):
            clr = up_clr
            arrow = "arrow.up.right"
            w.icon(arrow, size=8, color=clr)
            w.text("EUR 0.92", size=11, weight="medium", color=clr)
            w.spacer()
            clr = down_clr
            arrow = "arrow.down.right"
            w.icon(arrow, size=8, color=clr)
            w.text("JPY 149.9", size=11, weight="medium", color=clr)
        w.spacer()

elif family == MEDIUM:
    with w.vstack(spacing=0):
        with w.hstack(spacing=6):
            w.icon("dollarsign.circle.fill", size=14, color=accent)
            w.text("汇率", size=14, weight="semibold", color=txt_main)
            w.spacer()
            w.text(f"更新 {now}", size=11, color=txt_sub)
        w.spacer()
        with w.hstack(spacing=0):
            for flag, code, rate, trend in currencies[:4]:
                with w.vstack(spacing=2, align="center"):
                    clr = up_clr if trend == "up" else down_clr
                    arrow = "arrow.up.right" if trend == "up" else "arrow.down.right"
                    w.text(flag, size=16)
                    w.text(code, size=11, weight="semibold", color=txt_main)
                    with w.hstack(spacing=2):
                        w.icon(arrow, size=8, color=clr)
                        w.text(f"{rate:.2f}" if rate < 10 else f"{rate:.1f}", size=12, weight="medium", color=clr)
                w.spacer()
        w.spacer()

else:
    with w.vstack(spacing=6):
        with w.hstack(spacing=6, align="center"):
            w.icon("dollarsign.circle.fill", size=18, color=accent)
            w.text("汇率转换器", size=17, weight="bold", color=txt_main)
            w.spacer()
            w.icon("clock", size=12, color=txt_sub)
            w.text(f"更新于 {now}", size=12, color=txt_sub)
        w.divider(color=("#E2E8F0", "#334155"))
        for flag, code, rate, trend in currencies:
            with w.hstack(spacing=6, align="center"):
                w.text(flag, size=16)
                w.text(code, size=14, weight="bold", color=txt_main)
                w.spacer()
                clr = up_clr if trend == "up" else down_clr
                arrow = "arrow.up.right" if trend == "up" else "arrow.down.right"
                w.icon(arrow, size=11, color=clr)
                w.text(f"{rate:.4f}" if rate < 10 else f"{rate:.2f}",
                       size=15, weight="semibold", color=clr)
            if code != "CNY":
                w.divider(color=("#F1F5F9", "#1E293B"))

w.render()