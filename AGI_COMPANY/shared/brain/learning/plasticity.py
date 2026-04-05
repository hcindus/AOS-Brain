"""
Plasticity Module
Step sheet with Hebbian learning and homeostatic decay.
"""

def step_sheet_with_plasticity(sheet):
    """
    Execute one step of cortical dynamics with plasticity.
    
    Args:
        sheet: TernaryCorticalSheet3D instance
    """
    new_state = [0] * len(sheet.state)
    
    for idx in range(len(sheet.state)):
        neighbors = sheet._neighbors(idx)
        excitation = sum(sheet.state[n] * sheet.weight[n] for n in neighbors)
        
        threshold = _threshold(sheet, idx)
        
        if excitation > threshold:
            new_state[idx] = 1
        elif excitation < -threshold:
            new_state[idx] = -1
        else:
            new_state[idx] = 0
            
    _update_plasticity(sheet, new_state)
    sheet.state = new_state


def _threshold(sheet, idx):
    """Calculate activation threshold based on weight"""
    base = 1.0
    return max(0.1, base - 0.3 * (sheet.weight[idx] - 0.5))


def _update_plasticity(sheet, new_state):
    """
    Update synaptic weights based on activation.
    
    Hebbian: active cells strengthen
    Homeostatic: inactive cells decay
    """
    lr_up = getattr(sheet, 'lr_up', 0.01)
    lr_down = getattr(sheet, 'lr_down', 0.001)
    
    for idx, v in enumerate(new_state):
        if v == 1:
            # Strengthen
            sheet.weight[idx] += lr_up * (1.0 - sheet.weight[idx])
        else:
            # Decay
            sheet.weight[idx] -= lr_down * (sheet.weight[idx] - 0.1)
            
    # Clamp
    for idx in range(len(sheet.weight)):
        sheet.weight[idx] = max(0.1, min(1.0, sheet.weight[idx]))
