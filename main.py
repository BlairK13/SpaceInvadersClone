import pygame
import sys
import random
from Enemy import Enemy
from Bullet import Bullet, EnemyBullet
from Player import Player
from config import screen_width, screen_height, BLACK, WHITE, RED
from utils import (
    spawn_enemies_in_grid,
    draw_text,
    display_message,
    handle_collisions,
    can_shoot,
    reset_game
)

if __name__ == "__main__":
    pygame.init()

    # Window setup
    screen = pygame.display.set_mode([screen_width, screen_height])
    pygame.display.set_caption("Space Invaders")

    font = pygame.font.Font(None, 36)

    # Load background
    try:
        background = pygame.image.load('assets/background.jpg').convert()
        background = pygame.transform.scale(background, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Unable to load background image: {e}")
        background = pygame.Surface(screen.get_size())
        background.fill(BLACK)

    # Sprite groups
    enemy_list = pygame.sprite.Group()
    all_sprites_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    enemy_bullet_list = pygame.sprite.Group()

    # Create player
    player = Player()
    player.rect.y = int(screen_height * 0.9)
    player.rect.x = int(screen_width * 0.5)
    all_sprites_list.add(player)

    # Spawn initial enemies
    rows = 5
    cols = 8
    x_spacing = 50
    y_spacing = 15
    start_x = 50
    start_y = 50

    spawn_enemies_in_grid(
        enemy_class=Enemy,
        enemy_list=enemy_list,
        all_sprites_list=all_sprites_list,
        rows=rows,
        cols=cols,
        x_spacing=x_spacing,
        y_spacing=y_spacing,
        start_x=start_x,
        start_y=start_y
    )

    done = False
    clock = pygame.time.Clock()
    FPS = 60

    score = 0
    lives = 3
    elapsed_time = 0

    last_shot_time = 0
    bullet_cooldown = 500

    enemy_direction = 1
    enemy_speed = 1
    enemy_move_down = 10

    player_speed = 5
    moving_left = False
    moving_right = False

    # Main loop
    while not done:
        elapsed_time = pygame.time.get_ticks() // 1000
        if elapsed_time > 100:
            done = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    can_fire, last_shot_time = can_shoot(last_shot_time, bullet_cooldown)
                    if can_fire:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False

        # Handle player movement
        if moving_left:
            player.rect.x -= player_speed
            if player.rect.x < 0:
                player.rect.x = 0
        if moving_right:
            player.rect.x += player_speed
            if player.rect.x > screen_width - player.rect.width:
                player.rect.x = screen_width - player.rect.width

        # Update enemies (they need direction)
        enemy_list.update(enemy_direction)

        # Update bullets, enemy bullets, and player (though player update is empty)
        bullet_list.update()
        enemy_bullet_list.update()
        player.update()

        # Check enemy boundaries
        change_direction = False
        for enemy in enemy_list:
            # Enemy firing
            if random.random() < 0.001:
                e_bullet = EnemyBullet(enemy.rect.centerx, enemy.rect.bottom)
                all_sprites_list.add(e_bullet)
                enemy_bullet_list.add(e_bullet)

            # If an enemy hits the sides
            if enemy.rect.right >= screen_width or enemy.rect.left <= 0:
                change_direction = True

        # If any enemy hits the side, reverse direction and bump down
        if change_direction:
            enemy_direction *= -1
            for enemy in enemy_list:
                enemy.rect.y += enemy_move_down

        # Collisions with bullets
        score, game_over = handle_collisions(bullet_list, enemy_list, all_sprites_list, score)
        if game_over:
            done = True

        # Collisions with enemy bullets
        if pygame.sprite.spritecollide(player, enemy_bullet_list, True):
            lives -= 1
            if lives <= 0:
                done = True

        # Increase difficulty as score grows
        if score > 0 and score % 10 == 0:
            enemy_speed += 0.5
            score += 1

        if len(enemy_list) == 0:
            done = True     

        # Rendering
        screen.blit(background, (0, 0))
        all_sprites_list.draw(screen)

        # Display stats
        draw_text(screen, f"Score: {score}", font, WHITE, 10, 10)
        draw_text(screen, f"Lives: {lives}", font, WHITE, 10, 40)
        draw_text(screen, f"Time: {elapsed_time}s", font, WHITE, screen_width - 150, 10)

        pygame.display.flip()
        clock.tick(FPS)

    # End game
    if score >= 50:
        display_message(screen, "You Win!", font, WHITE, screen_width, screen_height, 3000)
    elif lives <= 0:
        display_message(screen, "Game Over!", font, WHITE, screen_width, screen_height, 3000)
    else:
        display_message(screen, "Time Up!", font, WHITE, screen_width, screen_height, 3000)

    pygame.quit()
    sys.exit()
