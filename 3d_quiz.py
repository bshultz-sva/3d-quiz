"""3D QUIZ: a flip-card study game for the After Effects 3D material.

Cards come from the class recordings in Motion Design: the diorama class
(diorama_export (1): built-in 3D geometry, cameras, lights, Substance materials,
Media Encoder and compression, Photoshop batch actions) and the time travel class
(time travel: 2.5D, 3D layers, lights and material options, per-character 3D,
keying, Auto-Orient, the photo tunnel, depth of field and rack focus).
Starred cards are things the teacher flagged in class as quiz material or kept repeating.

Space or click flips a card. Then Y or the Right arrow if you knew it, N or the Left arrow if
you didn't. Missed cards come back a few cards later until you get them, and the
end screen lets you go over just the ones you missed.

Everything can also be clicked or tapped (the decks, the card, the answer buttons, Menu), so it
plays in a web browser and on touch screens too. The web version is built with pygbag.

Run:  python3 3d_quiz.py
"""
import asyncio
import random
import sys

import pygame

WEB = sys.platform == "emscripten"  # running in a browser (pygbag)

# --- The cards: (deck, front, back, note, flagged in class) ---

SPACE = "3D space & layers"
CAMERAS = "Cameras"
LIGHTS = "Lights & materials"
TRICKS = "Text, keying & tricks"
OUTPUT = "Output & compression"

