from settings import *

class Player_shadow(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("assets","player_shadow","0.png")).convert_alpha()
        self.rect = self.image.get_frect(midbottom=pos)
        self.is_shadow = True

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, hitbox, groups, collision_sprites):
        super().__init__(groups)
        self.load_images()
        self.state = "right"
        self.image = pygame.image.load(join("assets","player","sprite4","right","0.png")).convert_alpha()
        self.hitbox_rect = pygame.FRect(hitbox["x"],hitbox["y"],hitbox["width"],hitbox["height"])
        self.sprite_offset = (0,-1)
        self.animation_offset = (0,0)
        self.rect = self.image.get_frect(midbottom=(self.hitbox_rect.midbottom[0]+self.sprite_offset[0]+self.animation_offset[0],self.hitbox_rect.midbottom[1]+self.sprite_offset[1]+self.animation_offset[1]))
        self.shadow = Player_shadow((self.hitbox_rect.midbottom[0]+self.sprite_offset[0],self.hitbox_rect.midbottom[1]+self.sprite_offset[1]),groups)
        self.frames_offset = [(0,0),(0,-5)]
        
        #animation
        self.frame_index = 0

        #movement
        self.direction = pygame.Vector2(0,0)
        self.speed = 1500
        self.collision_sprites = collision_sprites
    
    def load_images(self):
        self.frames = {"left": [], "right": [],"up": [],"down": []}

        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join("assets","player","sprite4", state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split(".")[0])):
                        full_path = join(folder_path,file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) 
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
        self.direction = self.direction.normalize() if self.direction else self.direction

    def move(self,dt):
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision("horizontal")
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision("vertical")
        self.rect.midbottom = (self.hitbox_rect.midbottom[0]+self.sprite_offset[0],self.hitbox_rect.midbottom[1]+self.sprite_offset[1])
        self.shadow.rect.midbottom = (self.hitbox_rect.midbottom[0]+self.sprite_offset[0],self.hitbox_rect.midbottom[1]+self.sprite_offset[1])
    
    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == "horizontal":
                    if self.direction.x > 0: self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0: self.hitbox_rect.left = sprite.rect.right
                else:
                    if self.direction.y < 0: self.hitbox_rect.top = sprite.rect.bottom
                    if self.direction.y > 0: self.hitbox_rect.bottom = sprite.rect.top

    def animate(self, dt):
        # get state
        if self.direction.x != 0:
            self.state = "right" if self.direction.x > 0 else "left"
        if self.direction.y != 0:
            self.state = "down" if self.direction.y > 0 else "up"


        # animate
        # self.frame_index = self.frame_index + 8 * dt
        # self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]

        self.frame_index = self.frame_index + 4 * dt
        self.image = self.frames[self.state][0]
        actual_frame = int(self.frame_index) % len(self.frames_offset)
        self.rect.midbottom = (self.rect.midbottom[0]+self.frames_offset[actual_frame][0],self.rect.midbottom[1]+self.frames_offset[actual_frame][1])

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)