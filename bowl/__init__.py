from random import randint

class Ball:

    def throw(self, fallen=0):
        return randint(0, 10 - fallen)

class Frame:

    def __init__(self, frame_number, next_frame):
        self.frame_number = frame_number
        self.pins1 = None
        self.pins2 = None
        self.pins3 = None
        self.next_frame = next_frame

    def has_thrown_1(self):
        return self.pins1 is not None

    def has_thrown_2(self):
        return self.pins2 is not None

    def has_thrown_3(self):
        return self.pins3 is not None

    def is_strike(self):
        return self.has_thrown_1() and self.pins1 == 10

    def is_spare(self):
        return self.has_thrown_1() and self.has_thrown_2() and (self.pins1 + self.pins2 == 10)

    def is_last(self):
        return self.frame_number == 10

    def calc_score(self):
        score = "?"
        if self.is_strike() and self.next_frame and self.next_frame.has_thrown_1() and self.next_frame.has_thrown_2():
            score = 10 + self.next_frame.pins1 + self.next_frame.pins2
        elif self.is_spare() and self.next_frame and self.next_frame.has_thrown_1():
            score = 10 + self.next_frame.pins1
        elif not self.is_strike() and not self.is_spare() and self.has_thrown_1() and self.has_thrown_2():
            score = self.pins1 + self.pins2
        return str(score)

    def __str__(self):
        return f"{self.pins1 or 0:02d}/{self.pins2 or 0:02d}/{self.calc_score():3}"


class Player:

    def __init__(self, playerName, ball):
        self.playerName = playerName
        self.ball = ball
        self.current_frame_index = 0
        self.frames = []
        next_frame = None
        for frame_number in range(10, 0, -1):
            next_frame = Frame(frame_number, next_frame)
            self.frames.insert(0, next_frame)

    def __str__(self):
        score = " ".join(str(frame) for frame in self.frames)
        return f"{self.playerName} {self.current_frame_index:2} {score}"

    def increment_frame(self):
         self.current_frame_index += 1

    def take_turn(self):

        frame = self.frames[self.current_frame_index]

        # every frame has at least 1 throw
        frame.pins1 = self.ball.throw()

        # return early after only 1 throw if not the last frame and strike thrown
        if not frame.is_last() and frame.is_strike():
            self.increment_frame()
            return

        # 2nd throw
        frame.pins2 = self.ball.throw(frame.pins1)

        # extra, 3rd throw if last frame and strike/spare
        if frame.is_last() and (frame.is_strike() or frame.is_spare()):
            frame.pins3 = self.ball.throw()

        self.increment_frame()
 
    def is_game_over(self):
        return self.current_frame_index == 10

    def is_done(self):
        return self.current_frame_index == 9
    


class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def play(self):
        game_over = False
        while not game_over:
            self.player1.take_turn()
            print(self.player1)
            self.player2.take_turn()
            print(self.player2)
            game_over = self.player1.is_game_over() and self.player2.is_game_over()
