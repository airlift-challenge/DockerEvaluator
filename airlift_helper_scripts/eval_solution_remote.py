from afrl.evaluators.utils import doremoteeval
from solution.mysolution import MySolution
import click

@click.command()
@click.option('--scenario-folder',
              default="./scenarios",
              help='Location of the evaluation pkl files')
def run_evaluation(scenario_folder):
    doremoteeval(scenario_folder, MySolution())

if __name__ == "__main__":
    print("running remote eval")
    run_evaluation()
