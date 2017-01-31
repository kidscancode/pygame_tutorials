# Particles for pygame
# by KidsCanCode 2015
# For educational purposes only
import pygame
import random

# TODO: particle rotations
# TODO: test with varied particle images
# TODO: more particle paths

def interpolate(v1, v2, range):
    return pygame.math.Vector2(v1.x + (v2.x - v1.x) * range,
                               v1.y + (v2.y - v1.y) * range)

class Particle(pygame.sprite.Sprite):
    def __init__(self, game, image, pos, vel, life, lifetime,
                 fade_start, dorotate):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.pos = pos
        self.vel = vel
        self.rot_cache = {}
        self.base_image = image
        self.dorotate = dorotate
        if dorotate:
            self.image = pygame.transform.rotate(self.base_image, -self.rot)
        else:
            self.image = self.base_image.copy()

        self.rect = self.image.get_rect()
        self.lifetime = lifetime
        self.life = life
        self.fade_start = fade_start
        self.duration = lifetime - fade_start
        self.update()

    def update(self):
        # if self.dorotate:
        #     old_center = self.rect.center
        #     if self.rot in self.rot_cache:
        #         self.image = self.rot_cache[self.rot]
        #     else:
        #         self.image = pygame.transform.rotate(self.base_image, -self.rot)
        #         self.rot_cache[self.rot] = self.image
        #     self.rect = self.image.get_rect()
        #     self.rect.center =  old_center

        self.life += self.game.dt
        self.fade()
        self.pos += self.vel
        self.rect.centerx = self.pos.x  # + self.game.OFFSET.x
        self.rect.centery = self.pos.y  # + self.game.OFFSET.y

    def blit(self):
        return self.game.screen.blit(self.image, self.rect, special_flags=pygame.BLEND_ADD)

    def fade(self):
        if self.life > self.fade_start:
            try:
                ratio = (self.life - self.fade_start) / self.duration
            except ZeroDivisionError:
                ratio = 1.0
            if ratio > 1.0:
                ratio = 1.0
            mask = int(255 * (1 - ratio))
            self.image.fill([mask, mask, mask], special_flags=pygame.BLEND_MIN)

    def is_dead(self):
        if self.life > self.lifetime:
            return True
        return False

class ParticleEmitter:
    def __init__(self, game, parent, offset, vel, image, count, lifetime,
                 fade_start, size, angle_range, dorotate=False):
        self.game = game
        self.parent = parent
        self.offset = offset
        self.particle_vel = vel
        self.pos = self.parent.pos + self.game.OFFSET + self.offset.rotate(self.parent.rot)
        self.base_image = image
        self.size = size
        self.angle_range = angle_range
        self.image = pygame.transform.scale(self.base_image, (self.size, self.size))
        self.count = count
        self.lifetime = lifetime
        self.fade_start = fade_start
        self.particles = []
        self.timer = 0
        self.prevcurve = [self.pos for x in range(3)]
        self.active = True

    def print_state(self):
        print("c:{}, p:{}".format(self.count, len(self.particles)))

    def update(self):
        self.pos = self.parent.pos + self.game.OFFSET + self.offset.rotate(-self.parent.rot)
        self.rand_angle = random.randint(-self.angle_range, self.angle_range)
        # update all particles
        for part in self.particles:
            part.update()
            if part.is_dead():
                self.particles.remove(part)
                # print("p.kill")

        # create a new particle
        if self.count != 0 and self.active:
            self.timer += self.game.dt
            newparticles = self.count * self.timer
            if newparticles > 1:
                for i in range(int(newparticles)):
                    t = i / newparticles
                    time_elapsed = (1.0 - t) * self.game.dt

                    vel = self.particle_vel.rotate(-self.parent.rot + self.rand_angle)
                    pos = interpolate(self.prevcurve[0], self.pos, t)
                    pos += (self.parent.vel + vel) * time_elapsed
                    # pos += vel * time_elapsed
                    init_life = time_elapsed
                    self.timer = 0
                    # print("new part: pos: {} vel: {}".format(pos, vel))
                    self.particles.append(Particle(self.game, self.image, pos,
                                                   vel, init_life, self.lifetime,
                                                   self.fade_start, False))

        self.prevcurve[2] = self.prevcurve[1]
        self.prevcurve[1] = self.prevcurve[0]
        self.prevcurve[0] = self.pos

    def draw(self):
        rects = []
        for part in self.particles:
            rects.append(part.blit())
        return rects

    def kill_all(self):
        self.count = 0
        self.active = False
        self.particles = []
