from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.Vector2()
    
    def draw(self, target_position):
        self.offset.x = -(target_position[0] - WINDOW_WIDTH/2)
        self.offset.y = -(target_position[1] - WINDOW_HEIGHT/2)

        ground_sprites = [sprite for sprite in self if hasattr(sprite,"ground")]
        shadow_sprites = [sprite for sprite in self if hasattr(sprite,"is_shadow")]
        object_sprites = [sprite for sprite in self if not (hasattr(sprite,"ground") or hasattr(sprite,"is_shadow"))]

        for layer in [ground_sprites, shadow_sprites, object_sprites]:
            for sprite in sorted(layer, key = lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)