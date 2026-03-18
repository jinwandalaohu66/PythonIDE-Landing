# 节奏达人 — Rhythm Master
# A rhythm game for the Pythonista Scene module on iOS

import scene
import math

PERFECT_W = 0.045
GREAT_W = 0.095
GOOD_W = 0.15
NOTE_H = 30
HIT_OFFSET = 130

COLORS = [
    (1.0, 0.18, 0.47),
    (0.18, 0.58, 1.0),
    (0.12, 0.95, 0.50),
    (1.0, 0.78, 0.12),
]

SONGS = [
    {'name': '初心练习', 'sub': 'First Steps', 'bpm': 100, 'speed': 300, 'diff': 1},
    {'name': '霓虹节拍', 'sub': 'Neon Beat',   'bpm': 128, 'speed': 400, 'diff': 2},
    {'name': '极速狂飙', 'sub': 'Turbo Rush',  'bpm': 155, 'speed': 500, 'diff': 3},
]

MENU, PLAY, RESULT = 0, 1, 2


def make_notes(idx):
    beat = 60.0 / SONGS[idx]['bpm']
    notes = []
    t = beat * 4

    def add(tm, lane):
        notes.append({'time': tm, 'lane': lane, 'hit': False, 'miss': False})

    if idx == 0:
        measures = [
            [0, 2, 1, 3],
            [1, 3, 0, 2],
            [0, 1, 2, 3],
            [3, 2, 1, 0],
            [(0, 2), -1, (1, 3), -1],
            [0, 1, 2, 3],
            [2, 0, 3, 1],
            [(0, 3), -1, (1, 2), -1],
        ]
        for _ in range(3):
            for m in measures:
                for v in m:
                    if isinstance(v, tuple):
                        for ln in v:
                            add(t, ln)
                    elif v >= 0:
                        add(t, v)
                    t += beat

    elif idx == 1:
        hb = beat / 2
        measures = [
            [0, -1, 2, -1, 1, -1, 3, -1],
            [1,  3, -1, 0, 2, -1, 1,  3],
            [0,  1,  2, 3, -1, 3, 2,  1],
            [-1, 0, -1, 2, -1, 1, -1, 3],
            [0,  2,  1, 3,  0, 2,  1, 3],
            [3, -1,  1, -1, 2, -1, 0, -1],
            [0,  1,  0,  1, 2,  3, 2, 3],
            [3,  1,  2,  0, -1, -1, 0, 3],
        ]
        for _ in range(4):
            for m in measures:
                for v in m:
                    if v >= 0:
                        add(t, v)
                    t += hb

    else:
        hb = beat / 2
        measures = [
            [(0,), (2,), (1, 3), (), (0, 2), (), (3,), (1,)],
            [(0, 1), (), (2, 3), (), (1,), (3,), (0,), (2,)],
            [(3,), (2,), (1,), (0,), (0, 3), (), (1, 2), ()],
            [(0,), (1,), (2,), (3,), (3,), (2,), (1,), (0,)],
            [(0, 2), (1, 3), (), (0,), (2,), (1, 3), (0, 2), ()],
            [(1,), (0,), (3,), (2,), (0, 1, 2, 3), (), (), ()],
            [(0,), (1,), (0,), (1,), (2,), (3,), (2,), (3,)],
            [(0, 3), (1, 2), (0, 3), (1, 2), (), (0, 1, 2, 3), (), ()],
        ]
        for _ in range(4):
            for m in measures:
                for lanes in m:
                    for ln in lanes:
                        add(t, ln)
                    t += hb

    return notes


