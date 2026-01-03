import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print("Screen width: 1280")
    print("Screen height: 720")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock() 
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()


    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()
    player = Player(x=SCREEN_WIDTH // 2, y = SCREEN_HEIGHT // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        dt = clock.tick(60) / 1000
        updatable.update(dt)

        for asteroid in list(asteroids):
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                pygame.quit()
                return
        
        for shot in list(shots):
            for asteroid in list(asteroids):
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                    asteroid.kill()
                    
                    break

        screen.fill("black")
        for entity in drawable:
            entity.draw(screen)
        pygame.display.flip()

        log_state()

if __name__ == "__main__":
    main()

