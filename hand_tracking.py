import leap
from leap import datatypes as ldt
import pygame
from multiprocessing import Process
from threading import Thread

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

    def on_tracking_event(self, event):
        for hand in event.hands:
            thumb = get_fingertip_location(hand, 0)
            index = get_fingertip_location(hand, 1)

            is_pinching, diff = detect_pinch(thumb, index)
            if is_pinching:
                pygame.event.post(self.pinch_event)
                print("Skibidi!")
            else:
                pygame.event.post(self.unpinch_event)
                

class LeapHandler:
    def __init__(self, pinch_event, unpinch_event):
        self.listener = PinchingListener(pinch_event, unpinch_event)

        self.leap_connection = leap.Connection()
        self.leap_connection.add_listener(self.listener)
        
        self.leap_process = Thread(target=self.__poll_leap_connection, daemon=True)
        self.leap_process.start()

    def __poll_leap_connection(self):
        with self.leap_connection.open():
            while True:
                ...