#!/usr/bin/env python3
"""Draw entry.png: a world map of 19 November 2026's top stories.

Layout (1024x1024):
  - navy banner with the date
  - pale-ocean world map with simplified continents and numbered pins
  - numbered legend of the day's stories at the bottom
Only verified facts from the news brief are used; nothing is invented.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

# Map region and equirectangular-ish projection.
MAP_X0, MAP_Y0 = 10, 92
MAP_W, MAP_H = 1004, 556
LON_MIN, LON_MAX = -170.0, 190.0
LAT_MAX, LAT_MIN = 75.0, -55.0


def project(lon, lat):
    x = MAP_X0 + (lon - LON_MIN) / (LON_MAX - LON_MIN) * MAP_W
    y = MAP_Y0 + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * MAP_H
    return (x, y)


def poly(points):
    return [project(lon, lat) for lon, lat in points]


# Simplified continent outlines, as (lon, lat) vertices.
NORTH_AMERICA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69),
                 (-85, 66), (-80, 73), (-65, 60), (-55, 52), (-60, 47),
                 (-70, 42), (-75, 35), (-80, 32), (-81, 26), (-84, 30),
                 (-90, 21), (-97, 16), (-94, 17), (-105, 20), (-110, 24),
                 (-117, 33), (-125, 40), (-124, 48), (-135, 58),
                 (-155, 58), (-165, 60), (-168, 66)]
GREENLAND = [(-58, 64), (-45, 60), (-32, 68), (-25, 70), (-40, 76),
             (-58, 76), (-60, 70)]
SOUTH_AMERICA = [(-79, 9), (-72, 12), (-62, 11), (-52, 5), (-50, 0),
                 (-44, -3), (-35, -8), (-40, -20), (-48, -28), (-57, -38),
                 (-65, -41), (-68, -52), (-70, -54), (-73, -44),
                 (-73, -30), (-70, -18), (-77, -12), (-81, -5),
                 (-80, 1), (-79, 9)]
AFRICA = [(-6, 35), (-10, 31), (-17, 15), (-17, 12), (-13, 8), (-8, 5),
          (0, 6), (9, 4), (9, -1), (13, -12), (12, -18), (15, -27),
          (20, -35), (28, -33), (35, -24), (40, -16), (41, -10),
          (51, -11), (51, 2), (46, 11), (43, 12), (39, 15), (37, 18),
          (33, 27), (32, 31), (22, 33), (11, 34), (10, 37), (-6, 35)]
EUROPE = [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (0, 51), (3, 53),
          (8, 57), (10, 59), (5, 60), (12, 56), (18, 56), (21, 55),
          (24, 59), (21, 65), (25, 71), (30, 70), (40, 68), (44, 68),
          (40, 60), (35, 55), (30, 50), (28, 45), (23, 40), (26, 38),
          (23, 36), (19, 42), (12, 44), (8, 44), (3, 42), (0, 38),
          (-9, 37), (-10, 36)]
ASIA = [(30, 70), (40, 68), (50, 69), (60, 69), (70, 72), (80, 73),
        (90, 75), (100, 76), (110, 74), (120, 73), (130, 72), (140, 72),
        (150, 70), (158, 66), (162, 60), (158, 52), (150, 59), (142, 55),
        (140, 50), (135, 44), (130, 42), (127, 40), (122, 38), (120, 32),
        (122, 28), (114, 22), (108, 18), (105, 10), (100, 8), (98, 12),
        (94, 17), (91, 22), (88, 22), (86, 20), (80, 15), (77, 8),
        (75, 12), (72, 20), (66, 25), (62, 25), (58, 26), (56, 27),
        (52, 26), (50, 29), (48, 30), (44, 29), (40, 31), (36, 36),
        (33, 31), (30, 36), (30, 41), (28, 45), (30, 46), (30, 50),
        (28, 55), (30, 60), (30, 70)]
AUSTRALIA = [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
             (114, -22)]
SUMATRA = [(95, 5), (100, 0), (104, -3), (106, -6), (100, -2), (95, 5)]
BORNEO = [(109, 1), (113, 4), (117, 6), (119, 1), (117, -3), (113, -3),
          (110, -1)]
NEW_GUINEA = [(131, -1), (136, -2), (141, -3), (146, -6), (150, -8),
              (147, -9), (141, -8), (136, -6), (131, -1)]
JAPAN = [(130, 31), (133, 34), (137, 35), (140, 38), (141, 41),
         (143, 43), (141, 45), (139, 41), (136, 37), (132, 33), (130, 31)]
BRITAIN = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53),
           (-5, 50)]

CONTINENTS = [NORTH_AMERICA, GREENLAND, SOUTH_AMERICA, AFRICA, EUROPE,
              ASIA, AUSTRALIA, SUMATRA, BORNEO, NEW_GUINEA, JAPAN, BRITAIN]

# (number, lon, lat, headline, detail)
STORIES = [
    (1, 114.1, 22.5,
     "Trump, Xi and Putin meet in Shenzhen",
     "first-ever trilateral at APEC"),
    (2, 48.0, 29.4,
     "Iran war widens in the Gulf",
     "US bases in Kuwait and Bahrain hit"),
    (3, 34.5, 31.5,
     "Israel opens Gaza ground operation",
     "tanks cross the Yellow Line"),
    (4, 83.3, 17.7,
     "Cyclone Akvan nears Andhra coast",
     "landfall Friday, winds to 120 kmph"),
    (5, 77.2, 28.6,
     "William and Kate meet Modi in Delhi",
     "royal visit to India ends"),
    (6, -77.0, 38.9,
     "Jeffries nominated US House Speaker",
     "first Black Speaker expected"),
    (7, -74.0, 40.7,
     "Anthropic IPO debuts on Nasdaq",
     "shares at $83, valued near $1.5tn"),
]

NAVY = (27, 42, 74)
OCEAN = (220, 232, 242)
LAND = (143, 166, 189)
LABEL_DARK = (90, 109, 132)
LABEL_OCEAN = (122, 147, 173)
RED = (214, 48, 49)
WHITE = (255, 255, 255)
INK = (30, 41, 59)
GREY = (100, 116, 139)
GOLD = (245, 176, 65)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # --- Banner ---
    d.rectangle([0, 0, W, 92], fill=NAVY)
    title = font("DejaVuSans-Bold.ttf", 44)
    d.text((W // 2, 14), "THE WORLD — 19 NOVEMBER 2026",
           font=title, fill=WHITE, anchor="ma")
    sub = font("DejaVuSans.ttf", 20)
    d.text((W // 2, 62), "Thursday's top stories, mapped",
           font=sub, fill=(176, 190, 205), anchor="ma")

    # --- Ocean + graticule ---
    d.rectangle([0, 92, W, 648], fill=OCEAN)
    for lon in range(-150, 181, 30):
        x, _ = project(lon, 0)
        d.line([(x, 92), (x, 648)], fill=(255, 255, 255), width=1)
    for lat in range(60, -61, -30):
        _, y = project(0, lat)
        d.line([(0, y), (W, y)], fill=(255, 255, 255), width=1)

    # --- Continents ---
    for cont in CONTINENTS:
        d.polygon(poly(cont), fill=LAND)

    # --- Place labels ---
    lab = font("DejaVuSans-Bold.ttf", 17)
    for text, lon, lat in [
            ("NORTH AMERICA", -100, 50), ("SOUTH AMERICA", -60, -15),
            ("AFRICA", 20, 5), ("EUROPE", 15, 52), ("ASIA", 100, 55),
            ("AUSTRALIA", 134, -25)]:
        x, y = project(lon, lat)
        d.text((x, y), text, font=lab, fill=LABEL_DARK, anchor="mm")
    ocean_lab = font("DejaVuSans.ttf", 17)
    for text, lon, lat in [("PACIFIC OCEAN", -140, -10),
                           ("ATLANTIC OCEAN", -30, -5),
                           ("INDIAN OCEAN", 80, -30)]:
        x, y = project(lon, lat)
        d.text((x, y), text, font=ocean_lab, fill=LABEL_OCEAN, anchor="mm")

    # --- Pins ---
    pin_num = font("DejaVuSans-Bold.ttf", 18)
    # New York's true spot is almost on top of Washington's, so its pin is
    # offset with a leader line to the true location.
    ny_true = project(-74.0, 40.7)
    ny_pin = (ny_true[0] + 27, ny_true[1] - 17)
    d.line([ny_pin, ny_true], fill=RED, width=2)
    d.ellipse([ny_true[0] - 4, ny_true[1] - 4,
               ny_true[0] + 4, ny_true[1] + 4], fill=WHITE, outline=RED,
              width=2)
    for num, lon, lat, _, _ in STORIES:
        if num == 7:
            cx, cy = ny_pin
        else:
            cx, cy = project(lon, lat)
        d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=RED,
                  outline=WHITE, width=2)
        d.text((cx, cy - 1), str(num), font=pin_num, fill=WHITE, anchor="mm")

    # --- Legend ---
    d.rectangle([0, 648, W, H], fill=WHITE)
    head = font("DejaVuSans-Bold.ttf", 26)
    d.text((30, 660), "TODAY'S TOP STORIES", font=head, fill=NAVY)
    d.line([(30, 696), (W - 30, 696)], fill=(203, 213, 225), width=2)
    bold = font("DejaVuSans-Bold.ttf", 21)
    reg = font("DejaVuSans.ttf", 19)
    small_num = font("DejaVuSans-Bold.ttf", 15)
    y = 706
    for num, _, _, headline, detail in STORIES:
        cx, cy = 44, y + 17
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=RED)
        d.text((cx, cy - 1), str(num), font=small_num, fill=WHITE,
               anchor="mm")
        d.text((66, y), headline, font=bold, fill=INK)
        hw = d.textlength(headline, font=bold)
        d.text((66 + hw + 10, y + 1), "· " + detail, font=reg, fill=GREY)
        y += 38
    also = font("DejaVuSans.ttf", 18)
    d.text((30, 978), "Also today: GTA VI launches at midnight  ·  "
           "Takaichi meets Putin at APEC", font=also, fill=LABEL_DARK)
    src = font("DejaVuSans.ttf", 15)
    d.text((30, 1004), "Sources: Yonhap · Nikkei Asia · Dawn · Firstpost · "
           "Japan Times · Gulf News", font=src, fill=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