class RhythmMaster(scene.Scene):

    def setup(self):
        self.state = MENU
        self._init_vars()

    def _init_vars(self):
        self.notes = []
        self.score = 0
        self.combo = 0
        self.best_combo = 0
        self.health = 1.0
        self.jc = [0, 0, 0, 0]
        self.effects = []
        self.flash = [0.0] * 4
        self.t0 = 0.0
        self.end_t = 0.0
        self.song_idx = 0
        self._scan = 0

    def _lane_x(self, lane):
        sl = self.safe_area_insets.left
        lw = (self.size.w - sl - self.safe_area_insets.right) / 4
        return sl + lw * lane, lw

    def _hit_y(self):
        return self.safe_area_insets.bottom + HIT_OFFSET

    # ═══════════════════════════════════════════════════════
    #  MENU
    # ═══════════════════════════════════════════════════════

    def _draw_menu(self):
        W, H = self.size.w, self.size.h
        scene.background(0.04, 0.04, 0.09)
        scene.no_stroke()

        for i in range(16):
            phase = (self.t * 0.22 + i * 0.83) % 1.0
            dx = math.sin(i * 2.1) * 0.35 + 0.5
            r, g, b = COLORS[i % 4]
            scene.fill(r, g, b, 0.06)
            scene.ellipse(W * dx - 5, H * phase - 5, 10, 10)

        pulse = 0.7 + 0.3 * math.sin(self.t * 2)
        scene.tint(1.0, 0.3, 0.6, pulse)
        scene.text('节奏达人', 'Helvetica-Bold', 46,
                   W / 2, H * 0.84, 5)
        scene.tint(0.55, 0.55, 0.72, 0.65)
        scene.text('Rhythm Master', 'Helvetica', 18, W / 2, H * 0.79, 5)
        scene.no_tint()

        card_w = min(W * 0.85, 360)
        card_h = 80
        base_y = H * 0.55

        for i, s in enumerate(SONGS):
            cy = base_y - i * (card_h + 14)
            x0 = (W - card_w) / 2
            r, g, b = COLORS[i]

            scene.fill(r, g, b, 0.10)
            scene.rect(x0, cy - card_h / 2, card_w, card_h)
            scene.no_fill()
            scene.stroke(r, g, b, 0.40)
            scene.stroke_weight(1.5)
            scene.rect(x0, cy - card_h / 2, card_w, card_h)
            scene.no_stroke()

            scene.tint(r, g, b, 1.0)
            scene.text(s['name'], 'Helvetica-Bold', 24, W / 2, cy + 12, 5)
            scene.tint(0.62, 0.62, 0.76, 0.78)
            scene.text('{0}  BPM {1}'.format(s['sub'], s['bpm']),
                       'Helvetica', 13, W / 2, cy - 8, 5)
            scene.tint(1.0, 0.85, 0.15, 0.9)
            scene.text('\u2605' * s['diff'] + '\u2606' * (3 - s['diff']),
                       'Helvetica', 15, W / 2, cy - 25, 5)
            scene.no_tint()

        fade = 0.4 + 0.25 * math.sin(self.t * 3)
        scene.tint(0.5, 0.5, 0.6, fade)
        scene.text('点击歌曲开始游戏',
                   'Helvetica', 14, W / 2, H * 0.11, 5)
        scene.no_tint()

    def _touch_menu(self, touch):
        H = self.size.h
        card_h = 80
        base_y = H * 0.55
        ty = touch.location.y
        for i in range(len(SONGS)):
            cy = base_y - i * (card_h + 14)
            if abs(ty - cy) < card_h / 2:
                self._begin_song(i)
                return

    # ═══════════════════════════════════════════════════════
    #  START SONG
    # ═══════════════════════════════════════════════════════

    def _begin_song(self, idx):
        self._init_vars()
        self.state = PLAY
        self.song_idx = idx
        self.notes = make_notes(idx)
        self.t0 = self.t
        self.end_t = (self.notes[-1]['time'] + 3.0) if self.notes else 5.0

    # ═══════════════════════════════════════════════════════
    #  PLAY — UPDATE
    # ═══════════════════════════════════════════════════════

    def _update_play(self):
        elapsed = self.t - self.t0

        for n in self.notes[self._scan:]:
            if n['hit'] or n['miss']:
                continue
            dt = n['time'] - elapsed
            if dt < -GOOD_W:
                n['miss'] = True
                self.combo = 0
                self.health = max(0.0, self.health - 0.025)
                self.jc[3] += 1
                x, lw = self._lane_x(n['lane'])
                self.effects.append(
                    (x + lw / 2, self._hit_y(), (0.5, 0.5, 0.5), 'Miss', self.t))
            elif dt > 1.0:
                break

        while self._scan < len(self.notes):
            n = self.notes[self._scan]
            if n['hit'] or n['miss']:
                self._scan += 1
            else:
                break

        for i in range(4):
            self.flash[i] = max(0.0, self.flash[i] - self.dt * 5)

        self.effects = [e for e in self.effects if self.t - e[4] < 0.8]

        if elapsed > self.end_t or self.health <= 0:
            self.state = RESULT

    # ═══════════════════════════════════════════════════════
    #  PLAY — DRAW
    # ═══════════════════════════════════════════════════════

    def _draw_play(self):
        W, H = self.size.w, self.size.h
        elapsed = self.t - self.t0
        speed = SONGS[self.song_idx]['speed']
        hy = self._hit_y()
        sl = self.safe_area_insets.left
        sr = self.safe_area_insets.right
        sb = self.safe_area_insets.bottom
        st = self.safe_area_insets.top

        scene.background(0.04, 0.04, 0.09)
        scene.no_stroke()

        # Lane dividers
        scene.stroke(0.16, 0.16, 0.26, 0.30)
        scene.stroke_weight(1)
        for i in range(5):
            if i < 4:
                x = self._lane_x(i)[0]
            else:
                lx, lw = self._lane_x(3)
                x = lx + lw
            scene.line(x, sb, x, H - st)
        scene.no_stroke()

        # Lane flash overlays
        for i in range(4):
            if self.flash[i] > 0.01:
                x, lw = self._lane_x(i)
                r, g, b = COLORS[i]
                scene.fill(r, g, b, self.flash[i] * 0.22)
                scene.rect(x, sb, lw, H - sb - st)

        # Beat pulse
        beat_dur = 60.0 / SONGS[self.song_idx]['bpm']
        bp = (elapsed % beat_dur) / beat_dur
        ba = max(0.0, 1.0 - bp * 4) * 0.4

        # Hit-zone lane indicators
        for i in range(4):
            x, lw = self._lane_x(i)
            r, g, b = COLORS[i]
            scene.fill(r, g, b, 0.10 + ba * 0.12)
            scene.rect(x + 2, hy - 18, lw - 4, 36)

        scene.stroke(1.0, 1.0, 1.0, 0.40 + ba * 0.25)
        scene.stroke_weight(2)
        scene.line(sl, hy, W - sr, hy)
        scene.no_stroke()

        # Falling notes
        for n in self.notes[self._scan:]:
            if n['hit'] or n['miss']:
                continue
            dt = n['time'] - elapsed
            ny = hy + dt * speed
            if ny > H + NOTE_H:
                break
            if ny < -NOTE_H:
                continue
            lane = n['lane']
            x, lw = self._lane_x(lane)
            r, g, b = COLORS[lane]

            scene.fill(r, g, b, 0.10)
            scene.rect(x - 2, ny - NOTE_H / 2 - 2, lw + 4, NOTE_H + 4)
            scene.fill(r, g, b, 0.82)
            scene.rect(x + 3, ny - NOTE_H / 2, lw - 6, NOTE_H)
            scene.fill(min(1, r + 0.35), min(1, g + 0.35),
                       min(1, b + 0.35), 0.40)
            scene.rect(x + 3, ny + NOTE_H / 2 - 4, lw - 6, 4)

        # Hit / judgment effects
        for (ex, ey, ec, etxt, et0) in self.effects:
            age = self.t - et0
            alpha = max(0.0, 1.0 - age / 0.8)
            ring = 36 * (1 + age * 2.5)
            r, g, b = ec

            scene.no_fill()
            scene.stroke(r, g, b, alpha * 0.50)
            scene.stroke_weight(2)
            scene.ellipse(ex - ring / 2, ey - ring / 2, ring, ring)
            if etxt == 'Perfect':
                ring2 = ring * 0.6
                scene.stroke(r, g, b, alpha * 0.30)
                scene.ellipse(ex - ring2 / 2, ey - ring2 / 2, ring2, ring2)
            scene.no_stroke()

            scene.tint(r, g, b, alpha)
            scene.text(etxt, 'Helvetica-Bold', 18,
                       ex, ey + 26 + age * 50, 5)
            scene.no_tint()

        # ── HUD ──

        top_y = H - st

        scene.tint(1, 1, 1, 0.90)
        scene.text(str(self.score), 'Helvetica-Bold', 26,
                   W / 2, top_y - 28, 5)
        scene.no_tint()

        if self.combo >= 2:
            cp = 0.8 + 0.2 * math.sin(self.t * 8)
            size = min(24, 20 + self.combo // 25)
            scene.tint(1, 0.9, 0.25, cp)
            scene.text('{0} COMBO'.format(self.combo),
                       'Helvetica-Bold', size, W / 2, top_y - 56, 5)
            scene.no_tint()

        # Health bar
        bar_w = min(W * 0.30, 140)
        bar_h = 7
        bar_x = W - sr - bar_w - 14
        bar_y = top_y - 32
        scene.fill(0.2, 0.2, 0.28, 0.40)
        scene.rect(bar_x, bar_y, bar_w, bar_h)
        hp = max(0, self.health)
        scene.fill(0.15 + 0.85 * (1 - hp), 0.82 * hp, 0.15, 0.85)
        scene.rect(bar_x, bar_y, bar_w * hp, bar_h)
        scene.tint(0.60, 0.60, 0.72, 0.65)
        scene.text('HP', 'Helvetica-Bold', 10,
                   bar_x - 14, bar_y + bar_h / 2, 5)
        scene.no_tint()

        # Song name
        scene.tint(0.48, 0.48, 0.62, 0.50)
        scene.text(SONGS[self.song_idx]['name'], 'Helvetica', 12,
                   sl + 14, top_y - 28, 4)
        scene.no_tint()

        # Progress bar
        if self.end_t > 0:
            prog = min(1.0, elapsed / self.end_t)
            py = sb + 3
            scene.fill(0.22, 0.22, 0.32, 0.28)
            scene.rect(sl, py, W - sl - sr, 3)
            scene.fill(0.65, 0.65, 0.80, 0.45)
            scene.rect(sl, py, (W - sl - sr) * prog, 3)

        # Countdown during lead-in
        lead_in = beat_dur * 4
        if elapsed < lead_in:
            count = int((lead_in - elapsed) / beat_dur) + 1
            if 1 <= count <= 4:
                frac = ((lead_in - elapsed) % beat_dur) / beat_dur
                ca = 0.35 + 0.45 * frac
                scene.tint(1, 1, 1, ca)
                scene.text(str(count), 'Helvetica-Bold', 56,
                           W / 2, H / 2, 5)
                scene.no_tint()

    # ═══════════════════════════════════════════════════════
    #  PLAY — TOUCH
    # ═══════════════════════════════════════════════════════

    def _touch_play(self, touch):
        tx = touch.location.x

        lane = -1
        for i in range(4):
            x, lw = self._lane_x(i)
            if x <= tx <= x + lw:
                lane = i
                break
        if lane < 0:
            return

        self.flash[lane] = 1.0
        elapsed = self.t - self.t0

        best = None
        best_dist = 999.0
        for n in self.notes[self._scan:]:
            if n['lane'] != lane or n['hit'] or n['miss']:
                continue
            d = abs(n['time'] - elapsed)
            if d < best_dist and d <= GOOD_W:
                best = n
                best_dist = d
            if n['time'] - elapsed > GOOD_W + 0.5:
                break

        if best is None:
            return

        best['hit'] = True

        if best_dist <= PERFECT_W:
            ji, pts, col, label = 0, 300, (1.0, 0.92, 0.20), 'Perfect'
        elif best_dist <= GREAT_W:
            ji, pts, col, label = 1, 200, (0.30, 0.92, 1.0), 'Great'
        else:
            ji, pts, col, label = 2, 100, (0.30, 1.0, 0.50), 'Good'

        self.combo += 1
        self.best_combo = max(self.best_combo, self.combo)
        self.score += pts * (1 + self.combo // 10)
        self.jc[ji] += 1

        if ji == 0:
            self.health = min(1.0, self.health + 0.005)

        x, lw = self._lane_x(lane)
        self.effects.append((x + lw / 2, self._hit_y(), col, label, self.t))

    # ═══════════════════════════════════════════════════════
    #  RESULT
    # ═══════════════════════════════════════════════════════

    def _draw_result(self):
        W, H = self.size.w, self.size.h
        scene.background(0.04, 0.04, 0.09)
        scene.no_stroke()

        scene.tint(1.0, 0.3, 0.6, 1.0)
        if self.health <= 0:
            scene.text('挑战失败', 'Helvetica-Bold', 34,
                       W / 2, H * 0.82, 5)
        else:
            scene.text('演奏结束', 'Helvetica-Bold', 34,
                       W / 2, H * 0.82, 5)
        scene.no_tint()

        total = max(sum(self.jc), 1)
        ratio = (self.jc[0] + self.jc[1] * 0.7) / total
        thresholds = [
            (0.95, 'S', (1.0, 0.85, 0.10)),
            (0.85, 'A', (0.20, 1.0, 0.40)),
            (0.70, 'B', (0.20, 0.70, 1.0)),
            (0.50, 'C', (0.80, 0.50, 1.0)),
        ]
        rank, rank_color = 'D', (0.55, 0.55, 0.55)
        for thr, rk, c in thresholds:
            if ratio >= thr:
                rank, rank_color = rk, c
                break

        if rank == 'S':
            for i in range(8):
                ang = self.t * 2 + i * 0.785
                dx = math.cos(ang) * 55
                dy = math.sin(ang) * 55
                a = 0.3 + 0.2 * math.sin(self.t * 4 + i)
                scene.fill(1.0, 0.85, 0.1, a)
                scene.ellipse(W / 2 + dx - 4, H * 0.70 + dy - 4, 8, 8)

        scene.tint(*rank_color, 1.0)
        scene.text(rank, 'Helvetica-Bold', 68, W / 2, H * 0.70, 5)
        scene.no_tint()

        scene.tint(1.0, 1.0, 1.0, 0.90)
        scene.text(str(self.score), 'Helvetica-Bold', 30,
                   W / 2, H * 0.57, 5)
        scene.tint(0.70, 0.70, 0.82, 0.78)
        scene.text('最大连击  {0}'.format(self.best_combo),
                   'Helvetica', 17, W / 2, H * 0.52, 5)
        scene.no_tint()

        breakdown = [
            ('Perfect', (1.0, 0.90, 0.20), self.jc[0]),
            ('Great',   (0.30, 0.90, 1.0), self.jc[1]),
            ('Good',    (0.30, 1.0,  0.50), self.jc[2]),
            ('Miss',    (0.55, 0.30, 0.30), self.jc[3]),
        ]
        y = H * 0.44
        for label, color, count in breakdown:
            scene.tint(*color, 0.85)
            scene.text('{0}  {1}'.format(label, count),
                       'Helvetica', 16, W / 2, y, 5)
            scene.no_tint()
            y -= 26

        fade = 0.40 + 0.25 * math.sin(self.t * 3)
        scene.tint(0.50, 0.50, 0.60, fade)
        scene.text('点击返回', 'Helvetica', 15,
                   W / 2, H * 0.10, 5)
        scene.no_tint()

    def _touch_result(self, touch):
        self.state = MENU

    # ═══════════════════════════════════════════════════════
    #  DISPATCH
    # ═══════════════════════════════════════════════════════

    def update(self):
        if self.state == PLAY:
            self._update_play()

    def draw(self):
        if self.state == MENU:
            self._draw_menu()
        elif self.state == PLAY:
            self._draw_play()
        else:
            self._draw_result()

    def touch_began(self, touch):
        if self.state == MENU:
            self._touch_menu(touch)
        elif self.state == PLAY:
            self._touch_play(touch)
        else:
            self._touch_result(touch)

    def touch_moved(self, touch):
        pass

    def touch_ended(self, touch):
        pass


scene.run(RhythmMaster())
