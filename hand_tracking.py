import leap
from leap import datatypes as ldt
from leap.events import Event
import pygame
from multiprocessing import Process
from threading import Thread
from ship import Ship

PINCH_THRESHOLD = 20


def get_fingertip_location(hand: ldt.Hand, digit_idx: int) -> ldt.Vector:
    digit = hand.digits[digit_idx]
    return digit.distal.next_joint

def subtract_vectors(v1: ldt.Vector, v2: ldt.Vector) -> list:
    return map(float.__sub__, v1, v2)

def detect_pinch(thumb: ldt.Vector, index: ldt.Vector):
    diff = list(map(abs, subtract_vectors(thumb, index)))

    if all([diff[i] < PINCH_THRESHOLD for i in range(0, 3)]):
        return True, diff
    else:
        return False, diff

class PinchingListener(leap.Listener):
    def __init__(self, pinch_event, unpinch_event):
        self.pinch_event = pinch_event
        self.unpinch_event = unpinch_event
        self.already_pinched = False
        self.already_unpinched = True

    def on_tracking_event(self, event):
        for hand in event.hands:
            thumb = get_fingertip_location(hand, 0)
            index = get_fingertip_location(hand, 1)

            is_pinching, diff = detect_pinch(thumb, index)

            print(f"Firing: {is_pinching}")

            if is_pinching and not self.already_pinched:
                pygame.event.post(self.pinch_event)
                self.already_pinched = True
                self.already_unpinched = False
            
            if not is_pinching and not self.already_unpinched:
                pygame.event.post(self.unpinch_event)
                self.already_unpinched = True
                self.already_pinched = False

class HorizontalListener(leap.Listener):
    def __init__(self, game_screen: pygame.Surface, ship: Ship):
        self.screen_rect = game_screen.get_rect()
        self.max = 200
        self.min = -200
        self.ship = ship
        self.leap_offset = self.screen_rect.midbottom[0]

        

    def on_tracking_event(self, event: Event):
        for hand in event.hands:
            print(f"Current Position: {hand.palm.position.x}")
            if hand.palm.position.x > self.max:
                self.max = hand.palm.position.x
            elif hand.palm.position.x < self.min:
                self.min = hand.palm.position.x
            elif -100 < hand.palm.position.x < 100:
                self.max -= 1 if self.max > 200 else 0
                self.min += 1 if self.min < -200 else 0
            movement_factor = (self.screen_rect.right - self.leap_offset) / max(self.max, abs(self.min))
            self.ship.rect.x = min(self.screen_rect.right - self.ship.rect.width, hand.palm.position.x * movement_factor + self.leap_offset)

            print(f"Minimum Value: {self.min}")
            print(f"Maximum Value: {self.max}")
            print("\x1b[H\x1b[J", end="")
            #if hand.palm.position.x > 50:
            #    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d))
            #elif hand.palm.position.x < -50:
            #    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a))
            #else:
            #    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_d))
            #    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_a))
                


class LeapHandler:
    def __init__(self, pinch_event, unpinch_event, game_screen, ship):
        self.pinch_listener = PinchingListener(pinch_event, unpinch_event)
        self.horizontal_listener = HorizontalListener(game_screen, ship)

        self.leap_connection = leap.Connection()
        self.leap_connection.add_listener(self.pinch_listener)
        self.leap_connection.add_listener(self.horizontal_listener)
        
        self.leap_process = Thread(target=self.__poll_leap_connection, daemon=True)
        self.leap_process.start()

    def __poll_leap_connection(self):
        with self.leap_connection.open():
            while True:
                pygame.time.wait(1000)