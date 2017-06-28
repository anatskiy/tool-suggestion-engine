import os
import re
from configparser import ConfigParser, NoOptionError

from sqlalchemy import create_engine
import pandas as pd


def main():
    galaxy_path = os.environ['GALAXY_DIRECTORY']
    config_file = os.path.join(galaxy_path, 'config/galaxy.ini.sample')

    if os.path.isfile(config_file):
        config = ConfigParser()
        config.read_file(open(config_file))

        try:
            # Get database path
            db_conn = config.get('app:main', 'database_connection')
            match = re.match(r'(.+:\/{2,3})(.+)\?', db_conn)
            protocol = match[1]
            file = os.path.join(galaxy_path, match[2])
            db_path = protocol + file if os.path.isfile(file) else db_conn

        except NoOptionError:
            # Default
            db_path = 'sqlite:///' + os.path.join(galaxy_path,
                                                  'database/universe.sqlite')

        # Connect to DB
        engine = create_engine(db_path)

        history_query = """
        SELECT * FROM history
        """

        workflows_steps_query = """
        SELECT * FROM workflow_step
        """

        workflows_steps_connections_query = """
        SELECT * FROM workflow_step_connection
        """

        histories = pd.read_sql(history_query, con=engine)
        w_steps = pd.read_sql(workflows_steps_query, con=engine)
        w_steps_connections = pd.read_sql(workflows_steps_connections_query,
                                          con=engine)

        # Create CSV files
        histories.to_csv('histories.csv')
        w_steps.to_csv('workflow_steps.csv')
        w_steps_connections.to_csv('workflow_steps_connections.csv')


if __name__ == '__main__':
    main()
