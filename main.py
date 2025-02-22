import pygame
import math
import sys
import pygame.gfxdraw
from collections import defaultdict
from gu_data import objects  # Import the Gu database

# Override radius values based on desired distances:
distance_mapping = {4: 100, 3: 220, 2: 340, 1: 460}
for obj in objects.values():
    level = obj.get("level", 1)
    obj["radius"] = distance_mapping.get(level, obj.get("radius", 0))

# Helper function: convert hex color to RGB tuple.
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Initialize Pygame and font module.
pygame.init()
pygame.font.init()

# -------------------------------
# DISPLAY SETTINGS (Enhanced Resolution & Colors)
# -------------------------------
display_width = 1280    # Increased width for higher resolution
display_height = 720    # Increased height for higher resolution
screen = pygame.display.set_mode((display_width, display_height))
center_x = display_width // 2
center_y = display_height // 2

# Define Colors.
BG_COLOR = (30, 30, 30)           # A muted dark gray background
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_COLOR = (50, 50, 50)
TEXT_COLOR = (240, 240, 240)
FRAME_COLOR = (190, 190, 190)
display_width = 1280   # or your chosen width
display_height = 720   # or your chosen height

FUSION_LINE_MODE = False  # Track if we're in fusion line view
DOUBLE_CLICK_TIME = 300   # Maximum time between clicks for double click (in milliseconds)
VERTICAL_SPACING = 150    # Vertical space between Gu levels in fusion line view
HORIZONTAL_SPACING = 200  # Horizontal space between Gu in the same level

def get_fusion_line_elements(objects, selected_gu):
    """
    Get all Gu related to the selected one in the fusion hierarchy.
    Returns a dict with levels (negative for ingredients, positive for products).
    """
    elements = defaultdict(list)
    elements[0] = [selected_gu]  # Center level

    # Get ingredients (upward)
    def add_ingredients(gu_name, level):
        if gu_name in objects:
            recipe = objects[gu_name].get("recipe", [])
            ingredients = [ing for ing in recipe if ing != "???" and ing in objects]
            if ingredients:
                elements[level].extend(ingredients)
                for ing in ingredients:
                    add_ingredients(ing, level - 1)

    # Get products (downward)
    def add_products(gu_name, level):
        products = []
        for name, data in objects.items():
            if gu_name in data.get("recipe", []):
                products.append(name)
        if products:
            elements[level].extend(products)
            for prod in products:
                add_products(prod, level + 1)

    add_ingredients(selected_gu, -1)
    add_products(selected_gu, 1)
    return elements

def calculate_fusion_line_positions(elements, center_x, center_y):
    """
    Calculate positions for Gu in fusion view.
    This version groups duplicate Gu (so if an ingredient is used in multiple fusions,
    it appears only once) and uses a reduced horizontal spacing so that items are
    positioned closer to the selected Gu.
    """
    positions = {}
    for level, gu_list in elements.items():
        if not gu_list:
            continue

        # Remove duplicates while preserving order.
        unique_gu = []
        for gu in gu_list:
            if gu not in unique_gu:
                unique_gu.append(gu)
        
        n = len(unique_gu)
        # Vertical position remains based on level:
        y = center_y + (level * VERTICAL_SPACING)
        
        # If only one unique Gu, center it.
        if n == 1:
            positions[unique_gu[0]] = (center_x, y)
        else:
            # Use a reduced horizontal spacing in fusion view.
            effective_spacing = HORIZONTAL_SPACING * 0.8  # 80% of normal spacing
            total_width = (n - 1) * effective_spacing
            start_x = center_x - (total_width / 2)
            for i, gu in enumerate(unique_gu):
                x = start_x + i * effective_spacing
                positions[gu] = (x, y)
    return positions

