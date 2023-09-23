import pygame


pygame.init()

screen_width, screen_height = 1280, 720

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Red Ball - Meme Version")
clock = pygame.time.Clock()

FPS = 30


class Player:
    def __init__(self):
        self.health = 3

        self.is_jump = False
        self.speed = 7
        self.rot_speed = 7
        self.angle = 0

        self.jump_force = 20
        self.jump_count = self.jump_force

        self.x = 640
        self.y = 500

        self.sprite = pygame.image.load('sprites/Player.png').convert_alpha()
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    def update(self):
        self.angle %= 360

        sprite = pygame.transform.rotate(self.sprite, self.angle)
        self.rect = sprite.get_rect(center=(self.x, self.y))

        screen.blit(sprite,
                    self.rect)

    def move(self, direction):
        self.x += self.speed * direction
        self.angle -= self.rot_speed * direction

    def jump(self):
        self.y -= self.jump_count

        if self.jump_count > -self.jump_force:
            self.jump_count -= 1
        else:
            self.is_jump = False
            self.jump_count = player.jump_force

    def set_damage(self):
        self.health -= 1


class Enemy:
    def __init__(self):
        self.time_attack = 30
        self.current_time_attack = self.time_attack
        self.isAttack = False
        self.isDie = False
        self.speed = 5

        self.x = 1000
        self.y = 500

        self.sprite = pygame.image.load("sprites/Enemy.png")
        self.rect = self.sprite.get_rect(center=(self.x, self.y))

    def update(self):
        screen.blit(self.sprite, self.rect)

        if self.isAttack:
            if self.current_time_attack > 0:
                self.current_time_attack -= 1
            else:
                self.isAttack = False
                self.current_time_attack = self.time_attack

    def died(self):
        self.isDie = True


if __name__ == "__main__":
    player = Player()
    enemy_list = [Enemy()]

    bg_sprite = pygame.image.load('sprites/BG.png').convert_alpha()
    bg_rect = bg_sprite.get_rect(center=(screen_width // 2, screen_height // 2))

    filled_hearth_sprite = pygame.image.load('sprites/filled hearth.png').convert_alpha()
    unfilled_hearth_sprite = pygame.image.load('sprites/unfilled hearth.png').convert_alpha()

    ui_hearth = [filled_hearth_sprite.get_rect(center=(1200, 50)),
                 filled_hearth_sprite.get_rect(center=(1150, 50)),
                 filled_hearth_sprite.get_rect(center=(1100, 50))]

    while True:
        screen.blit(bg_sprite, bg_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move(-1)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move(1)

        if keys[pygame.K_w] or keys[pygame.K_SPACE]:
            player.is_jump = True

        if player.is_jump:
            player.jump()

        for i, enemy in enumerate(enemy_list):
            if abs(player.x - enemy.x) <= 100 \
                    and abs(player.x - enemy.x) <= 100 and \
                    not enemy.isDie and not player.is_jump:
                if not enemy.isAttack:
                    player.set_damage()
                    enemy.isAttack = True
            if abs(player.x - enemy.x) <= 40 \
                    and abs(player.x - enemy.x) <= 40 and \
                    not enemy.isDie and (player.is_jump and player.jump_count < -player.jump_force + 2):
                enemy.died()
                enemy_list.pop(i)

            enemy.update()

        player.update()

        t = player.health
        for rect in ui_hearth:
            if t <= 0:
                screen.blit(unfilled_hearth_sprite, rect)
            else:
                screen.blit(filled_hearth_sprite, rect)
            t -= 1

        if player.health <= 0:
            lose_sprite = pygame.image.load("sprites/lose.png")
            lose_rect = lose_sprite.get_rect(center=(640, 360))
            screen.blit(lose_sprite, lose_rect)

        pygame.display.flip()
        clock.tick(FPS)