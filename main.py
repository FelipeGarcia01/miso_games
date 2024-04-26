#!/usr/bin/python3
"""Función Main"""
import os

from src.engine.game_engine import GameEngine

if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    engine = GameEngine()
    engine.run()