# -------------------------------
# BOX DRAWING AND RECTANGLE CALCULATION
# -------------------------------
def draw_square(screen, x, y, color, name, scale):
    """
    Draw a box (Gu) with the given color and name at (x,y) and return its rectangle.
    The box is drawn with slightly rounded corners.
    """
    padding = 5 * scale
    font_size = max(int(24 * scale), 12)
    font = pygame.font.Font(None, font_size)
    lines = name.split()
    max_line_width = 0
    total_text_height = 0
    for line in lines:
        line_width, line_height = font.size(line)
        max_line_width = max(max_line_width, line_width)
        total_text_height += line_height

    box_width = max(60 * scale, max_line_width + 2 * padding)
    box_height = total_text_height + 2 * padding

    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (x, y)
    # Draw rectangle with rounded corners.
    pygame.draw.rect(screen, color, box_rect, border_radius=int(10 * scale))

    current_y = box_rect.top + padding
    for line in lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(centerx=box_rect.centerx, top=current_y)
        screen.blit(text_surface, text_rect)
        current_y += font.get_height()

    return box_rect  # Return the rectangle for collision detection

def calculate_box_rect(x, y, name, scale):
    """
    Calculate and return the rectangle for a Gu box (using the same geometry as draw_square)
    without drawing it. This is used for arrow positioning.
    """
    padding = 5 * scale
    font_size = max(int(24 * scale), 12)
    font = pygame.font.Font(None, font_size)
    lines = name.split()
    max_line_width = 0
    total_text_height = 0
    for line in lines:
        line_width, line_height = font.size(line)
        max_line_width = max(max_line_width, line_width)
        total_text_height += line_height

    box_width = max(60 * scale, max_line_width + 2 * padding)
    box_height = total_text_height + 2 * padding

    box_rect = pygame.Rect(0, 0, box_width, box_height)
    box_rect.center = (x, y)
    return box_rect

# -------------------------------
# POSITION CALCULATION
# -------------------------------
def calculate_positions(objects):
    # First, group objects by level
    grouped_objects = {}
    for name, data in objects.items():
        level = data.get("level", 1)
        grouped_objects.setdefault(level, []).append(name)

    # Build relationship graph
    relationships = {}
    for name, data in objects.items():
        relationships[name] = set()
        # Add recipe relationships
        for ingredient in data.get("recipe", []):
            if ingredient != "???" and ingredient in objects:
                relationships[name].add(ingredient)
                relationships.setdefault(ingredient, set()).add(name)
        # Add fusion relationships
        for fusion in data.get("fusions", []):
            if fusion in objects:
                relationships[name].add(fusion)
                relationships.setdefault(fusion, set()).add(name)

    object_positions = {}

    # Process each level
    for level, names in sorted(grouped_objects.items(), reverse=True):
        radius = objects[names[0]].get("radius", 0)
        count = len(names)

        if count == 1:
            # Single object at this level - place at top
            x = center_x
            y = center_y - radius
            object_positions[names[0]] = (x, y)
        else:
            # Sort objects based on their relationships
            def get_relationship_score(name):
                score = 0
                related = relationships.get(name, set())
                for rel in related:
                    if rel in object_positions:  # If related object is already placed
                        score += 1
                return score

            # Sort names by relationship score
            sorted_names = sorted(names, key=get_relationship_score, reverse=True)

            # Calculate positions around the circle
            angle_step = 360 / count
            best_start_angle = -90  # Default start from top

            # Try different starting angles to find best arrangement
            if count > 2:
                min_distance = 0
                for test_angle in range(-90, 270, 45):
                    total_distance = 0
                    test_positions = {}
                    # Calculate test positions
                    for i, name in enumerate(sorted_names):
                        angle = test_angle + i * angle_step
                        angle_rad = math.radians(angle)
                        x = center_x + radius * math.cos(angle_rad)
                        y = center_y + radius * math.sin(angle_rad)
                        test_positions[name] = (x, y)
                    # Calculate total distance to related objects
                    for name, pos in test_positions.items():
                        for related in relationships.get(name, set()):
                            if related in object_positions:
                                rel_pos = object_positions[related]
                                dist = math.hypot(pos[0] - rel_pos[0], pos[1] - rel_pos[1])
                                total_distance += dist
                    # Update best angle if this arrangement is better
                    if min_distance == 0 or total_distance < min_distance:
                        min_distance = total_distance
                        best_start_angle = test_angle

            # Place objects using best starting angle
            for i, name in enumerate(sorted_names):
                angle = best_start_angle + i * angle_step
                angle_rad = math.radians(angle)
                x = center_x + radius * math.cos(angle_rad)
                y = center_y + radius * math.sin(angle_rad)
                object_positions[name] = (x, y)

    return object_positions

