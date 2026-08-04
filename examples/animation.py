class Animation:

    def __init__(self,frames,duration=53.3,direction=1):
        self.frames = frames
        self.direction = direction

        self.state = 'idle'

        self.current = self.frames[self.state]

        self.animation_speed = 16/duration
        self.idx = 0
        self.idx_f = 0
        self.isfinished = False


    def set_state(self,state):
        if self.state != state:
            self.state = state
            self.idx = 0
            self.idx_f = 0
            self.current = self.frames[self.state]

    def update(self):
        self.idx_f += self.animation_speed
        self.idx = int(self.idx_f)

        if self.idx >= len(self.current[self.direction]):
            self.idx = 0
            self.idx_f = 0
            self.isfinished = True
        else:
            self.isfinished = False

    @property
    def index(self):
        return self.idx
    
    @property
    def image(self):
        return self.current[self.direction][self.idx]

    @property
    def finished(self):
        return self.isfinished