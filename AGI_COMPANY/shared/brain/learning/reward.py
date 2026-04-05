"""
Reward Module
Dopamine-like reward modulation.
"""

import random


def apply_reward_to_sheet(sheet, valence):
    """
    Modulate plasticity rates based on valence.
    
    Args:
        sheet: TernaryCorticalSheet3D
        valence: -1.0 to 1.0
    """
    if valence > 0:
        sheet.lr_up = 0.02
        sheet.lr_down = 0.0005
    elif valence < 0:
        sheet.lr_up = 0.005
        sheet.lr_down = 0.005
    else:
        sheet.lr_up = 0.01
        sheet.lr_down = 0.001


def apply_reward_to_tracray(valence, organizer_module):
    """
    Modulate Tracray organization rates.
    
    Args:
        valence: -1.0 to 1.0
        organizer_module: Module with attract_lr and repel_lr
    """
    if valence > 0:
        organizer_module.attract_lr = 0.08
        organizer_module.repel_lr = 0.008
    elif valence < 0:
        organizer_module.attract_lr = 0.03
        organizer_module.repel_lr = 0.02
    else:
        organizer_module.attract_lr = 0.05
        organizer_module.repel_lr = 0.01


def consolidate_memory(memory_store, trace, valence):
    """
    Consolidate memory with probability based on valence.
    
    Args:
        memory_store: Memory storage object
        trace: Memory trace dict
        valence: -1.0 to 1.0
    """
    base_prob = 0.3
    p = base_prob + 0.4 * abs(valence)
    if random.random() < p:
        memory_store.add_trace(**trace)