# -------------------------------
# ARROW CALCULATION AND DRAWING
# -------------------------------
def calculate_arrow_points(start_x, start_y, end_x, end_y, box_width, box_height):
    """
    Calculate points for drawing an arrow from one Gu to another so that
    the arrow tip touches the target box edge.
    """
    # Calculate the angle between start and end points.
    angle = math.atan2(end_y - start_y, end_x - start_x)

    # Compute half-dimensions of the target box.
    half_width = box_width / 2
    half_height = box_height / 2

    # Determine the intersection with the box edge.
    if abs(math.cos(angle)) * half_height > abs(math.sin(angle)) * half_width:
        # Intersects with left/right edge.
        if end_x > start_x:
            actual_end_x = end_x - half_width
        else:
            actual_end_x = end_x + half_width
        actual_end_y = start_y + (actual_end_x - start_x) * math.tan(angle)
    else:
        # Intersects with top/bottom edge.
        if end_y > start_y:
            actual_end_y = end_y - half_height
        else:
            actual_end_y = end_y + half_height
        actual_end_x = start_x + (actual_end_y - start_y) / math.tan(angle) if math.tan(angle) != 0 else end_x

    # Arrow head parameters.
    arrow_size = 15
    arrow_angle = math.pi / 6  # 30 degrees.

    # Calculate arrow head points.
    point1_x = actual_end_x - arrow_size * math.cos(angle - arrow_angle)
    point1_y = actual_end_y - arrow_size * math.sin(angle - arrow_angle)
    point2_x = actual_end_x - arrow_size * math.cos(angle + arrow_angle)
    point2_y = actual_end_y - arrow_size * math.sin(angle + arrow_angle)

    return (start_x, start_y), (actual_end_x, actual_end_y), (point1_x, point1_y), (point2_x, point2_y)

def draw_arrows(screen, objects, object_positions, camera_offset_x, camera_offset_y, scale, gu_boxes):
    """
    Draw arrows between related Gu objects so that the arrow tip meets the target
    box at its edge.
    """
    ARROW_COLOR = (240, 240, 240)  # Brighter (near-white) color for clarity.
    ARROW_WIDTH = max(1, int(2 * scale))
    
    # For each fusion relationship (using the "recipe" key):
    for source_name, source_data in objects.items():
        if "recipe" in source_data and source_data["recipe"]:
            for ingredient in source_data["recipe"]:
                if ingredient in object_positions and source_name in object_positions:
                    # Ingredient: start point.
                    start_pos = object_positions[ingredient]
                    start_x = center_x + (start_pos[0] - center_x) * scale + camera_offset_x
                    start_y = center_y + (start_pos[1] - center_y) * scale + camera_offset_y

                    # Result: end point.
                    end_pos = object_positions[source_name]
                    end_x = center_x + (end_pos[0] - center_x) * scale + camera_offset_x
                    end_y = center_y + (end_pos[1] - center_y) * scale + camera_offset_y

                    # Get the target box dimensions from gu_boxes.
                    target_box = gu_boxes.get(source_name)
                    if target_box:
                        box_width = target_box.width
                        box_height = target_box.height
                        start, end, point1, point2 = calculate_arrow_points(
                            start_x, start_y, end_x, end_y, box_width, box_height
                        )
                        # Use anti-aliased line if ARROW_WIDTH is 1, otherwise use normal line.
                        if ARROW_WIDTH == 1:
                            pygame.draw.aaline(screen, ARROW_COLOR, (int(start[0]), int(start[1])), (int(end[0]), int(end[1])))
                        else:
                            pygame.draw.line(screen, ARROW_COLOR, start, end, ARROW_WIDTH)
                        pygame.draw.polygon(screen, ARROW_COLOR, [end, point1, point2])