CARDS = [
    # 3D space & layers
    (SPACE, "What is 2.5D?", "2D images (flat layers) arranged and moved in 3D space", "", False),
    (SPACE, "How do you make a 2D layer 3D?", "Turn on its 3D Layer switch (the little cube) in the timeline", "", False),
    (SPACE, "What new axis do you get when a layer becomes 3D?", "Z (depth)",
     "Anchor point, position and scale all become X, Y, Z.", False),
    (SPACE, "Where is 0,0 in a comp, and which way is positive?",
     "Top left corner. Right is positive X, down is positive Y",
     "Left and up are negative. On Z, positive goes farther away from the viewer.", False),
    (SPACE, "Does scaling a 3D layer's Z make it thicker?", "No. 3D layers are flat; Z scale doesn't extrude them", "", False),
    (SPACE, "X, Y and Z Rotation vs Orientation: what's the difference?",
     "X/Y/Z Rotation are object-based. Orientation is scene-based",
     "Football trick: tip it back with Orientation, then spin it on Y Rotation.", False),
    (SPACE, "How do you move a 3D layer along just one axis?", "Drag that axis arrow (it constrains the move)", "", False),
    (SPACE, "What does a 2D layer's anchor point become on a 3D layer?", "An axis you rotate around (X, Y and Z)", "", False),
    (SPACE, "Which renderer do you need for the built-in 3D shapes and 3D models?", "Advanced 3D",
     "Classic 3D is for 2D layers in 3D space. A Cinema 4D renderer is also built in.", False),
    (SPACE, "Name some of the built-in 3D shapes in Advanced 3D", "Sphere, torus, cube, plane, cone, cylinder",
     "A torus has ring radius, pipe radius and sides (3 sides = triangle, 8 = octagon).", False),
    (SPACE, "What should you always think about when you start working in 3D?", "The center of the world (0, 0, 0)",
     "New things line up there. Build away from it and you waste time later.", True),
    (SPACE, "What 3D model file types did the class download?", "GLB and FBX", "", False),
    (SPACE, "What does After Effects ask when you import an FBX or GLB?", "Whether to Make Comp Size / Set Effect Position", "", False),
    (SPACE, "Where did the class get free 3D models and materials?",
     "Adobe Substance 3D community assets, Pixabay, and Pixel Lab", "", False),
    (SPACE, "What is an .SBSAR file?", "A Substance material (a \"smart\" material) from the Substance community", "", False),
    (SPACE, "What does displacement do on a 3D plane's material?",
     "Uses the grayscale of the map to push the surface up and down (like cobblestones)",
     "It needs subdivisions to look good.", False),
    (SPACE, "How do you hide layers from the timeline so it's not cluttered?", "Make them shy, then turn on Hide Shy Layers", "", False),
    (SPACE, "Hot key to add selected footage to the comp, centered", "Cmd + /  (Ctrl + / on Windows)",
     "Also File > Add Footage to Comp.", False),
    (SPACE, "How was the photo tunnel laid out?",
     "Images on the 0 and 1280 lines (left and right edges), stepping back 500 on Z each row",
     "Leave a hole down the middle for the camera.", False),
    (SPACE, "Hot key for a new solid", "Cmd + Y  (Ctrl + Y on Windows)", "", False),
    (SPACE, "How do you get a perfect 50% gray?", "In the color picker, type 50 for brightness (B)", "", False),
    (SPACE, "Hot key to show all of a layer's properties", "Cmd + ~  (Ctrl + ~ on Windows)", "", False),

    # Cameras
    (CAMERAS, "What renders in a 3D comp?", "The active camera",
     "\"The active camera is what renders.\" Said over and over in class.", True),
    (CAMERAS, "Two cameras are in the comp. Which one is the active camera?", "The top one in the layer order",
     "Cut between cameras by trimming their layers (shot one, shot two).", True),
    (CAMERAS, "One-node camera vs two-node camera?",
     "One-node: just a position; it looks where you rotate it. Two-node: position plus a point of interest (target)", "",
     True),
    (CAMERAS, "On a two-node camera or spotlight, what does pressing A show?", "The point of interest",
     "The point of interest takes the place of the anchor point.", True),
    (CAMERAS, "What does AA show on a camera, light or 3D layer?", "Its options (camera options, light options, material options)",
     "\"I said it before 500 times. AA.\" Double-clicking the layer works too.", True),
    (CAMERAS, "How do you reset a 3D view?", "View > Reset Default Camera (Reset 3D View)",
     "\"That's a definite quiz question.\"", True),
    (CAMERAS, "What key cycles through the camera tools (orbit, pan, dolly)?", "C", "", False),
    (CAMERAS, "What is an Orbit Null, and how do you make one?",
     "A null the camera is attached to; rotate the null to circle the scene. Layer > Camera > Create Orbit Null",
     "Only works on a two-node camera.", True),
    (CAMERAS, "Name two other things in Layer > Camera besides Orbit Null", "Create Camera From 3D View, and Create Stereo 3D Rig",
     "The stereo rig is for red and blue glasses.", False),
    (CAMERAS, "Why did people once parent the camera to a null?",
     "The original After Effects camera was two-node only; a null let you move it like a hand-held camera",
     "Now there's a one-node camera, so you don't need to.", False),
    (CAMERAS, "Which camera did the class use to push down the hall in the tunnel?", "A one-node camera (35 mm lens)", "", False),
    (CAMERAS, "Shorter lens (20 mm) vs longer lens (200 mm)?",
     "Shorter lens opens up the view (wider). Longer lens gives a further throw (you see farther down the tunnel)", "", False),
    (CAMERAS, "How do you change a camera's lens?", "Double-click the camera layer and pick a preset (15, 20, 35, 50, 80, 200 mm)", "", False),
    (CAMERAS, "\"Breaking news\" camera move: what do you animate?",
     "The two-node camera's position AND point of interest together (e.g. 0,0 to 1920,1080)", "", False),
    (CAMERAS, "What do you turn on to get camera blur in 3D?", "Depth of Field (in the camera options)",
     "Turn the Blur Level up (e.g. 800%) to really see it.", False),
    (CAMERAS, "What is the aperture?", "The opening of the iris; it lets light in and controls how much blur you get", "", False),
    (CAMERAS, "Name some camera Iris Shapes", "Fast Rectangle, Triangle, Square, Hexagon (up to Decagon)",
     "Iris rotation and roundness change the bokeh too. Save first; it's heavy on the computer.", False),
    (CAMERAS, "What is a rack focus?",
     "Changing the focus distance during a shot to reveal something that was already in the frame", "", False),
    (CAMERAS, "How do you animate a rack focus in the tunnel?", "Keyframe Focus Distance (+500 moves focus back one row)", "", False),
    (CAMERAS, "Name three things a rack focus gains you",
     "Controls the viewer's eye, shows layered depth, visual storytelling, saves shots (economic), emotional connection", "",
     False),
    (CAMERAS, "Which key moves a layer's in point to the current time (to cut to the second camera)?", "[  (left bracket)", "", False),
    (CAMERAS, "Rule for flying the camera past objects?", "Don't fly into an object (unless you really mean to)", "", False),

    # Lights & materials
    (LIGHTS, "Name the light types", "Parallel, spot, point, ambient, and environment",
     "Environment only works in the Advanced 3D renderer.", False),
    (LIGHTS, "What is a point light?", "A 360-degree light, like a bare bulb", "", False),
    (LIGHTS, "Which light has no direction and casts no shadows?", "Ambient", "", False),
    (LIGHTS, "Which light only works in the Advanced 3D renderer?", "Environment light",
     "With 3D geometry you need an environment light plus a point light to get shadows.", True),
    (LIGHTS, "Spotlight default settings?", "Intensity 100%, cone angle 90, cone feather 50%", "", False),
    (LIGHTS, "Is a spotlight one-node or two-node?", "Two-node: it has a point of interest",
     "If you only move its position, it flips around; drag its axis instead.", False),
    (LIGHTS, "You turned on Casts Shadows on the light but see no shadow. What else do you need?",
     "Turn on Casts Shadows on the layer too (its Material Options, AA)",
     "In most 3D programs the light controls shadows; here the layer has to cast them as well.", True),
    (LIGHTS, "What does Casts Shadows: Only do?", "Hides the layer and shows only its shadow",
     "Great for puppet theater and silhouettes.", False),
    (LIGHTS, "What is Light Transmission?", "Lets light pass through a layer and cast its colors (like stained glass)",
     "It works like a gobo.", True),
    (LIGHTS, "What is a gobo, and why use one?", "A cutout projected by a light (like concert lights)",
     "Projecting foliage with a light saves the processing of building real trees.", False),
    (LIGHTS, "Shadows are noisy. Where do you make them smoother?",
     "Composition Settings (Cmd + K) > 3D Renderer > Options: raise Quality and shadow resolution",
     "Smoother, but slower to render.", False),
    (LIGHTS, "Hot key for Composition Settings", "Cmd + K  (Ctrl + K on Windows)", "", False),
    (LIGHTS, "Draft 3D vs full: which shows shadows properly?", "Full (turn Draft 3D off)", "", False),
    (LIGHTS, "Name the Material Options that change how a surface looks",
     "Diffuse, Specular Intensity, Specular Shininess, Metal", "", False),
    (LIGHTS, "What is a specular?", "The sparkle highlight (lights on a river at night, glasses, earrings)", "", True),
    (LIGHTS, "Glossy \"trading card\" shine: what settings?", "Specular Intensity and Shininess up to 100, Metal down to 0",
     "Metal at 0 gives a white highlight instead of the layer's color.", False),
    (LIGHTS, "Light shows a hot spot. Which material option do you adjust?", "Diffuse", "", False),
    (LIGHTS, "How did the class fade a light up dramatically?", "Keyframe Intensity from 0 to 100 over 2 seconds", "", False),
    (LIGHTS, "Where do you get Substance materials inside After Effects?", "Layer > Material > Get Substance Community Assets", "",
     False),

    # Text, keying & tricks
    (TRICKS, "How do text animators work in 3D?", "Turn on per-character 3D: Animate > Enable Per-character 3D",
     "The 3D switch shows two little cubes.", True),
    (TRICKS, "Where do you move the anchor point of each character for per-character 3D?",
     "More Options > Grouping Alignment",
     "\"No tutorial ever talks about it.\" Use it to swing letters from the top like a pendulum.", True),
    (TRICKS, "How did the class make floating dust in a spotlight?",
     "A text layer of periods, per-character 3D, spread with position, and a Wiggly selector set to a slow wiggle (0.05)", "",
     False),
    (TRICKS, "What is billboarding?", "A flat image on one poly that always faces the camera (from video games)", "", False),
    (TRICKS, "How do you make a 2D layer always face the camera?", "Layer > Transform > Auto-Orient > Orient Towards Camera", "",
     True),
    (TRICKS, "How do you make a layer point the way it's moving?", "Layer > Transform > Auto-Orient > Orient Along Path", "", False),
    (TRICKS, "How do you edit an effect point's motion path?", "Double-click the layer and edit the path in the Layer window", "",
     False),
    (TRICKS, "Which keying effect did the class use for green screen?", "Keylight 1.2 (Effect > Keying)", "", False),
    (TRICKS, "How do you check if a key is good in Keylight?", "View > Screen Matte",
     "White is seen, black isn't. Gray residue means semi-opaque pixels.", True),
    (TRICKS, "The screen matte has gray residue. How do you fix it?", "Raise Clip Black and lower Clip White until it's pure black and white", "",
     False),
    (TRICKS, "Best practice for compositing a keyed shot?",
     "Leave the footage alone, make a black-and-white matte from a duplicate, cut it in with a luma matte, and do it in its own comp",
     "Then you can color correct the bottom layer. Don't do multi-layer comping in one timeline.", False),
    (TRICKS, "How do you make Fractal Noise animate on its own?",
     "Option-click the Evolution stopwatch and type the expression time*200",
     "A higher number is faster; 75 was used for slow smoke.", False),
    (TRICKS, "What does E reveal?", "The layer's effects", "", False),
    (TRICKS, "F, and MM?", "F: Mask Feather.  MM: all mask properties", "", False),
    (TRICKS, "How do you make a mask perfectly centered on a layer?", "Double-click the shape tool (e.g. ellipse)", "", False),
    (TRICKS, "How do you build a vignette?", "Adjustment layer with an ellipse mask, inverted and feathered", "", False),
    (TRICKS, "What curve gives the \"action movie\" look?", "An S curve (Curves effect, on an adjustment layer)",
     "Lower the adjustment layer's opacity (T) to blend it in.", False),
    (TRICKS, "Which color tool is shared by Premiere and After Effects?", "Lumetri Color", "", False),
    (TRICKS, "What is the box in the middle of the Add Grain effect?", "The preview box (switch to Final Output to see it all)", "", False),
    (TRICKS, "How do you package a project with all of its files?", "File > Dependencies > Collect Files", "", False),
    (TRICKS, "Where do you set the default length for new stills and solids?", "Preferences (under the Edit menu on Windows)", "", False),

    # Output & compression
    (OUTPUT, "What are the four parts of knowing your output?", "Frame size, frame rate, compression and audio",
     "Settle these with the client up front.", True),
    (OUTPUT, "How do you send a comp to Media Encoder?", "File > Export > Add to Adobe Media Encoder Queue", "", False),
    (OUTPUT, "What's recommended while Media Encoder is rendering?", "Only have Media Encoder running (it's processor intensive)", "",
     False),
    (OUTPUT, "What lets Media Encoder pull a comp straight from the project?", "Dynamic Link", "", False),
    (OUTPUT, "Which ProRes do you need for an alpha channel?", "ProRes 4444",
     "ProRes 422 has no alpha.", False),
    (OUTPUT, "Progressive or interlaced?", "Progressive", "", False),
    (OUTPUT, "What standard HD color space was the default?", "Rec. 709", "Rec. 2100 is newer HDR; ACES is also common.", False),
    (OUTPUT, "Two types of compression?", "Lossy and lossless", "Lossless can hold the alpha channel.", False),
    (OUTPUT, "Spatial vs temporal compression?", "Spatial: within a single frame.  Temporal: over time, across frames", "",
     True),
    (OUTPUT, "What is CBR?", "Constant bit rate: every frame gets the same amount of data (e.g. 4,000k)", "", False),
    (OUTPUT, "What is VBR?", "Variable bit rate: data changes from frame to frame", "", False),
    (OUTPUT, "What is keyframe distance in compression?",
     "How often a full-quality frame appears (e.g. every 90 frames); frames in between are lower quality", "", False),
    (OUTPUT, "VBR 1 pass vs 2 pass?",
     "1 pass puts keyframes at a fixed interval. 2 pass also looks for changes (like cuts) and adds keyframes there",
     "2 pass gives better quality.", True),
    (OUTPUT, "What is a fast start header?", "A low-quality first frame that loads quickly so playback can start", "", False),
    (OUTPUT, "I-frame vs P-frame?", "I-frame: a whole image.  P-frame: only records the change from the last frame", "", False),
    (OUTPUT, "What is datamoshing?", "Glitch art where the motion of one clip is applied to another (by removing I-frames)",
     "aescripts sells Datamosh plugins.", False),
    (OUTPUT, "Name some Media Encoder effects you can add on export", "Tone mapping, image overlay, text overlay, timecode overlay", "",
     False),
    (OUTPUT, "Optical flow is an option for what?", "Frame resampling (time interpolation)", "Frame sampling is frame blending.", False),
    (OUTPUT, "Which output takes Media Encoder a really long time?", "Animated GIFs",
     "Faster: render frames and make the GIF in Photoshop.", False),
    (OUTPUT, "When you render an image sequence, what must you do?", "Render it into its own folder", "", False),
    (OUTPUT, "How do you record a Photoshop action?", "Actions panel > + (new action), name it, Record, do the steps, Stop", "",
     False),
    (OUTPUT, "How do you run an action on a whole folder of images?", "File > Automate > Batch",
     "Pick the action, source folder and destination folder.", False),
    (OUTPUT, "Batch keeps saving in the wrong place. Which option fixes it?", "Override Action \"Save As\" Commands",
     "Record a Save As inside the action.", False),
]

