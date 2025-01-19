from textx import metamodel_from_file

# all the validators are in the validators.py file
from validators import validate_move_command

robot_mm = metamodel_from_file('robot.tx')


robot_mm.register_obj_processors({'MoveCommand': validate_move_command})

robot_model = robot_mm.model_from_file('program.rbt')


class Robot:

    def __init__(self):
        # Initial position is (0,0)
        self.x = 0
        self.y = 0
        self.direction = "north"

    def __str__(self):
        return f"Robot position is {self.x}, {self.y} facing {self.direction}."

    def interpret(self, model):

        # Define the circular order of directions
        directions = ["north", "east", "south", "west"]

        # Define the movement deltas for each direction
        direction_moves = {
            "north": (0, 1),
            "east": (1, 0),
            "south": (0, -1),
            "west": (-1, 0)
        }

        # model is an instance of Program
        for c in model.commands:

            match(c.__class__.__name__):
                case "InitialCommand":
                    print(f"Setting position to: {c.x}, {c.y}")
                    self.x = c.x
                    self.y = c.y

                case "TurnCommand":
                    print(f"Turning {c.direction}.")
                    # Get current direction index
                    current_index = directions.index(self.direction)
                    # Update direction based on turn direction
                    if c.direction == "left":
                        self.direction = directions[(current_index - 1) % 4]
                    elif c.direction == "right":
                        self.direction = directions[(current_index + 1) % 4]

                case "MoveCommand":
                    print(f"Going {c.direction} for {c.steps} step(s).")

                    move = direction_moves[self.direction]
                    # Calculate new robot position
                    self.x += c.steps * move[0]
                    self.y += c.steps * move[1]

            print(self)


robot = Robot()
robot.interpret(robot_model)
