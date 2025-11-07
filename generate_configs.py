#!/usr/bin/env python3
"""
Generate all Miryoku Kanata configuration variants programmatically.
Based on Miryoku specification and dinaldoap-miryoku.kbd reference implementation.
"""

from pathlib import Path

# Configuration options
ALPHAS = {
    'colemakdh': {
        'name': 'Colemak Mod-DH',
        'layout': ['q', 'w', 'f', 'p', 'b', 'j', 'l', 'u', 'y', "'",
                   'a', 'r', 's', 't', 'g', 'm', 'n', 'e', 'i', 'o',
                   'z', 'x', 'c', 'd', 'v', 'k', 'h', ',', '.', '/']
    },
    'qwerty': {
        'name': 'QWERTY',
        'layout': ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', "'",
                   'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
    },
    'dvorak': {
        'name': 'Dvorak',
        'layout': ["'", ',', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l',
                   'a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's',
                   '/', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z']
    },
    'colemak': {
        'name': 'Colemak',
        'layout': ['q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', "'",
                   'a', 'r', 's', 't', 'd', 'h', 'n', 'e', 'i', 'o',
                   'z', 'x', 'c', 'v', 'b', 'k', 'm', ',', '.', '/']
    },
    'colemakdhk': {
        'name': 'Colemak Mod-DHk',
        'layout': ['q', 'w', 'f', 'p', 'b', 'j', 'l', 'u', 'y', "'",
                   'a', 'r', 's', 't', 'g', 'k', 'n', 'e', 'i', 'o',
                   'z', 'x', 'c', 'd', 'v', 'm', 'h', ',', '.', '/']
    },
    'azerty': {
        'name': 'AZERTY',
        'layout': ['a', 'z', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
                   'q', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
                   'w', 'x', 'c', 'v', 'b', 'n', ',', '.', '/', "'"]
    },
    'qwertz': {
        'name': 'QWERTZ',
        'layout': ['q', 'w', 'e', 'r', 't', 'z', 'u', 'i', 'o', 'p',
                   'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', "'",
                   'y', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/']
    },
    'halmak': {
        'name': 'Halmak',
        'layout': ['w', 'l', 'r', 'b', 'z', "'", 'q', 'u', 'd', 'j',
                   's', 'h', 'n', 't', ',', '.', 'a', 'e', 'o', 'i',
                   'f', 'm', 'v', 'c', '/', 'g', 'p', 'x', 'k', 'y']
    },
    'workman': {
        'name': 'Workman',
        'layout': ['q', 'd', 'r', 'w', 'b', 'j', 'f', 'u', 'p', "'",
                   'a', 's', 'h', 't', 'g', 'y', 'n', 'e', 'o', 'i',
                   'z', 'x', 'm', 'c', 'v', 'k', 'l', ',', '.', '/']
    },
}

NAV_VARIANTS = {
    'default': 'Standard navigation (arrows on NEIO)',
    'vi': 'Vi-style navigation (shifted one column left)',
    'invertedt': 'Inverted-T navigation (arrows in T-shape)'
}

PLATFORMS = {
    'nix': {
        'name': 'Linux/Unix',
        'undo': 'C-z',
        'redo': 'C-S-z',
        'cut': 'S-del',
        'copy': 'C-ins',
        'paste': 'S-ins'
    },
    'win': {
        'name': 'Windows',
        'undo': 'C-z',
        'redo': 'C-y',
        'cut': 'S-del',
        'copy': 'C-ins',
        'paste': 'S-ins'
    },
    'mac': {
        'name': 'macOS',
        'undo': 'M-z',
        'redo': 'M-S-z',
        'cut': 'M-x',
        'copy': 'M-c',
        'paste': 'M-v'
    },
}

def generate_filename(alpha, nav, flip, platform):
    """Generate filename based on configuration."""
    parts = []
    if alpha != 'colemakdh':
        parts.append(alpha)
    if flip:
        parts.append('flip')
    if nav != 'default':
        parts.append(nav)

    name = 'miryoku-kanata'
    if parts:
        name += '-' + '-'.join(parts)
    name += f'--{platform}.kbd'
    return name

def format_layout_line(keys):
    """Format a row of keys with proper spacing."""
    return '\t'.join(keys)

def generate_base_layer(alpha_layout, flip, platform_data):
    """Generate the base layer with home row mods."""
    layout = ALPHAS[alpha_layout]['layout']

    # Home row mod positions (0-indexed in flattened 30-key layout)
    # Left hand: A(10), R(11), S(12), T(13)
    # Right hand: N(16), E(17), I(18), O(19)

    if not flip:
        # Standard: Left thumbs = Media/Nav/Mouse, Right thumbs = Sym/Num/Fun
        row1 = [layout[i] for i in range(0, 5)] + [layout[i] for i in range(5, 10)]
        row2_left = [
            f'(tap-hold-release 200 200 {layout[10]} met)',
            f'(tap-hold-release 200 200 {layout[11]} alt)',
            f'(tap-hold-release 200 200 {layout[12]} ctl)',
            f'(tap-hold-release 200 200 {layout[13]} sft)',
            layout[14]
        ]
        row2_right = [
            layout[15],
            f'(tap-hold-release 200 200 {layout[16]} sft)',
            f'(tap-hold-release 200 200 {layout[17]} ctl)',
            f'(tap-hold-release 200 200 {layout[18]} alt)',
            f'(tap-hold-release 200 200 {layout[19]} met)'
        ]
        row3 = [
            f'(tap-hold-release 200 200 {layout[20]} (layer-toggle U_BUTTON))',
            f'(tap-hold-release 200 200 {layout[21]} ralt)',
            layout[22], layout[23], layout[24],
            layout[25], layout[26], layout[27],
            f'(tap-hold-release 200 200 {layout[28]} ralt)',
            f'(tap-hold-release 200 200 {layout[29]} (layer-toggle U_BUTTON))'
        ]
        thumbs = [
            '(tap-hold-release 200 200 esc (layer-toggle U_MEDIA))',
            '(tap-hold-release 200 200 spc (layer-toggle U_NAV))',
            '(tap-hold-release 200 200 tab (layer-toggle U_MOUSE))',
            '(tap-hold-release 200 200 ent (layer-toggle U_SYM))',
            '(tap-hold-release 200 200 bspc (layer-toggle U_NUM))',
            '(tap-hold-release 200 200 del (layer-toggle U_FUN))'
        ]
    else:
        # Flipped: Right thumbs = Media/Nav/Mouse, Left thumbs = Sym/Num/Fun
        row1 = [layout[i] for i in range(0, 5)] + [layout[i] for i in range(5, 10)]
        row2_left = [
            f'(tap-hold-release 200 200 {layout[10]} met)',
            f'(tap-hold-release 200 200 {layout[11]} alt)',
            f'(tap-hold-release 200 200 {layout[12]} ctl)',
            f'(tap-hold-release 200 200 {layout[13]} sft)',
            layout[14]
        ]
        row2_right = [
            layout[15],
            f'(tap-hold-release 200 200 {layout[16]} sft)',
            f'(tap-hold-release 200 200 {layout[17]} ctl)',
            f'(tap-hold-release 200 200 {layout[18]} alt)',
            f'(tap-hold-release 200 200 {layout[19]} met)'
        ]
        row3 = [
            f'(tap-hold-release 200 200 {layout[20]} (layer-toggle U_BUTTON))',
            f'(tap-hold-release 200 200 {layout[21]} ralt)',
            layout[22], layout[23], layout[24],
            layout[25], layout[26], layout[27],
            f'(tap-hold-release 200 200 {layout[28]} ralt)',
            f'(tap-hold-release 200 200 {layout[29]} (layer-toggle U_BUTTON))'
        ]
        thumbs = [
            '(tap-hold-release 200 200 ent (layer-toggle U_SYM))',
            '(tap-hold-release 200 200 bspc (layer-toggle U_NUM))',
            '(tap-hold-release 200 200 del (layer-toggle U_FUN))',
            '(tap-hold-release 200 200 esc (layer-toggle U_MEDIA))',
            '(tap-hold-release 200 200 spc (layer-toggle U_NAV))',
            '(tap-hold-release 200 200 tab (layer-toggle U_MOUSE))'
        ]

    lines = []
    lines.append('(deflayer U_BASE')
    lines.append(format_layout_line(row1))
    lines.append(format_layout_line(row2_left + row2_right))
    lines.append(format_layout_line(row3))
    lines.append('\t\t' + '\t'.join(thumbs))
    lines.append(')')
    return '\n'.join(lines)

def generate_nav_layer(nav_variant, flip, platform_data):
    """Generate navigation layer."""
    undo, redo, cut, copy, paste = (
        platform_data['undo'], platform_data['redo'],
        platform_data['cut'], platform_data['copy'], platform_data['paste']
    )

    if nav_variant == 'default':
        # Standard: arrows on NEIO (right home row)
        row1_left = ['XX', '(tap-dance 200 (XX (layer-switch U_TAP)))',
                     '(tap-dance 200 (XX (layer-switch U_EXTRA)))',
                     '(tap-dance 200 (XX (layer-switch U_BASE)))', 'XX']
        row1_right = [redo, paste, copy, cut, undo]
        row2_left = ['met', 'alt', 'ctl', 'sft', 'XX']
        row2_right = ['caps', 'left', 'down', 'up', 'right']
        row3_left = ['XX', 'ralt', '(tap-dance 200 (XX (layer-switch U_NUM)))',
                     '(tap-dance 200 (XX (layer-switch U_NAV)))', 'XX']
        row3_right = ['ins', 'home', 'pgdn', 'pgup', 'end']
    elif nav_variant == 'vi':
        # Vi-style: shifted one column left
        row1_left = ['XX', '(tap-dance 200 (XX (layer-switch U_TAP)))',
                     '(tap-dance 200 (XX (layer-switch U_EXTRA)))',
                     '(tap-dance 200 (XX (layer-switch U_BASE)))', 'XX']
        row1_right = [redo, paste, copy, cut, undo]
        row2_left = ['met', 'alt', 'ctl', 'sft', 'XX']
        row2_right = ['caps', 'down', 'up', 'right', 'XX']  # hjkl positions
        row3_left = ['XX', 'ralt', '(tap-dance 200 (XX (layer-switch U_NUM)))',
                     '(tap-dance 200 (XX (layer-switch U_NAV)))', 'XX']
        row3_right = ['ins', 'XX', 'left', 'pgdn', 'pgup']
    else:  # invertedt
        # Inverted-T: arrow keys in T shape
        row1_left = ['XX', '(tap-dance 200 (XX (layer-switch U_TAP)))',
                     '(tap-dance 200 (XX (layer-switch U_EXTRA)))',
                     '(tap-dance 200 (XX (layer-switch U_BASE)))', 'XX']
        row1_right = [redo, paste, copy, cut, undo]
        row2_left = ['met', 'alt', 'ctl', 'sft', 'XX']
        row2_right = ['ins', 'home', 'up', 'end', 'caps']
        row3_left = ['XX', 'ralt', '(tap-dance 200 (XX (layer-switch U_NUM)))',
                     '(tap-dance 200 (XX (layer-switch U_NAV)))', 'XX']
        row3_right = ['XX', 'left', 'down', 'right', 'XX']

    thumbs = ['XX', 'XX', 'XX', 'ent', 'bspc', 'del'] if not flip else ['ent', 'bspc', 'del', 'XX', 'XX', 'XX']

    lines = []
    lines.append('(deflayer U_NAV')
    lines.append(format_layout_line(row1_left + row1_right))
    lines.append(format_layout_line(row2_left + row2_right))
    lines.append(format_layout_line(row3_left + row3_right))
    lines.append('\t\t' + '\t'.join(thumbs))
    lines.append(')')
    return '\n'.join(lines)

def generate_config(alpha, nav, flip, platform):
    """Generate complete Kanata configuration."""
    alpha_data = ALPHAS[alpha]
    platform_data = PLATFORMS[platform]

    undo, redo, cut, copy, paste = (
        platform_data['undo'], platform_data['redo'],
        platform_data['cut'], platform_data['copy'], platform_data['paste']
    )

    config = f''';; Miryoku Kanata Configuration
;;
;; Alpha Layout: {alpha_data['name']}
;; Navigation: {NAV_VARIANTS[nav]}
;; Layers: {'Flipped' if flip else 'Standard'}
;; Platform: {platform_data['name']}
;;
;; Generated from Miryoku specification
;; https://github.com/manna-harbour/miryoku

(defcfg
  process-unmapped-keys yes
  block-unmapped-keys yes
)

;; Source: 36-key layout
(defsrc
  q w e r t   y u i o p
  a s d f g   h j k l ;
  z x c v b   n m , . /
  esc spc tab   ent bspc del
)

;; Base Layer - {alpha_data['name']} with home row mods
{generate_base_layer(alpha, flip, platform_data)}

;; Extra Layer - QWERTY alternative (switchable via tap-dance)
(deflayer U_EXTRA
q\tw\te\tr\tt\ty\tu\ti\to\tp
(tap-hold-release 200 200 a met)\t(tap-hold-release 200 200 s alt)\t(tap-hold-release 200 200 d ctl)\t(tap-hold-release 200 200 f sft)\tg\th\t(tap-hold-release 200 200 j sft)\t(tap-hold-release 200 200 k ctl)\t(tap-hold-release 200 200 l alt)\t(tap-hold-release 200 200 ' met)
(tap-hold-release 200 200 z (layer-toggle U_BUTTON))\t(tap-hold-release 200 200 x ralt)\tc\tv\tb\tn\tm\t,\t(tap-hold-release 200 200 . ralt)\t(tap-hold-release 200 200 / (layer-toggle U_BUTTON))
\t\t{'(tap-hold-release 200 200 esc (layer-toggle U_MEDIA))\t(tap-hold-release 200 200 spc (layer-toggle U_NAV))\t(tap-hold-release 200 200 tab (layer-toggle U_MOUSE))\t(tap-hold-release 200 200 ent (layer-toggle U_SYM))\t(tap-hold-release 200 200 bspc (layer-toggle U_NUM))\t(tap-hold-release 200 200 del (layer-toggle U_FUN))' if not flip else '(tap-hold-release 200 200 ent (layer-toggle U_SYM))\t(tap-hold-release 200 200 bspc (layer-toggle U_NUM))\t(tap-hold-release 200 200 del (layer-toggle U_FUN))\t(tap-hold-release 200 200 esc (layer-toggle U_MEDIA))\t(tap-hold-release 200 200 spc (layer-toggle U_NAV))\t(tap-hold-release 200 200 tab (layer-toggle U_MOUSE))'}
)

;; Tap Layer - No dual-function keys
(deflayer U_TAP
{format_layout_line(ALPHAS[alpha]['layout'][:10])}
{format_layout_line(ALPHAS[alpha]['layout'][10:20])}
{format_layout_line(ALPHAS[alpha]['layout'][20:30])}
\t\tesc\tspc\ttab\tent\tbspc\tdel
)

;; Navigation Layer
{generate_nav_layer(nav, flip, platform_data)}

;; Mouse Layer
(deflayer U_MOUSE
XX\t(tap-dance 200 (XX (layer-switch U_TAP)))\t(tap-dance 200 (XX (layer-switch U_EXTRA)))\t(tap-dance 200 (XX (layer-switch U_BASE)))\tXX\t{redo}\t{paste}\t{copy}\t{cut}\t{undo}
met\talt\tctl\tsft\tXX\tXX\t(movemouse-left 5 1)\t(movemouse-down 5 1)\t(movemouse-up 5 1)\t(movemouse-right 5 1)
XX\tralt\t(tap-dance 200 (XX (layer-switch U_SYM)))\t(tap-dance 200 (XX (layer-switch U_MOUSE)))\tXX\tXX\tXX\tXX\tXX\tXX
\t\t{'XX\tXX\tXX\tmrgt\tmlft\tmmid' if not flip else 'mrgt\tmlft\tmmid\tXX\tXX\tXX'}
)

;; Button Layer
(deflayer U_BUTTON
{undo}\t{cut}\t{copy}\t{paste}\t{redo}\t{redo}\t{paste}\t{copy}\t{cut}\t{undo}
met\talt\tctl\tsft\tXX\tXX\tsft\tctl\talt\tmet
{undo}\t{cut}\t{copy}\t{paste}\t{undo}\t{undo}\t{paste}\t{copy}\t{cut}\t{undo}
\t\tmmid\tmlft\tmrgt\tmrgt\tmlft\tmmid
)

;; Media Layer
(deflayer U_MEDIA
XX\t(tap-dance 200 (XX (layer-switch U_TAP)))\t(tap-dance 200 (XX (layer-switch U_EXTRA)))\t(tap-dance 200 (XX (layer-switch U_BASE)))\tXX\tXX\tXX\tXX\tXX\tXX
met\talt\tctl\tsft\tXX\tXX\tprev\tvold\tvolu\tnext
XX\tralt\t(tap-dance 200 (XX (layer-switch U_FUN)))\t(tap-dance 200 (XX (layer-switch U_MEDIA)))\tXX\tXX\tXX\tXX\tXX\tXX
\t\t{'XX\tXX\tXX\tXX\tpp\tmute' if not flip else 'XX\tpp\tmute\tXX\tXX\tXX'}
)

;; Number Layer
(deflayer U_NUM
[\t7\t8\t9\t]\tXX\t(tap-dance 200 (XX (layer-switch U_BASE)))\t(tap-dance 200 (XX (layer-switch U_EXTRA)))\t(tap-dance 200 (XX (layer-switch U_TAP)))\tXX
;\t4\t5\t6\t=\tXX\tsft\tctl\talt\tmet
`\t1\t2\t3\t\\\tXX\t(tap-dance 200 (XX (layer-switch U_NUM)))\t(tap-dance 200 (XX (layer-switch U_NAV)))\tralt\tXX
\t\t{'.\t0\t-\tXX\tXX\tXX' if not flip else 'XX\tXX\tXX\t.\t0\t-'}
)

;; Symbol Layer
(deflayer U_SYM
S-{{\tS-7\tS-8\tS-9\tS-}}\tXX\t(tap-dance 200 (XX (layer-switch U_BASE)))\t(tap-dance 200 (XX (layer-switch U_EXTRA)))\t(tap-dance 200 (XX (layer-switch U_TAP)))\tXX
S-scln\tS-4\tS-5\tS-6\tS-eql\tXX\tsft\tctl\talt\tmet
S-grv\tS-1\tS-2\tS-3\tS-\\\tXX\t(tap-dance 200 (XX (layer-switch U_SYM)))\t(tap-dance 200 (XX (layer-switch U_MOUSE)))\tralt\tXX
\t\t{'S-9\tS-0\tS-min\tXX\tXX\tXX' if not flip else 'XX\tXX\tXX\tS-9\tS-0\tS-min'}
)

;; Function Layer
(deflayer U_FUN
f12\tf7\tf8\tf9\t102d\tXX\t(tap-dance 200 (XX (layer-switch U_BASE)))\t(tap-dance 200 (XX (layer-switch U_EXTRA)))\t(tap-dance 200 (XX (layer-switch U_TAP)))\tXX
f11\tf4\tf5\tf6\tslck\tXX\tsft\tctl\talt\tmet
f10\tf1\tf2\tf3\tpause\tXX\t(tap-dance 200 (XX (layer-switch U_FUN)))\t(tap-dance 200 (XX (layer-switch U_MEDIA)))\tralt\tXX
\t\t{'comp\tspc\ttab\tXX\tXX\tXX' if not flip else 'XX\tXX\tXX\tcomp\tspc\ttab'}
)
'''

    return config

def main():
    """Generate all configuration files."""
    base_output_dir = Path('.')
    configs_generated = []

    for alpha in ALPHAS.keys():
        for nav in NAV_VARIANTS.keys():
            for flip in [False, True]:
                # Skip vi+flip combination (not supported per Miryoku docs)
                if nav == 'vi' and flip:
                    continue

                for platform in PLATFORMS.keys():
                    # Create folder structure: alpha/platform/
                    output_dir = base_output_dir / alpha / platform
                    output_dir.mkdir(parents=True, exist_ok=True)

                    filename = generate_filename(alpha, nav, flip, platform)
                    filepath = output_dir / filename

                    content = generate_config(alpha, nav, flip, platform)

                    # Write file
                    filepath.write_text(content)
                    configs_generated.append(f"{alpha}/{platform}/{filename}")

    print(f"✓ Generated {len(configs_generated)} Miryoku Kanata configurations")
    print(f"\nBreakdown:")
    print(f"  • {len([c for c in configs_generated if '--nix' in c])} Linux/Unix configs")
    print(f"  • {len([c for c in configs_generated if '--win' in c])} Windows configs")
    print(f"  • {len([c for c in configs_generated if '--mac' in c])} macOS configs")

    # Show some examples
    print(f"\nSample configurations:")
    examples = [
        'miryoku-kanata--nix.kbd',
        'miryoku-kanata-qwerty--win.kbd',
        'miryoku-kanata-dvorak--mac.kbd',
        'miryoku-kanata-vi--nix.kbd',
        'miryoku-kanata-flip-invertedt--nix.kbd',
        'miryoku-kanata-qwerty-flip--win.kbd'
    ]
    for ex in examples:
        if ex in configs_generated:
            print(f"  • {ex}")

if __name__ == '__main__':
    main()
