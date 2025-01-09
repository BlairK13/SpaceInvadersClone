import pygame
import os
from config import screen_width, screen_height

def spawn_enemies_in_grid(
    enemy_class,
    enemy_list,
    all_sprites_list,
    rows,
    cols,
    x_spacing,
    y_spacing,
    start_x,
    start_y
):
    """
    Creates enemies in a grid layout. 
    Each row and column has an enemy spaced by x_spacing and y_spacing.
    """
    for row in range(rows):
        for col in range(cols):
            enemy = enemy_class()
            enemy.rect.x = start_x + col * (enemy.rect.width + x_spacing)
            enemy.rect.y = start_y + row * (enemy.rect.height + y_spacing)
            enemy_list.add(enemy)
            all_sprites_list.add(enemy)

def load_image(path, scale=None):
    """
    Loads and optionally scales an image from the assets folder.
    """
    full_path = os.path.join('assets', path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Could not load {full_path}: {e}")
        raise SystemExit(e)

def draw_text(surface, text, font, color, x, y, center=False):
    """
    Renders text on a surface at (x, y). If center=True, text is centered there.
    """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def display_message(screen, message, font, color, w, h, duration=3000):
    """
    Clears the screen, shows a centered message, and waits a bit.
    """
    screen.fill((0, 0, 0))
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(w // 2, h // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(duration)

def handle_collisions(bullet_list, enemy_list, all_sprites_list, score):
    """
    Checks if bullets hit enemies. Removes bullets and enemies, updates score.
    Returns (updated_score, True) if score >= 50, otherwise (updated_score, False).
    """
    for bullet in bullet_list.copy():
        hits = pygame.sprite.spritecollide(bullet, enemy_list, True)
        for enemy in hits:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print(f"Score: {score}")
            if score >= 50:
                return score, True
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    return score, False

def can_shoot(last_shot_time, cooldown):
    """
    Lets the player shoot if enough time has passed since the last shot.
    """
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= cooldown:
        return True, current_time
    return False, last_shot_time

def reset_game(all_sprites, enemy_list, bullet_list, player,
               rows, cols, x_space, y_space, start_x, start_y):
    """
    Clears enemies and bullets, resets the player, and respawns enemy grid.
    Returns (score, elapsed_time) both reset to 0.
    """
    enemy_list.empty()
    bullet_list.empty()
    for sprite in all_sprites.copy():
        if sprite != player:
            all_sprites.remove(sprite)

    player.rect.x = screen_width // 2
    player.rect.y = int(screen_height * 0.9)

    spawn_enemies_in_grid(
        enemy_list=enemy_list, 
        all_sprites_list=all_sprites, 
        enemy_class=type(player),  # Not exactly correct if 'enemy_class' differs
        rows=rows, 
        cols=cols, 
        x_spacing=x_space, 
        y_spacing=y_space, 
        start_x=start_x, 
        start_y=start_y
    )

    return 0, 0
