from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites

print("Hello From Afar")

class Game:
    def __init__(self):
        pygame.init()
        #setup the display image
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        #setup window name
        pygame.display.set_caption("From Afar")

        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        map = load_pygame(join("data","maps","FromAfarMap.tmx"))
        for obj in map.get_layer_by_name("ground"):
            Ground_sprite((obj.x,obj.y), obj.image, self.all_sprites)

        for obj in map.get_layer_by_name("collisions"):
            CollisionSprite((obj.x,obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        for obj in map.get_layer_by_name("Player"):
            if obj.name == "Player":
                self.player = Player((obj.x,obj.y),self.all_sprites, self.collision_sprites)

    def run(self):
        while(self.running):
            #delta time
            dt = self.clock.tick() / 1000

            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #update
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill("black")
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()