# -------------------------------
# INFO WINDOW DRAWING
# -------------------------------
def draw_info_window(screen, gu_box_rect, gu_name, scale):
    """
    Draws an info window for the selected Gu that displays:
      - The Gu's name (header), wrapped if too long.
      - The Gu's level.
      - The Gu's effect.
      - Its recipe (if any).
      - Its fusions (if any).

    The entire info window (dimensions and text) is scaled 20% larger than before.
    """
    # --- Info window fixed scaling factor: 20% larger
    info_scale_factor = 1.2

    # --- Fixed parameters for the info window (independent of global zoom) ---
    info_window_width = int(300 * info_scale_factor)      # New width: 300 * 1.2 = 360 px
    base_padding = int(20 * info_scale_factor)            # New padding: 20 * 1.2 = 24 px
    spacing_between_sections = int(10 * info_scale_factor)  # New spacing: 10 * 1.2 = 12 px

    # --- Fixed font sizes for the info window (so they remain readable) ---
    header_font_size = int(28 * info_scale_factor)  # New header font size: 28 * 1.2 ≈ 34
    content_font_size = int(20 * info_scale_factor)  # New content font size: 20 * 1.2 = 24

    header_font = pygame.font.Font(None, header_font_size)
    content_font = pygame.font.Font(None, content_font_size)

    max_text_width = info_window_width - 2 * base_padding

    # --- Helper function for wrapping text ---
    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = word if current_line == "" else current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    # --- Retrieve the Gu's data from objects ---
    gu_data = objects.get(gu_name, {})
    level_text = "Level: " + str(gu_data.get("level", "N/A"))
    effect_text = gu_data.get("effect", "No effect")
    recipe_list = gu_data.get("recipe", [])
    fusions_list = gu_data.get("fusions", [])

    # --- Wrap text for each section ---
    header_lines = wrap_text(gu_name, header_font, max_text_width)
    level_lines = wrap_text(level_text, content_font, max_text_width)
    effect_lines = wrap_text(effect_text, content_font, max_text_width)
    recipe_lines = wrap_text("Recipe: " + ", ".join(recipe_list), content_font, max_text_width) if recipe_list else []
    fusions_lines = wrap_text("Fusions: " + ", ".join(fusions_list), content_font, max_text_width) if fusions_list else []

    # --- Compute total content height ---
    header_height = len(header_lines) * header_font.get_linesize()
    level_height = len(level_lines) * content_font.get_linesize()
    effect_height = len(effect_lines) * content_font.get_linesize()
    recipe_height = len(recipe_lines) * content_font.get_linesize()
    fusions_height = len(fusions_lines) * content_font.get_linesize()

    # Count how many sections will be rendered
    sections = []
    if header_lines: sections.append(header_height)
    if level_lines: sections.append(level_height)
    if effect_lines: sections.append(effect_height)
    if recipe_lines: sections.append(recipe_height)
    if fusions_lines: sections.append(fusions_height)
    total_spacing = spacing_between_sections * (len(sections) - 1 if len(sections) > 1 else 0)

    content_height = header_height + level_height + effect_height + recipe_height + fusions_height + total_spacing

    # --- Compute window height ---
    info_window_height = content_height + 2 * base_padding

    # --- Position the window relative to the Gu box ---
    window_x = gu_box_rect.right + base_padding
    window_y = gu_box_rect.centery - info_window_height // 2

    # If the window goes off the right edge, place it to the left of the box.
    if window_x + info_window_width > display_width:
        window_x = gu_box_rect.left - info_window_width - base_padding
    # Keep the window fully on-screen vertically.
    window_y = max(0, min(display_height - info_window_height, window_y))

    window_rect = pygame.Rect(window_x, window_y, info_window_width, info_window_height)

    # --- Draw the window with rounded corners and a frame ---
    pygame.draw.rect(screen, WINDOW_COLOR, window_rect, border_radius=10)
    pygame.draw.rect(screen, FRAME_COLOR, window_rect, 2, border_radius=10)

    # --- Render the text ---
    current_y = window_rect.top + base_padding

    # Render header (possibly multiple lines)
    for line in header_lines:
        line_surface = header_font.render(line, True, TEXT_COLOR)
        line_rect = line_surface.get_rect(centerx=window_rect.centerx, top=current_y)
        screen.blit(line_surface, line_rect)
        current_y += header_font.get_linesize()
    if header_lines:
        current_y += spacing_between_sections

    # Render level
    for line in level_lines:
        line_surface = content_font.render(line, True, TEXT_COLOR)
        line_rect = line_surface.get_rect(centerx=window_rect.centerx, top=current_y)
        screen.blit(line_surface, line_rect)
        current_y += content_font.get_linesize()
    if level_lines:
        current_y += spacing_between_sections

    # Render effect
    for line in effect_lines:
        line_surface = content_font.render(line, True, TEXT_COLOR)
        line_rect = line_surface.get_rect(centerx=window_rect.centerx, top=current_y)
        screen.blit(line_surface, line_rect)
        current_y += content_font.get_linesize()
    if effect_lines:
        current_y += spacing_between_sections

    # Render recipe if available
    if recipe_lines:
        for line in recipe_lines:
            line_surface = content_font.render(line, True, TEXT_COLOR)
            line_rect = line_surface.get_rect(centerx=window_rect.centerx, top=current_y)
            screen.blit(line_surface, line_rect)
            current_y += content_font.get_linesize()
        current_y += spacing_between_sections

    # Render fusions if available
    if fusions_lines:
        for line in fusions_lines:
            line_surface = content_font.render(line, True, TEXT_COLOR)
            line_rect = line_surface.get_rect(centerx=window_rect.centerx, top=current_y)
            screen.blit(line_surface, line_rect)
            current_y += content_font.get_linesize()

    return window_rect

