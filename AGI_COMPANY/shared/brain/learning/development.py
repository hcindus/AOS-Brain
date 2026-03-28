"""
Development Module
Simulate developmental stages like a child.
"""


class BrainDevelopment:
    """
    Tracks developmental stage and configures brain parameters.
    """
    
    def __init__(self, infant_steps=10_000, child_steps=100_000, adolescent_steps=1_000_000):
        self.age_steps = 0
        self.infant_steps = infant_steps
        self.child_steps = child_steps
        self.adolescent_steps = adolescent_steps
        
    def step(self):
        """Increment age"""
        self.age_steps += 1
        
    def stage(self):
        """Get current developmental stage"""
        if self.age_steps < self.infant_steps:
            return "infant"
        elif self.age_steps < self.child_steps:
            return "child"
        elif self.age_steps < self.adolescent_steps:
            return "adolescent"
        return "adult"
        
    def configure(self, sheet, limbic):
        """
        Configure brain parameters based on stage.
        
        Args:
            sheet: TernaryCorticalSheet3D
            limbic: Limbic agent with novelty_gain
        """
        s = self.stage()
        
        if s == "infant":
            sheet.lr_up = 0.05
            sheet.lr_down = 0.0001
            limbic.novelty_gain = 2.0
        elif s == "child":
            sheet.lr_up = 0.02
            sheet.lr_down = 0.0005
            limbic.novelty_gain = 1.5
        elif s == "adolescent":
            sheet.lr_up = 0.01
            sheet.lr_down = 0.001
            limbic.novelty_gain = 1.2
        else:  # adult
            sheet.lr_up = 0.005
            sheet.lr_down = 0.002
            limbic.novelty_gain = 1.0
            
        return s
