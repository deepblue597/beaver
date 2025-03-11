# Validation Functions for MoveCommand
def validate_positive_steps(move_command):
    """Ensure steps are positive."""
    if move_command.steps < 0:
        raise ValueError(f"Invalid step count '{move_command.steps}' in command '{
                         move_command.direction}'. Steps must be positive.")


def move_command_processor(move_cmd):

    # If steps is not given, set it do default 1 value.
    if move_cmd.steps == 0:
        move_cmd.steps = 1


def validate_move_command(move_command):
    """Wrapper function for all MoveCommand validations."""
    validate_positive_steps(move_command)
    move_command_processor(move_command)
    # Add more validations as needed
