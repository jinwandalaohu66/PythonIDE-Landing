from scene import *
import json
import os
import random
import sound
import ui


GRID_SIZE = 8
TARGET_SCORE = 150
SAVE_FILE = 'block_blast_save.json'
NEON_BG = '#090c18'
NEON_PANEL = '#121a31'
NEON_PANEL_2 = '#182445'
NEON_GRID = '#22345f'
NEON_GRID_GLOW = '#2f4f8f'
NEON_TEXT = '#e8f7ff'
NEON_SUBTEXT = '#7fd6ff'
NEON_PINK = '#ff4fd8'
NEON_CYAN = '#38f6ff'
NEON_GREEN = '#59ffa8'
NEON_RED = '#ff6b8a'
NEON_YELLOW = '#ffe66d'


SHAPES = [
    {'name': 'single', 'cells': [(0, 0)], 'color': '#ffe66d'},
    {'name': 'domino_h', 'cells': [(0, 0), (1, 0)], 'color': '#59ffa8'},
    {'name': 'domino_v', 'cells': [(0, 0), (0, 1)], 'color': '#38f6ff'},
    {'name': 'triple_h', 'cells': [(0, 0), (1, 0), (2, 0)], 'color': '#58a6ff'},
    {'name': 'triple_v', 'cells': [(0, 0), (0, 1), (0, 2)], 'color': '#c77dff'},
    {'name': 'square_2', 'cells': [(0, 0), (1, 0), (0, 1), (1, 1)], 'color': '#ff9f68'},
    {'name': 'l_3', 'cells': [(0, 0), (0, 1), (1, 0)], 'color': '#ff6b8a'},
    {'name': 'l_3_b', 'cells': [(0, 0), (1, 0), (1, 1)], 'color': '#ff4fd8'},
    {'name': 'line_4_h', 'cells': [(0, 0), (1, 0), (2, 0), (3, 0)], 'color': '#00f5d4'},
    {'name': 'line_4_v', 'cells': [(0, 0), (0, 1), (0, 2), (0, 3)], 'color': '#4cc9f0'},
    {'name': 'l_4', 'cells': [(0, 0), (0, 1), (0, 2), (1, 0)], 'color': '#f72585'},
    {'name': 'l_4_b', 'cells': [(0, 0), (1, 0), (2, 0), (0, 1)], 'color': '#ffb703'},
    {'name': 't_4', 'cells': [(0, 0), (1, 0), (2, 0), (1, 1)], 'color': '#b8f2e6'},
    {'name': 'line_5_h', 'cells': [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], 'color': '#72efdd'},
    {'name': 'line_5_v', 'cells': [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4)], 'color': '#80ffdb'},
]


