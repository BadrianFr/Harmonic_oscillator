# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 09:09:14 2026

@author: adria
"""

from dataclasses import dataclass
import math

g=9.82 #m/s^2 

@dataclass
class Fjeder:
    def __init__(self, masse, fjederKonstant):
        self.masse = masse
        self.fjederkonstant = fjederKonstant

    def getMasse(self):
        return self.masse

    def getKonstant(self):
        return self.fjederkonstant


class Lod:
    def __init__(self, masse, radius):
        self.masse = masse
        self.radius = radius

    def getMasse(self):
        return self.masse
    
    def getRadius(self):
        return self.radius


# ---------- FYSIKFORMER ----------

def getSamletMasse(fjeder, lod):
    return fjeder.getMasse() + lod.getMasse()


def getLigevægt(fjeder, lod, m):
    return (m * g) / fjeder.getKonstant()


def getVinkelhastighed(fjeder, lod, m):
    k = fjeder.getKonstant()
    return math.sqrt(k / m)

def getSted(t, A, omega, dæmp):
    return A*math.e**(-dæmp*t) * math.cos(omega * t)


def getHastighed(t, A, omega, dæmp):
    return A * math.e**(-dæmp * t) * (-dæmp * math.sin(omega * t) + omega * math.cos(omega * t))


def getAcceleration(t, A, omega, dæmp):
    return A * math.e**(-dæmp * t) * ((dæmp**2 - omega**2) * math.sin(omega * t) - 2 * (dæmp * omega * math.cos(omega * t)))


def getFRes(fjeder, x):
    return -fjeder.getKonstant() * x