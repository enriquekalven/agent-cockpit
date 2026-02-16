import os
from scripts.hill_climber import HillClimber

def test_hill_climb_logic():
    """Verify the orchestration logic of the Hill Climber."""
    climber = HillClimber(target_repos=["app"])
    assert climber.iteration == 0
    assert climber.max_iterations == 5
    assert len(climber.target_repos) == 1

def test_hill_climb_logs_dir():
    """Ensure logs directory can be created."""
    if not os.path.exists("hill_climb_logs"):
        os.makedirs("hill_climb_logs")
    assert os.path.exists("hill_climb_logs")