class BlockBlastGame(Scene):
    def setup(self):
        self.background_color = NEON_BG
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.board_cells = []
        self.board_blocks = {}
        self.slot_nodes = []
        self.slot_glows = []
        self.pieces = []
        self.selected_piece = None
        self.drag_nodes = []
        self.preview_nodes = []
        self.preview_anchor = None
        self.score = 0
        self.best_score = self._load_best_score()
        self.combo = 0
        self.multiplier = 1
        self.game_over = False
        self.victory = False
        self.endless_mode = False
        self.show_menu = True
        self.board_left = 0
        self.board_bottom = 0
        self.cell_size = 0
        self.board_size = 0
        self.board_top = 0
        self.board_right = 0
        self.message_label = None
        self.restart_label = None
        self.score_label = None
        self.best_label = None
        self.combo_label = None
        self.goal_label = None
        self.endless_label = None
        self.last_preview_valid = False
        self.menu_nodes = []
        self.menu_buttons = {}
        self.skin_buttons = {}
        self.selected_skin = 'neon'
        self.shake_offset = (0, 0)
        self._build_ui()
        self._show_start_menu()
        self._update_status()

    def _build_ui(self):
        w, h = self.size.w, self.size.h
        insets = self.safe_area_insets

        self.world = Node(parent=self)

        self.bg = SpriteNode(color=NEON_BG, size=(w, h), position=(w / 2, h / 2), parent=self.world)
        self.bg.z_position = -50

        self.bg_glow_top = SpriteNode(
            color='#121f3f',
            size=(w * 0.9, h * 0.22),
            position=(w / 2, h - insets.top - 30),
            parent=self.world,
        )
        self.bg_glow_top.alpha = 0.28
        self.bg_glow_top.z_position = -40

        self.bg_glow_bottom = SpriteNode(
            color='#1a0f2f',
            size=(w * 0.85, h * 0.22),
            position=(w / 2, h * 0.08),
            parent=self.world,
        )
        self.bg_glow_bottom.alpha = 0.22
        self.bg_glow_bottom.z_position = -40

        self.cell_size = min(w * 0.093, h * 0.058)
        self.board_size = self.cell_size * GRID_SIZE
        self.board_left = (w - self.board_size) / 2
        self.board_bottom = h * 0.32
        self.board_right = self.board_left + self.board_size
        self.board_top = self.board_bottom + self.board_size

        board_back_size = self.board_size + self.cell_size * 0.6
        self.board_back_glow = SpriteNode(
            color=NEON_CYAN,
            size=(board_back_size + self.cell_size * 0.15, board_back_size + self.cell_size * 0.15),
            position=(w / 2, self.board_bottom + self.board_size / 2),
            parent=self.world,
        )
        self.board_back_glow.alpha = 0.11
        self.board_back_glow.z_position = -5

        self.board_back = SpriteNode(
            color=NEON_PANEL,
            size=(board_back_size, board_back_size),
            position=(w / 2, self.board_bottom + self.board_size / 2),
            parent=self.world,
        )
        self.board_back.z_position = -4

        self.title_label = LabelNode(
            'BLOCK BLAST',
            font=('Avenir Next Heavy', 26),
            position=(w / 2, h - insets.top - 34),
            color=NEON_CYAN,
            parent=self.world,
        )

        self.score_label = LabelNode(
            'SCORE 0',
            font=('Menlo-Bold', 20),
            position=(w * 0.28, h - insets.top - 72),
            color=NEON_TEXT,
            parent=self.world,
        )

        self.best_label = LabelNode(
            'BEST 0',
            font=('Menlo-Bold', 16),
            position=(w * 0.73, h - insets.top - 70),
            color=NEON_YELLOW,
            parent=self.world,
        )

        self.goal_label = LabelNode(
            'Mục tiêu %d' % TARGET_SCORE,
            font=('Menlo', 14),
            position=(w / 2, h - insets.top - 98),
            color=NEON_SUBTEXT,
            parent=self.world,
        )

        self.combo_label = LabelNode(
            'COMBO x1',
            font=('Menlo-Bold', 14),
            position=(w / 2, self.board_top + self.cell_size * 0.45),
            color=NEON_PINK,
            parent=self.world,
        )
        self.combo_label.alpha = 0.85

        self.endless_label = LabelNode(
            'CLASSIC',
            font=('Menlo-Bold', 13),
            position=(w / 2, self.board_top + self.cell_size * 0.78),
            color=NEON_SUBTEXT,
            parent=self.world,
        )
        self.endless_label.alpha = 0.82

        for row in range(GRID_SIZE):
            row_cells = []
            for col in range(GRID_SIZE):
                x = self.board_left + col * self.cell_size + self.cell_size / 2
                y = self.board_top - row * self.cell_size - self.cell_size / 2

                glow = SpriteNode(
                    color=NEON_GRID_GLOW,
                    size=(self.cell_size * 0.96, self.cell_size * 0.96),
                    position=(x, y),
                    parent=self.world,
                )
                glow.alpha = 0.08
                glow.z_position = -3

                cell = SpriteNode(
                    color=NEON_GRID,
                    size=(self.cell_size * 0.88, self.cell_size * 0.88),
                    position=(x, y),
                    parent=self.world,
                )
                cell.z_position = -2
                row_cells.append(cell)
            self.board_cells.append(row_cells)

        slot_y = max(insets.bottom + h * 0.12, h * 0.14)
        spacing = w / 3
        slot_size = self.cell_size * 3.35
        for i in range(3):
            x = spacing * (i + 0.5)

            glow = SpriteNode(
                color=NEON_PINK if i == 1 else NEON_CYAN,
                size=(slot_size + self.cell_size * 0.18, slot_size + self.cell_size * 0.18),
                position=(x, slot_y),
                parent=self.world,
            )
            glow.alpha = 0.14
            glow.z_position = -3
            self.slot_glows.append(glow)

            slot = SpriteNode(
                color=NEON_PANEL_2,
                size=(slot_size, slot_size),
                position=(x, slot_y),
                parent=self.world,
            )
            slot.alpha = 0.97
            slot.z_position = -2
            self.slot_nodes.append(slot)

        self.message_label = LabelNode(
            '',
            font=('Avenir Next Heavy', 24),
            position=(w / 2, self.board_bottom - self.cell_size * 0.8),
            color=NEON_TEXT,
            parent=self.world,
        )
        self.message_label.alpha = 0

        self.restart_label = LabelNode(
            '',
            font=('Menlo', 14),
            position=(w / 2, self.board_bottom - self.cell_size * 1.4),
            color=NEON_SUBTEXT,
            parent=self.world,
        )
        self.restart_label.alpha = 0

    def _show_start_menu(self):
        self._clear_menu()
        w, h = self.size.w, self.size.h

        overlay = SpriteNode(
            color='#04060d',
            size=(w, h),
            position=(w / 2, h / 2),
            parent=self,
        )
        overlay.alpha = 0.68
        overlay.z_position = 200
        self.menu_nodes.append(overlay)

        panel = ShapeNode(
            ui.Path.rounded_rect(0, 0, w * 0.82, h * 0.5, 22),
            fill_color=NEON_PANEL,
            stroke_color=NEON_CYAN,
            line_width=2,
            parent=self,
        )
        panel.position = (w / 2, h * 0.55)
        panel.alpha = 0.96
        panel.z_position = 201
        self.menu_nodes.append(panel)

        title = LabelNode(
            'BLOCK BLAST',
            font=('Avenir Next Heavy', 28),
            position=(w / 2, h * 0.71),
            color=NEON_CYAN,
            parent=self,
        )
        title.z_position = 202
        self.menu_nodes.append(title)

        desc = LabelNode(
            'Chọn chế độ chơi và skin block',
            font=('Menlo', 13),
            position=(w / 2, h * 0.665),
            color=NEON_TEXT,
            parent=self,
        )
        desc.z_position = 202
        self.menu_nodes.append(desc)

        classic = self._create_menu_button((w / 2, h * 0.59), w * 0.58, 54, 'CLASSIC MODE', NEON_CYAN)
        endless = self._create_menu_button((w / 2, h * 0.505), w * 0.58, 54, 'ENDLESS MODE', NEON_PINK)
        self.menu_buttons['classic'] = classic
        self.menu_buttons['endless'] = endless

        skin_title = LabelNode(
            'SKIN',
            font=('Menlo-Bold', 14),
            position=(w / 2, h * 0.43),
            color=NEON_YELLOW,
            parent=self,
        )
        skin_title.z_position = 202
        self.menu_nodes.append(skin_title)

        skin_y = h * 0.365
        skin_w = w * 0.19
        self.skin_buttons['neon'] = self._create_menu_button((w * 0.28, skin_y), skin_w, 44, 'NEON', NEON_CYAN, small=True)
        self.skin_buttons['candy'] = self._create_menu_button((w * 0.5, skin_y), skin_w, 44, 'CANDY', NEON_PINK, small=True)
        self.skin_buttons['pixel'] = self._create_menu_button((w * 0.72, skin_y), skin_w, 44, 'PIXEL', NEON_GREEN, small=True)
        self._refresh_skin_buttons()

        tip = LabelNode(
            'Classic: đạt mục tiêu  |  Endless: chơi vô tận',
            font=('Menlo', 11),
            position=(w / 2, h * 0.29),
            color=NEON_SUBTEXT,
            parent=self,
        )
        tip.z_position = 202
        self.menu_nodes.append(tip)

    def _create_menu_button(self, position, width, height, text, color, small=False):
        root = Node(position=position, parent=self)
        root.z_position = 202

        glow = ShapeNode(
            ui.Path.rounded_rect(0, 0, width + 10, height + 10, 18),
            fill_color=color,
            stroke_color='clear',
            parent=root,
        )
        glow.position = (0, 0)
        glow.alpha = 0.16
        glow.z_position = 0

        back = ShapeNode(
            ui.Path.rounded_rect(0, 0, width, height, 16),
            fill_color=NEON_PANEL_2,
            stroke_color=color,
            line_width=2,
            parent=root,
        )
        back.position = (0, 0)
        back.z_position = 0.1

        label = LabelNode(
            text,
            font=('Avenir Next Heavy', 14 if small else 18),
            position=(0, 0),
            color=NEON_TEXT,
            parent=root,
        )
        label.z_position = 1

        self.menu_nodes.append(root)
        return {
            'root': root,
            'glow': glow,
            'back': back,
            'label': label,
            'size': (width, height),
            'color': color,
            'small': small,
        }

    def _refresh_skin_buttons(self):
        for name, button in self.skin_buttons.items():
            active = name == self.selected_skin
            button['glow'].alpha = 0.26 if active else 0.10
            button['back'].fill_color = '#24355f' if active else NEON_PANEL_2
            button['back'].stroke_color = button['color']
            button['back'].line_width = 3 if active else 2
            button['label'].color = button['color'] if active else NEON_TEXT

    def _clear_menu(self):
        for node in self.menu_nodes:
            node.remove_from_parent()
        self.menu_nodes = []
        self.menu_buttons = {}
        self.skin_buttons = {}

    def _load_best_score(self):
        if not os.path.exists(SAVE_FILE):
            return 0
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return int(data.get('best_score', 0))
        except Exception:
            return 0

    def _save_best_score(self):
        try:
            with open(SAVE_FILE, 'w', encoding='utf-8') as f:
                json.dump({'best_score': self.best_score}, f)
        except Exception:
            pass

    def _start_game(self, endless=False):
        self.endless_mode = endless
        self.show_menu = False
        self._clear_menu()
        self._reset_game_state()
        self._update_status()
        sound.play_effect('game:Powerup', volume=0.45)

    def _reset_game_state(self):
        for node in list(self.board_blocks.values()):
            if isinstance(node, dict):
                for sub in node.values():
                    if sub is not None:
                        sub.remove_from_parent()
            elif node is not None:
                node.remove_from_parent()
        self.board_blocks = {}
        self.grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.victory = False
        self.score = 0
        self.combo = 0
        self.multiplier = 1
        self.selected_piece = None
        self.preview_anchor = None
        self.last_preview_valid = False
        self._clear_drag_nodes()
        self.message_label.alpha = 0
        self.restart_label.alpha = 0
        self.message_label.text = ''
        self.restart_label.text = ''
        self._new_hand()

    def _random_piece(self):
        shape = random.choice(SHAPES)
        return {
            'cells': list(shape['cells']),
            'color': shape['color'],
            'used': False,
            'root': None,
            'slot_index': -1,
            'preview_cell': 0,
        }

    def _skin_style(self, color, preview=False):
        if self.selected_skin == 'candy':
            return {
                'shadow': '#7a3b52',
                'glow_color': color,
                'glow_alpha': 0.10 if preview else 0.14,
                'tile_color': color,
                'tile_alpha': 0.22 if preview else 1.0,
                'highlight_color': '#fff8ff',
                'highlight_alpha': 0.30 if not preview else 0.14,
                'accent_color': '#ffffff',
                'accent_alpha': 0.16 if not preview else 0.08,
                'square': False,
            }
        if self.selected_skin == 'pixel':
            return {
                'shadow': '#111111',
                'glow_color': color,
                'glow_alpha': 0.04 if preview else 0.07,
                'tile_color': color,
                'tile_alpha': 0.20 if preview else 1.0,
                'highlight_color': '#ffffff',
                'highlight_alpha': 0.10 if not preview else 0.05,
                'accent_color': '#222222',
                'accent_alpha': 0.22 if not preview else 0.10,
                'square': True,
            }
        return {
            'shadow': '#04060d',
            'glow_color': color,
            'glow_alpha': 0.18 if not preview else 0.18,
            'tile_color': color,
            'tile_alpha': 0.26 if preview else 1.0,
            'highlight_color': '#ffffff',
            'highlight_alpha': 0.22 if not preview else 0.12,
            'accent_color': '#d7f9ff',
            'accent_alpha': 0.08 if not preview else 0.04,
            'square': False,
        }

    def _refresh_all_piece_previews(self):
        active = list(self.pieces)
        self._clear_piece_nodes()
        for piece in active:
            if piece.get('used'):
                piece['root'] = None
                continue
            self._create_piece_preview(piece, piece['slot_index'])

    def _new_hand(self):
        self._clear_piece_nodes()
        self.pieces = []
        for i in range(3):
            piece = self._random_piece()
            piece['slot_index'] = i
            self._create_piece_preview(piece, i)
            self.pieces.append(piece)
        self._check_game_state()

    def _clear_piece_nodes(self):
        for piece in self.pieces:
            if piece.get('root') is not None:
                piece['root'].remove_from_parent()

    def _make_block_visual(self, parent, position, size, color, z_base, preview=False):
        style = self._skin_style(color, preview=preview)

        shadow = SpriteNode(
            color=style['shadow'],
            size=(size * 0.9, size * 0.9),
            position=(position[0] + size * 0.08, position[1] - size * 0.08),
            parent=parent,
        )
        shadow.alpha = 0.35 if not preview else 0.12
        shadow.z_position = z_base

        glow = SpriteNode(
            color=style['glow_color'],
            size=(size * 1.02, size * 1.02),
            position=position,
            parent=parent,
        )
        glow.alpha = style['glow_alpha']
        glow.z_position = z_base + 0.1

        tile_scale = 0.80 if style['square'] else 0.84
        tile = SpriteNode(
            color=style['tile_color'],
            size=(size * tile_scale, size * tile_scale),
            position=position,
            parent=parent,
        )
        tile.alpha = style['tile_alpha']
        tile.z_position = z_base + 0.2

        highlight_h = 0.11 if style['square'] else 0.15
        highlight = SpriteNode(
            color=style['highlight_color'],
            size=(size * 0.48, size * highlight_h),
            position=(position[0] - size * 0.12, position[1] + size * 0.18),
            parent=parent,
        )
        highlight.alpha = style['highlight_alpha']
        highlight.z_position = z_base + 0.3

        accent = SpriteNode(
            color=style['accent_color'],
            size=(size * 0.22, size * 0.22),
            position=(position[0] + size * 0.15, position[1] - size * 0.15),
            parent=parent,
        )
        accent.alpha = style['accent_alpha']
        accent.z_position = z_base + 0.25

        return {
            'shadow': shadow,
            'glow': glow,
            'tile': tile,
            'highlight': highlight,
            'accent': accent,
        }

    def _set_block_visual_position(self, visual, position, size):
        visual['shadow'].position = (position[0] + size * 0.08, position[1] - size * 0.08)
        visual['glow'].position = position
        visual['tile'].position = position
        visual['highlight'].position = (position[0] - size * 0.12, position[1] + size * 0.18)

    def _run_visual_action(self, visual, action):
        for key in visual:
            visual[key].run_action(action)

    def _remove_visual(self, visual):
        for key in visual:
            visual[key].remove_from_parent()

    def _create_piece_preview(self, piece, slot_index):
        slot = self.slot_nodes[slot_index]
        cells = piece['cells']
        max_x = max(c[0] for c in cells)
        max_y = max(c[1] for c in cells)
        width = max_x + 1
        height = max_y + 1
        preview_cell = min(self.cell_size * 0.58, (slot.size.w * 0.72) / max(width, height))
        root = Node(position=slot.position, parent=self.world)
        root.z_position = 5
        piece['preview_cell'] = preview_cell

        offset_x = -((width - 1) * preview_cell) / 2
        offset_y = -((height - 1) * preview_cell) / 2
        for dx, dy in cells:
            x = offset_x + dx * preview_cell
            y = offset_y + dy * preview_cell
            self._make_block_visual(root, (x, y), preview_cell, piece['color'], 0, preview=False)
        piece['root'] = root

    def _board_cell_position(self, row, col):
        x = self.board_left + col * self.cell_size + self.cell_size / 2
        y = self.board_top - row * self.cell_size - self.cell_size / 2
        return x, y

    def _board_coords_from_point(self, point):
        if not (self.board_left <= point.x <= self.board_right and self.board_bottom <= point.y <= self.board_top):
            return None
        col = int((point.x - self.board_left) / self.cell_size)
        row = int((self.board_top - point.y) / self.cell_size)
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            return row, col
        return None

    def _piece_bounds(self, piece):
        max_x = max(c[0] for c in piece['cells'])
        max_y = max(c[1] for c in piece['cells'])
        return max_x + 1, max_y + 1

    def _piece_center_offset(self, piece, cell_size):
        cells = piece['cells']
        min_x = min(c[0] for c in cells)
        max_x = max(c[0] for c in cells)
        min_y = min(c[1] for c in cells)
        max_y = max(c[1] for c in cells)
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        return center_x * cell_size, center_y * cell_size

    def _can_place(self, piece, row, col):
        for dx, dy in piece['cells']:
            r = row - dy
            c = col + dx
            if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                return False
            if self.grid[r][c] is not None:
                return False
        return True

    def _best_anchor_for_point(self, piece, point):
        best = None
        best_dist = None
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                can_place = self._can_place(piece, row, col)
                cells = []
                center_sum_x = 0
                center_sum_y = 0
                valid_for_display = True

                for dx, dy in piece['cells']:
                    r = row - dy
                    c = col + dx
                    if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE):
                        valid_for_display = False
                        break
                    x, y = self._board_cell_position(r, c)
                    cells.append((r, c, x, y))
                    center_sum_x += x
                    center_sum_y += y

                if not valid_for_display:
                    continue

                center_x = center_sum_x / len(cells)
                center_y = center_sum_y / len(cells)
                dist = (center_x - point.x) ** 2 + (center_y - point.y) ** 2

                if best is None or dist < best_dist or (dist == best_dist and can_place and not best['can_place']):
                    best = {
                        'row': row,
                        'col': col,
                        'can_place': can_place,
                        'cells': cells,
                        'center': (center_x, center_y),
                    }
                    best_dist = dist
        return best

    def _show_floating_text(self, text, color, position, dy=42, font_size=16):
        label = LabelNode(
            text,
            font=('Avenir Next Heavy', font_size),
            position=position,
            color=color,
            parent=self.world,
        )
        label.z_position = 60
        label.run_action(Action.sequence(
            Action.group(
                Action.move_by(0, dy, 0.65),
                Action.fade_to(0.0, 0.65),
                Action.scale_to(1.15, 0.18),
            ),
            Action.remove(),
        ))

    def _pulse_slot(self, piece):
        if piece is None or piece.get('slot_index', -1) < 0:
            return
        slot = self.slot_nodes[piece['slot_index']]
        glow = self.slot_glows[piece['slot_index']]
        slot.run_action(Action.sequence(
            Action.scale_to(1.07, 0.08),
            Action.scale_to(1.0, 0.1),
        ))
        glow.run_action(Action.sequence(
            Action.fade_to(0.24, 0.08),
            Action.fade_to(0.14, 0.12),
        ))

    def _explode_cells(self, cells, color):
        for r, c in cells:
            x, y = self._board_cell_position(r, c)
            for _ in range(6):
                spark = SpriteNode(
                    color=color,
                    size=(self.cell_size * 0.22, self.cell_size * 0.22),
                    position=(x, y),
                    parent=self.world,
                )
                spark.z_position = 30
                spark.alpha = 0.95
                dx = random.uniform(-self.cell_size * 1.1, self.cell_size * 1.1)
                dy = random.uniform(-self.cell_size * 1.1, self.cell_size * 1.1)
                scale = random.uniform(0.2, 1.2)
                spark.run_action(Action.sequence(
                    Action.group(
                        Action.move_by(dx, dy, 0.26),
                        Action.fade_to(0.0, 0.26),
                        Action.scale_to(scale, 0.26),
                    ),
                    Action.remove(),
                ))

            flash = SpriteNode(
                color='white',
                size=(self.cell_size * 1.05, self.cell_size * 1.05),
                position=(x, y),
                parent=self.world,
            )
            flash.alpha = 0.35
            flash.z_position = 29
            flash.run_action(Action.sequence(
                Action.group(
                    Action.scale_to(1.35, 0.12),
                    Action.fade_to(0.0, 0.14),
                ),
                Action.remove(),
            ))

    def _shake_board(self, strength=6, times=4):
        actions = []
        for i in range(times):
            dx = strength if i % 2 == 0 else -strength
            actions.append(Action.move_by(dx, 0, 0.03))
        actions.append(Action.move_to(0, 0, 0.03))
        self.world.run_action(Action.sequence(*actions))

    def _bump_block(self, visual):
        self._run_visual_action(visual, Action.sequence(
            Action.scale_to(1.08, 0.06),
            Action.scale_to(1.0, 0.08),
        ))

    def _place_piece(self, piece, row, col):
        if not self._can_place(piece, row, col):
            sound.play_effect('game:Error', volume=0.5)
            return False

        placed = []
        for dx, dy in piece['cells']:
            r = row - dy
            c = col + dx
            self.grid[r][c] = piece['color']
            x, y = self._board_cell_position(r, c)
            visual = self._make_block_visual(self.world, (x, y), self.cell_size, piece['color'], 1.5, preview=False)
            self.board_blocks[(r, c)] = visual
            self._bump_block(visual)
            placed.append((r, c))

        piece['used'] = True
        if piece.get('root') is not None:
            piece['root'].alpha = 0.15

        base_gain = len(placed)
        self.score += base_gain
        sound.play_effect('ui:click1', volume=0.45)

        cleared_lines, cleared_cells = self._clear_lines(piece['color'])
        if cleared_lines:
            self.combo += 1
            self.multiplier = min(8, 1 + self.combo)
            combo_bonus = cleared_cells * self.multiplier + cleared_lines * 8
            self.score += combo_bonus
            self._show_floating_text(
                'COMBO x%d  +%d' % (self.multiplier, combo_bonus),
                NEON_PINK,
                (self.size.w / 2, self.board_top + self.cell_size * 0.28),
                dy=26,
                font_size=15,
            )
            sound.play_effect('arcade:Coin_1', volume=0.65)
        else:
            self.combo = 0
            self.multiplier = 1

        if self.score > self.best_score:
            self.best_score = self.score
            self._save_best_score()

        self._update_status()

        if all(p['used'] for p in self.pieces):
            self._new_hand()
        else:
            self._check_game_state()

        if not self.endless_mode and self.score >= TARGET_SCORE and not self.victory:
            self._win_game()
        return True

    def _clear_lines(self, effect_color):
        full_rows = []
        full_cols = []

        for row in range(GRID_SIZE):
            if all(self.grid[row][col] is not None for col in range(GRID_SIZE)):
                full_rows.append(row)

        for col in range(GRID_SIZE):
            if all(self.grid[row][col] is not None for row in range(GRID_SIZE)):
                full_cols.append(col)

        if not full_rows and not full_cols:
            return 0, 0

        to_remove = set()
        for row in full_rows:
            for col in range(GRID_SIZE):
                to_remove.add((row, col))
        for col in full_cols:
            for row in range(GRID_SIZE):
                to_remove.add((row, col))

        self._explode_cells(list(to_remove), effect_color)

        line_count = len(full_rows) + len(full_cols)
        if line_count >= 2:
            self._shake_board(strength=5 + line_count, times=6)

        for key in to_remove:
            self.grid[key[0]][key[1]] = None
            visual = self.board_blocks.pop(key, None)
            if visual is not None:
                for node in visual.values():
                    node.run_action(Action.sequence(
                        Action.group(
                            Action.scale_to(1.35, 0.08),
                            Action.fade_to(0.0, 0.12),
                            Action.rotate_by(0.2, 0.12),
                        ),
                        Action.remove(),
                    ))

        self.message_label.text = 'CLEAR %d LINE%s!' % (line_count, '' if line_count == 1 else 'S')
        self.message_label.color = NEON_GREEN if line_count == 1 else NEON_CYAN
        self.message_label.alpha = 1
        self.message_label.run_action(Action.sequence(
            Action.group(
                Action.scale_to(1.12, 0.08),
                Action.fade_to(1.0, 0.01),
            ),
            Action.wait(0.4),
            Action.group(
                Action.fade_to(0.0, 0.35),
                Action.scale_to(1.0, 0.35),
            ),
        ))
        return line_count, len(to_remove)

    def _update_status(self):
        self.score_label.text = 'SCORE %d' % self.score
        self.best_label.text = 'BEST %d' % self.best_score
        self.combo_label.text = 'COMBO x%d' % self.multiplier
        self.endless_label.text = 'ENDLESS' if self.endless_mode else 'CLASSIC'
        if self.multiplier > 1:
            self.combo_label.color = NEON_PINK
        else:
            self.combo_label.color = NEON_SUBTEXT
        if self.endless_mode:
            self.goal_label.text = 'Không giới hạn điểm'
            self.endless_label.color = NEON_PINK
        else:
            self.goal_label.text = 'Mục tiêu %d' % TARGET_SCORE
            self.endless_label.color = NEON_SUBTEXT

    def _check_game_state(self):
        if self.game_over or self.victory or self.show_menu:
            return

        available = [p for p in self.pieces if not p['used']]
        for piece in available:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    if self._can_place(piece, row, col):
                        return
        self._lose_game()

    def _win_game(self):
        self.victory = True
        self.game_over = True
        self.message_label.text = 'Bạn thắng!'
        self.message_label.color = NEON_GREEN
        self.message_label.alpha = 1
        self.restart_label.text = 'Chạm để mở menu'
        self.restart_label.alpha = 1
        self._show_floating_text('VICTORY!', NEON_YELLOW, (self.size.w / 2, self.board_top), dy=56, font_size=22)
        sound.play_effect('music:Victory_NES_1', volume=0.8)

    def _lose_game(self):
        self.game_over = True
        self.message_label.text = 'Hết chỗ đặt!'
        self.message_label.color = NEON_RED
        self.message_label.alpha = 1
        self.restart_label.text = 'Chạm để mở menu'
        self.restart_label.alpha = 1
        sound.play_effect('music:GameOver_NES_1', volume=0.8)

    def _back_to_menu(self):
        self.show_menu = True
        self.selected_piece = None
        self._clear_drag_nodes()
        self.message_label.alpha = 0
        self.restart_label.alpha = 0
        self.message_label.text = ''
        self.restart_label.text = ''
        self._show_start_menu()

    def _clear_drag_nodes(self):
        for node in self.drag_nodes:
            if isinstance(node, dict):
                self._remove_visual(node)
            else:
                node.remove_from_parent()
        self.drag_nodes = []
        for node in self.preview_nodes:
            if isinstance(node, dict):
                self._remove_visual(node)
            else:
                node.remove_from_parent()
        self.preview_nodes = []

    def _select_piece(self, piece):
        if piece['used'] or self.game_over or self.show_menu:
            return
        self.selected_piece = piece
        self.preview_anchor = None
        self.last_preview_valid = False
        self._clear_drag_nodes()
        self._pulse_slot(piece)

        for dx, dy in piece['cells']:
            visual = self._make_block_visual(self.world, (-100, -100), self.cell_size, piece['color'], 19, preview=False)
            for key in visual:
                visual[key].alpha = min(0.98, visual[key].alpha if hasattr(visual[key], 'alpha') else 1.0)
            visual['glow'].alpha = 0.18
            visual['shadow'].alpha = 0.22
            self.drag_nodes.append(visual)
        sound.play_effect('ui:click2', volume=0.45)

    def _update_drag_piece(self, point):
        if self.selected_piece is None:
            return

        anchor = self._best_anchor_for_point(self.selected_piece, point)
        display_point = point
        if anchor is not None:
            center_x, center_y = anchor['center']
            mix = 0.72
            display_point = Point(
                point.x * (1.0 - mix) + center_x * mix,
                point.y * (1.0 - mix) + center_y * mix,
            )

        cells = self.selected_piece['cells']
        center_offset_x, center_offset_y = self._piece_center_offset(self.selected_piece, self.cell_size)

        for i, (dx, dy) in enumerate(cells):
            x = display_point.x + dx * self.cell_size - center_offset_x
            y = display_point.y + dy * self.cell_size - center_offset_y
            self._set_block_visual_position(self.drag_nodes[i], (x, y), self.cell_size)

        self._update_preview(point)

    def _update_preview(self, point):
        for node in self.preview_nodes:
            if isinstance(node, dict):
                self._remove_visual(node)
            else:
                node.remove_from_parent()
        self.preview_nodes = []
        self.preview_anchor = None
        self.last_preview_valid = False

        if self.selected_piece is None:
            return

        anchor = self._best_anchor_for_point(self.selected_piece, point)
        if anchor is None:
            return

        self.preview_anchor = (anchor['row'], anchor['col'])
        self.last_preview_valid = anchor['can_place']
        preview_color = NEON_GREEN if anchor['can_place'] else NEON_RED

        for r, c, x, y in anchor['cells']:
            visual = self._make_block_visual(self.world, (x, y), self.cell_size, preview_color, 3, preview=True)
            visual['shadow'].alpha = 0.12
            visual['glow'].alpha = max(visual['glow'].alpha, 0.12)
            visual['tile'].alpha = 0.26 if anchor['can_place'] else 0.18
            visual['highlight'].alpha = 0.12
            visual['accent'].alpha = 0.08
            self.preview_nodes.append(visual)

    def _piece_at_point(self, point):
        for piece in self.pieces:
            if piece['used']:
                continue
            root = piece.get('root')
            if root is None:
                continue
            width, height = self._piece_bounds(piece)
            preview_cell = piece.get('preview_cell', self.cell_size * 0.58)
            half_w = width * preview_cell * 0.7
            half_h = height * preview_cell * 0.7
            if abs(point.x - root.position.x) <= half_w and abs(point.y - root.position.y) <= half_h:
                return piece
        return None

    def _menu_button_at_point(self, point):
        for name, button in self.menu_buttons.items():
            root = button['root']
            width, height = button['size']
            if abs(point.x - root.position.x) <= width / 2 and abs(point.y - root.position.y) <= height / 2:
                return ('mode', name)
        for name, button in self.skin_buttons.items():
            root = button['root']
            width, height = button['size']
            if abs(point.x - root.position.x) <= width / 2 and abs(point.y - root.position.y) <= height / 2:
                return ('skin', name)
        return None

    def touch_began(self, touch):
        if self.show_menu:
            target = self._menu_button_at_point(touch.location)
            if target is None:
                return
            target_type, target_name = target
            if target_type == 'mode':
                if target_name == 'classic':
                    self._start_game(endless=False)
                elif target_name == 'endless':
                    self._start_game(endless=True)
            elif target_type == 'skin':
                self.selected_skin = target_name
                self._refresh_skin_buttons()
                if self.pieces:
                    self._refresh_all_piece_previews()
            return

        if self.game_over:
            self._back_to_menu()
            return

        piece = self._piece_at_point(touch.location)
        if piece is not None:
            self._select_piece(piece)
            self._update_drag_piece(touch.location)

    def touch_moved(self, touch):
        if self.selected_piece is not None and not self.show_menu:
            self._update_drag_piece(touch.location)

    def touch_ended(self, touch):
        if self.selected_piece is None:
            return

        placed = False
        if self.preview_anchor is not None and self.last_preview_valid:
            row, col = self.preview_anchor
            placed = self._place_piece(self.selected_piece, row, col)

        if not placed and self.selected_piece.get('root') is not None:
            self.selected_piece['root'].run_action(Action.sequence(
                Action.scale_to(1.08, 0.08),
                Action.scale_to(1.0, 0.08)
            ))
            sound.play_effect('game:Error', volume=0.35)

        self.selected_piece = None
        self.preview_anchor = None
        self.last_preview_valid = False
        self._clear_drag_nodes()


run(BlockBlastGame(), _mode='main')