# -------------------------------
# MAIN GAME LOOP
# -------------------------------
def main():
    try:
        running = True
        clock = pygame.time.Clock()

        # Camera and interaction states.
        camera_offset_x = 0
        camera_offset_y = 0
        dragging = False
        drag_start = (0, 0)
        offset_start = (0, 0)

        # Zoom state.
        scale = 1.0
        min_scale = 0.5
        max_scale = 2.0

        # Selection and window states.
        selected_gu = None
        show_info_window = False
        info_window_rect = None
        drag_threshold = 5
        click_candidate = False

        # Animation states for smooth camera movement.
        target_offset_x = 0
        target_offset_y = 0
        camera_moving = False
        animation_speed = 0.1

        # Variables to track double clicks.
        last_click_time = 0
        last_clicked_gu = None

        # Track fusion line view state.
        global FUSION_LINE_MODE
        selected_fusion_gu = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and FUSION_LINE_MODE:
                        FUSION_LINE_MODE = False
                        selected_fusion_gu = None

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click.
                        dragging = True
                        drag_start = event.pos
                        offset_start = (camera_offset_x, camera_offset_y)
                        click_candidate = True

                        current_time = pygame.time.get_ticks()
                        mouse_pos = event.pos
                        clicked_gu = None

                        if FUSION_LINE_MODE and selected_fusion_gu:
                            positions_for_click = calculate_fusion_line_positions(
                                get_fusion_line_elements(objects, selected_fusion_gu),
                                center_x, center_y
                            )
                        else:
                            positions_for_click = calculate_positions(objects)

                        for name, pos in positions_for_click.items():
                            transformed_x = center_x + (pos[0] - center_x) * scale + camera_offset_x
                            transformed_y = center_y + (pos[1] - center_y) * scale + camera_offset_y
                            distance = math.hypot(mouse_pos[0] - transformed_x, mouse_pos[1] - transformed_y)
                            if distance < 30 * scale:
                                clicked_gu = name
                                break

                        if (clicked_gu and clicked_gu == last_clicked_gu and 
                            current_time - last_click_time < DOUBLE_CLICK_TIME):
                            FUSION_LINE_MODE = True
                            selected_fusion_gu = clicked_gu
                            camera_offset_x = 0
                            camera_offset_y = 0
                            show_info_window = False

                        last_click_time = current_time
                        last_clicked_gu = clicked_gu

                    elif event.button == 3:  # Right click.
                        mouse_pos = event.pos
                        if FUSION_LINE_MODE and selected_fusion_gu:
                            positions_for_click = calculate_fusion_line_positions(
                                get_fusion_line_elements(objects, selected_fusion_gu),
                                center_x, center_y
                            )
                        else:
                            positions_for_click = calculate_positions(objects)
                        for name, pos in positions_for_click.items():
                            transformed_x = center_x + (pos[0] - center_x) * scale + camera_offset_x
                            transformed_y = center_y + (pos[1] - center_y) * scale + camera_offset_y
                            distance = math.hypot(mouse_pos[0] - transformed_x, mouse_pos[1] - transformed_y)
                            if distance < 30 * scale:
                                selected_gu = name
                                target_offset_x = -(pos[0] - center_x) * scale
                                target_offset_y = -(pos[1] - center_y) * scale
                                camera_moving = True
                                show_info_window = True
                                break

                    elif event.button in (4, 5):  # Scroll.
                        scale = min(max(scale + (0.1 if event.button == 4 else -0.1), min_scale), max_scale)

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click release.
                        dragging = False
                        if click_candidate:
                            mouse_pos = event.pos
                            if FUSION_LINE_MODE and selected_fusion_gu:
                                positions_for_click = calculate_fusion_line_positions(
                                    get_fusion_line_elements(objects, selected_fusion_gu),
                                    center_x, center_y
                                )
                            else:
                                positions_for_click = calculate_positions(objects)
                            for name, pos in positions_for_click.items():
                                transformed_x = center_x + (pos[0] - center_x) * scale + camera_offset_x
                                transformed_y = center_y + (pos[1] - center_y) * scale + camera_offset_y
                                distance = math.hypot(mouse_pos[0] - transformed_x, mouse_pos[1] - transformed_y)
                                if distance < 30 * scale:
                                    selected_gu = name
                                    show_info_window = False
                                    target_offset_x = -(pos[0] - center_x) * scale
                                    target_offset_y = -(pos[1] - center_y) * scale
                                    camera_moving = True
                                    break
                        click_candidate = False

                elif event.type == pygame.MOUSEMOTION and dragging:
                    dx = event.pos[0] - drag_start[0]
                    dy = event.pos[1] - drag_start[1]
                    if math.hypot(dx, dy) > drag_threshold:
                        click_candidate = False
                    camera_offset_x = offset_start[0] + dx
                    camera_offset_y = offset_start[1] + dy
                    camera_moving = False

            if camera_moving:
                dx = target_offset_x - camera_offset_x
                dy = target_offset_y - camera_offset_y
                if abs(dx) < 0.5 and abs(dy) < 0.5:
                    camera_offset_x = target_offset_x
                    camera_offset_y = target_offset_y
                    camera_moving = False
                else:
                    camera_offset_x += dx * animation_speed
                    camera_offset_y += dy * animation_speed

            screen.fill(BG_COLOR)

            if FUSION_LINE_MODE and selected_fusion_gu:
                elements = get_fusion_line_elements(objects, selected_fusion_gu)
                object_positions = calculate_fusion_line_positions(elements, center_x, center_y)
            else:
                object_positions = calculate_positions(objects)

            gu_boxes = {}
            for name, pos in object_positions.items():
                transformed_x = center_x + (pos[0] - center_x) * scale + camera_offset_x
                transformed_y = center_y + (pos[1] - center_y) * scale + camera_offset_y
                box_rect = calculate_box_rect(transformed_x, transformed_y, name, scale)
                gu_boxes[name] = box_rect

            draw_arrows(screen, objects, object_positions, camera_offset_x, camera_offset_y, scale, gu_boxes)

            for name, pos in object_positions.items():
                transformed_x = center_x + (pos[0] - center_x) * scale + camera_offset_x
                transformed_y = center_y + (pos[1] - center_y) * scale + camera_offset_y
                gu_color_hex = objects[name].get("color", "#FFFFFF")
                gu_color_rgb = hex_to_rgb(gu_color_hex)
                box_rect = draw_square(screen, transformed_x, transformed_y, gu_color_rgb, name, scale)
                gu_boxes[name] = box_rect

            if show_info_window and selected_gu and not camera_moving:
                selected_box_rect = gu_boxes.get(selected_gu)
                if selected_box_rect:
                    info_window_rect = draw_info_window(screen, selected_box_rect, selected_gu, scale)

            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()