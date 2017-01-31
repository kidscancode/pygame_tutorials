# Steering Manager example
# KidsCanCode 2016
# TODO: weights
# TODO: seek w/approach
# TODO: flocking
# TODO: pursuit
# TODO: flow field
# TODO: obstacle avoidance
# TODO: default (max speed)

import pygame as pg
from random import uniform
vec = pg.math.Vector2

class SteeringManager:
    def __init__(self, host):
        self.host = host
        self.behaviors = host.behaviors
        self.steering = vec(0, 0)

    def update(self, acc=vec(0, 0)):
        # if self.steering.length_squared() == 0 and self.host.vel.length() < self.behaviors['max_speed']:
        #     desired = self.host.vel.normalize() * self.behaviors['max_speed']
        #     self.steering = (desired - self.host.vel)
        # if self.steering.length() > self.behaviors['max_force']:
        if self.steering.length() != 0:
            self.steering.scale_to_length(self.behaviors['max_force'])
        self.host.acc = acc + self.steering
        # equations of motion
        self.host.vel += self.host.acc
        if self.host.vel.length() > self.behaviors['max_speed']:
            self.host.vel.scale_to_length(self.behaviors['max_speed'])
        self.host.pos += self.host.vel
        self.steering_tmp = vec(self.steering)
        self.steering = vec(0, 0)

    def seek(self, target, weight=1):
        dist = target - self.host.pos
        if dist.length() < self.behaviors['seek_radius']:
            desired = dist.normalize() * self.behaviors['max_speed']
            steer = desired - self.host.vel
            if steer.length() > self.behaviors['max_force']:
                steer.scale_to_length(self.behaviors['max_force'])
            self.steering += steer * weight

    def avoid_walls(self, rect, weight=1):
        near_wall = False
        if self.host.pos.x < rect.left + self.behaviors['wall_limit']:
            desired = vec(self.behaviors['max_speed'], self.host.vel.y)
            near_wall = True
        if self.host.pos.x > rect.right - self.behaviors['wall_limit']:
            desired = vec(-self.behaviors['max_speed'], self.host.vel.y)
            near_wall = True
        if self.host.pos.y < rect.top + self.behaviors['wall_limit']:
            desired = vec(self.host.vel.x, self.behaviors['max_speed'])
            near_wall = True
        if self.host.pos.y > rect.bottom - self.behaviors['wall_limit']:
            desired = vec(self.host.vel.x, -self.behaviors['max_speed'])
            near_wall = True
        if near_wall:
            steer = (desired - self.host.vel)
            # if steer.length() > MAX_FORCE:
            #     steer.scale_to_length(MAX_FORCE)
            self.steering += steer * weight

    def wander(self, weight=1):
        future = self.host.pos + self.host.vel.normalize() * self.behaviors['wander_ring_distance']
        target = future + vec(self.behaviors['wander_ring_radius'], 0).rotate(uniform(0, 360))
        self.seek(target, weight)

    def approach(self, target, weight=1):
        # seek + easing
        pass

    def evade(self, target, weight=1):
        dist = self.host.pos - target
        if dist.length() < self.behaviors['flee_radius']:
            desired = dist.normalize() * self.behaviors['max_speed']
            steer = desired - self.host.vel
            # if steer.length() > MAX_FORCE:
            #     steer.scale_to_length(MAX_FORCE)
            self.steering += steer * weight

    def pursue(self, target, weight=1):
        pass

    def separation(self, avg_dist):
        # desire to move away from nearby mobs
        desired = avg_dist.normalize() * self.behaviors['max_speed']
        steer = desired - self.host.vel
        if steer.length() > self.behaviors['max_force']:
            steer.scale_to_length(self.behaviors['max_force'])
        return steer

    def alignment(self, avg_vel):
        # desire to move in dir of nearby mobs
        desired = avg_vel.normalize() * self.behaviors['max_speed']
        steer = desired - self.host.vel
        if steer.length() > self.behaviors['max_force']:
            steer.scale_to_length(self.behaviors['max_force'])
        return steer

    def cohesion(self, avg_pos):
        # desire to move to center of nearby mobs
        desired = (avg_pos - self.host.pos).normalize() * self.behaviors['max_speed']
        steer = desired - self.host.vel
        if steer.length() > self.behaviors['max_force']:
            steer.scale_to_length(self.behaviors['max_force'])
        return steer

    def get_averages(self, group):
        # find averages for group members
        count = 0
        avg_pos = vec(0, 0)
        avg_dist = vec(0, 0)
        avg_vel = vec(0, 0)
        for obj in group:
            if obj != self.host:
                d = self.host.pos.distance_to(obj.pos)
                if d < self.behaviors['neighbor_radius']:
                    avg_pos += obj.pos
                    avg_vel += obj.vel
                    avg_dist += (self.host.pos - obj.pos).normalize() / d
                    count += 1
        if count > 0:
            avg_pos /= count
            avg_vel /= count
            avg_dist /= count
        return count, avg_pos, avg_dist, avg_vel

    def flock(self, group):
        # get averages for group members w/in range
        count, avg_pos, avg_dist, avg_vel = self.get_averages(group)
        if count > 0:
            sep = self.separation(avg_dist) * self.behaviors['sep_weight']
            ali = self.alignment(avg_vel) * self.behaviors['ali_weight']
            coh = self.cohesion(avg_pos) * self.behaviors['coh_weight']
            self.steering += sep + ali + coh

    def draw_vectors(self, surf):
        scale = 25
        # vel
        pg.draw.line(surf, (0, 255, 0), self.host.pos, (self.host.pos + self.host.vel * scale), 5)
        # desired
        pg.draw.line(surf, (255, 0, 0), self.host.pos, (self.host.pos + self.steering_tmp * scale**2), 5)
        # neighbor radius
        pg.draw.circle(surf, (0, 255, 255), (int(self.host.pos.x), int(self.host.pos.y)), self.behaviors['neighbor_radius'], 1)
        # seek
        pg.draw.circle(surf, (100, 100, 100), pg.mouse.get_pos(), self.behaviors['seek_radius'], 1)