DECKS = [("1", SPACE, SPACE), ("2", CAMERAS, CAMERAS), ("3", LIGHTS, LIGHTS), ("4", TRICKS, TRICKS),
         ("5", OUTPUT, OUTPUT), ("6", "Everything", None), ("7", "Flagged in class", "missed")]

# --- Look ---

WIDTH, HEIGHT = 1000, 780
FPS = 60
CARD = pygame.Rect(150, 130, 700, 400)
FLIP_FRAMES = 14
RETRY_GAP = 3  # a missed card comes back after this many other cards

BG = (28, 31, 48)
CARD_FRONT = (250, 248, 240)
CARD_BACK = (255, 236, 190)
INK = (35, 35, 45)
SOFT_INK = (110, 105, 95)
ACCENT = (0, 170, 220)  # 3D blue
GOOD = (70, 180, 110)
BAD = (225, 85, 85)
STAR = (240, 170, 30)
WHITE = (240, 240, 250)
DIM = (150, 155, 180)


def wrap(text, font, width):
    """Lines of text that fit in `width` pixels. Keeps the line breaks already in the text."""
    lines = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split(" "):
            test = (line + " " + word).strip()
            if font.size(test)[0] <= width or not line:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_text_block(screen, text, fonts, color, rect):
    """Centered, wrapped text, using the biggest of `fonts` that fits inside `rect`."""
    for font in fonts:
        lines = wrap(text, font, rect.width)
        height = len(lines) * font.get_linesize()
        if height <= rect.height:
            break
    y = rect.centery - height // 2
    for line in lines:
        surface = font.render(line, True, color)
        screen.blit(surface, surface.get_rect(midtop=(rect.centerx, y)))
        y += font.get_linesize()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("3D QUIZ")
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.SysFont("Helvetica", 46, bold=True)
        self.big_fonts = [pygame.font.SysFont("Helvetica", s, bold=True) for s in (52, 42, 34, 28, 24)]
        self.font = pygame.font.SysFont("Helvetica", 26)
        self.small = pygame.font.SysFont("Helvetica", 20)
        self.state = "menu"

    # --- Decks and rounds ---

    def start(self, cards, label):
        # Cards flagged in class come first, then the rest shuffled
        missed = [c for c in cards if c[4]]
        rest = [c for c in cards if not c[4]]
        random.shuffle(missed)
        random.shuffle(rest)
        self.queue = missed + rest
        self.label = label
        self.total = len(cards)
        self.done = 0
        self.first_try = 0
        self.seen_wrong = []  # cards missed at least once this round, in order
        self.streak = self.best_streak = 0
        self.next_card()
        self.state = "play"

    def next_card(self):
        if not self.queue:
            self.state = "results"
            return
        self.card = self.queue.pop(0)
        self.showing_back = False
        self.flip = 0  # frames left in the flip animation
        self.feedback = None

    def answer(self, knew_it):
        if knew_it:
            self.done += 1
            self.streak += 1
            self.best_streak = max(self.best_streak, self.streak)
            if self.card not in self.seen_wrong:
                self.first_try += 1
            self.feedback = ("Got it!", GOOD)
        else:
            self.streak = 0
            if self.card not in self.seen_wrong:
                self.seen_wrong.append(self.card)
            self.queue.insert(min(RETRY_GAP, len(self.queue)), self.card)
            self.feedback = ("It'll come back", BAD)
        self.feedback_timer = 25

    # --- Main loop ---

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT and not WEB:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == "menu":
                        if not WEB:  # a browser tab can't be quit; Esc just stays on the menu
                            return
                        continue
                    self.state = "menu"
                    continue
                if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.state != "menu"
                        and self.menu_button().collidepoint(event.pos)):
                    self.state = "menu"
                    continue
                getattr(self, "on_" + self.state)(event)
            getattr(self, "draw_" + self.state)()
            pygame.display.flip()
            self.clock.tick(FPS)
            await asyncio.sleep(0)  # lets the browser draw the frame

    def menu_button(self):
        return pygame.Rect(WIDTH // 2 - 90, HEIGHT - 44, 180, 36)

    def draw_menu_button(self):
        box = self.menu_button()
        pygame.draw.rect(self.screen, (45, 50, 75), box, border_radius=10)
        label = self.small.render("Menu  (Esc)", True, DIM)
        self.screen.blit(label, label.get_rect(center=box.center))

    # --- Menu ---

    def deck_box(self, i):
        return pygame.Rect(220, 170 + i * 80, 560, 66)

    def on_menu(self, event):
        for i, (key, label, deck) in enumerate(DECKS):
            pressed = event.type == pygame.KEYDOWN and event.unicode == key
            clicked = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                       and self.deck_box(i).collidepoint(event.pos))
            if pressed or clicked:
                if deck == "missed":
                    cards = [c for c in CARDS if c[4]]
                elif deck is None:
                    cards = list(CARDS)
                else:
                    cards = [c for c in CARDS if c[0] == deck]
                self.start(cards, label)
                return

    def draw_menu(self):
        self.screen.fill(BG)
        title = self.title_font.render("3D QUIZ", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        sub = self.small.render("Study for the quiz. Click a deck or press its number:", True, DIM)
        self.screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 130)))
        for i, (key, label, deck) in enumerate(DECKS):
            if deck == "missed":
                count = sum(1 for c in CARDS if c[4])
            elif deck is None:
                count = len(CARDS)
            else:
                count = sum(1 for c in CARDS if c[0] == deck)
            box = self.deck_box(i)
            pygame.draw.rect(self.screen, (45, 50, 75), box, border_radius=14)
            pygame.draw.rect(self.screen, ACCENT, (box.x, box.y, 66, 66), border_radius=14)
            number = self.big_fonts[2].render(key, True, WHITE)
            self.screen.blit(number, number.get_rect(center=(box.x + 33, box.centery)))
            text = self.font.render(label, True, WHITE)
            self.screen.blit(text, (box.x + 90, box.y + 10))
            cards = self.small.render(f"{count} cards", True, DIM)
            self.screen.blit(cards, (box.x + 90, box.y + 40))
        tip = self.small.render("Starred cards were flagged in class as quiz material." + ("" if WEB else "  Esc quits."),
                                True, DIM)
        self.screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT - 40)))

    # --- Playing ---

    def on_play(self, event):
        flip_now = (event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN)) or \
                   (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and CARD.collidepoint(event.pos))
        if flip_now and self.flip == 0:
            self.flip = FLIP_FRAMES
            return
        if self.showing_back and self.flip == 0 and self.feedback is None:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RIGHT, pygame.K_y):
                    self.answer(True)
                elif event.key in (pygame.K_LEFT, pygame.K_n):
                    self.answer(False)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.choice_box(WIDTH // 2 + 170).collidepoint(event.pos):
                    self.answer(True)
                elif self.choice_box(WIDTH // 2 - 170).collidepoint(event.pos):
                    self.answer(False)

    def draw_play(self):
        self.screen.fill(BG)
        deck, front, back, note, missed = self.card

        # Top: deck name, progress bar, streak
        header = self.small.render(f"{self.label}   ·   {self.done} of {self.total} learned", True, DIM)
        self.screen.blit(header, (CARD.x, 40))
        streak = self.small.render(f"Streak {self.streak}   Best {self.best_streak}", True, DIM)
        self.screen.blit(streak, streak.get_rect(topright=(CARD.right, 40)))
        bar = pygame.Rect(CARD.x, 75, CARD.width, 12)
        pygame.draw.rect(self.screen, (55, 60, 85), bar, border_radius=6)
        if self.total:
            pygame.draw.rect(self.screen, ACCENT, (bar.x, bar.y, bar.width * self.done // self.total, bar.height),
                             border_radius=6)

        # The card, squeezed sideways while it flips
        if self.flip:
            self.flip -= 1
            if self.flip == FLIP_FRAMES // 2:
                self.showing_back = not self.showing_back
        squeeze = abs(self.flip - FLIP_FRAMES / 2) / (FLIP_FRAMES / 2) if self.flip else 1
        rect = CARD.inflate(-CARD.width * (1 - squeeze), 0)
        shadow = rect.move(6, 8)
        pygame.draw.rect(self.screen, (15, 17, 28), shadow, border_radius=22)
        pygame.draw.rect(self.screen, CARD_BACK if self.showing_back else CARD_FRONT, rect, border_radius=22)

        if squeeze > 0.95:
            corner = self.small.render("ANSWER" if self.showing_back else deck.upper(), True, SOFT_INK)
            self.screen.blit(corner, (rect.x + 24, rect.y + 20))
            if missed:
                star = self.small.render("* flagged in class", True, STAR)
                self.screen.blit(star, star.get_rect(topright=(rect.right - 24, rect.y + 20)))
            if self.showing_back:
                area = pygame.Rect(rect.x + 50, rect.y + 60, rect.width - 100, rect.height - (170 if note else 110))
                draw_text_block(self.screen, back, self.big_fonts, INK, area)
                if note:
                    draw_text_block(self.screen, note, [self.small], SOFT_INK,
                                    pygame.Rect(rect.x + 50, rect.bottom - 100, rect.width - 100, 70))
            else:
                area = pygame.Rect(rect.x + 50, rect.y + 60, rect.width - 100, rect.height - 110)
                draw_text_block(self.screen, front, self.big_fonts[1:], INK, area)

        # Bottom: what to press, or how the last answer went
        if self.feedback:
            text, color = self.feedback
            label = self.big_fonts[3].render(text, True, color)
            self.screen.blit(label, label.get_rect(center=(WIDTH // 2, CARD.bottom + 70)))
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                self.next_card()
        elif self.showing_back and not self.flip:
            self.draw_choice("<  N   Study again", BAD, WIDTH // 2 - 170)
            self.draw_choice("Knew it   Y  >", GOOD, WIDTH // 2 + 170)
        else:
            hint = self.font.render("Click the card or press Space to flip", True, DIM)
            self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, CARD.bottom + 70)))
        self.draw_menu_button()

    def choice_box(self, center_x):
        box = pygame.Rect(0, 0, 290, 56)
        box.center = (center_x, CARD.bottom + 70)
        return box

    def draw_choice(self, text, color, center_x):
        box = self.choice_box(center_x)
        pygame.draw.rect(self.screen, color, box, border_radius=14)
        label = self.font.render(text, True, WHITE)
        self.screen.blit(label, label.get_rect(center=box.center))

    # --- Results ---

    def retry_button(self):
        return pygame.Rect(WIDTH // 2 - 200, HEIGHT - 110, 400, 50)

    def on_results(self, event):
        retry = (event.type == pygame.KEYDOWN and event.key == pygame.K_r) or \
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.retry_button().collidepoint(event.pos))
        if retry and self.seen_wrong:
            self.start(list(self.seen_wrong), "Missed this round")
        elif event.type == pygame.KEYDOWN and event.key in (pygame.K_m, pygame.K_RETURN, pygame.K_SPACE):
            self.state = "menu"

    def draw_results(self):
        self.screen.fill(BG)
        title = self.title_font.render("Deck done!", True, WHITE)
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 80)))
        score = self.font.render(f"{self.first_try} of {self.total} right on the first try   ·   best streak {self.best_streak}",
                                 True, WHITE)
        self.screen.blit(score, score.get_rect(center=(WIDTH // 2, 140)))
        if self.seen_wrong:
            head = self.small.render("Worth another look:", True, DIM)
            self.screen.blit(head, (150, 190))
            y = 222
            for card in self.seen_wrong[:9]:
                line = wrap(f"{card[1]}  -  {card[2]}".replace("\n", "  "), self.small, 700)[0]
                self.screen.blit(self.small.render("• " + line, True, WHITE), (150, y))
                y += 32
            if len(self.seen_wrong) > 9:
                self.screen.blit(self.small.render(f"...and {len(self.seen_wrong) - 9} more", True, DIM), (150, y))
            box = self.retry_button()
            pygame.draw.rect(self.screen, ACCENT, box, border_radius=14)
            label = self.font.render("Go over the missed ones again  (R)", True, WHITE)
            self.screen.blit(label, label.get_rect(center=box.center))
        else:
            perfect = self.big_fonts[2].render("Perfect round. You're ready!", True, GOOD)
            self.screen.blit(perfect, perfect.get_rect(center=(WIDTH // 2, 300)))
        self.draw_menu_button()


async def main():
    await Game().run()
    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main())
