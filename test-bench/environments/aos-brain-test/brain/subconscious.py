class SubconsciousLayer:
    def __init__(self, hippocampus):
        self.hippo = hippocampus

    def context(self, obs):
        # Retrieve short-term working context
        return self.hippo.retrieve(obs)
