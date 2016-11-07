import pandas as pd
import sqlite3
import re

base_directory = "/home/u/abc/galaxy/"

with open(base_directory + './config/galaxy.ini') as file:
    # default
    db_path = 'database/universe.sqlite'

    # if different value in config file
    for line in file:
        if re.match('^database_connection\ =.*', line):
            db_path = re.sub('database_connection\ = sqlite:///./', '', line)
            # without the index the string finishes with a space
            db_path = re.sub('\?.*', '', db_path)[:-1]

# connect to database -> will change to ORM/SQLalchemy
conn = sqlite3.connect(base_directory + db_path)

query = '''
    SELECT job.tool_id, metric_value AS runtime_seconds, galaxy_user.username
    FROM job_metric_numeric INNER JOIN job INNER JOIN galaxy_user
    WHERE metric_name=\'runtime_seconds\' AND job.id=job_metric_numeric.job_id
'''

tools_runtime = pd.read_sql(query, con=conn)

df = pd.DataFrame(tools_runtime,
                  columns=['tool_id', 'runtime_seconds', 'username'])

# convert entries in unicode to string (required by HDF)
types = df.apply(lambda x: pd.lib.infer_dtype(x.values))
for col in types[types == 'unicode'].index:
    df[col] = df[col].astype(str)
df.columns = [str(c) for c in df.columns]

tools_dataset_list = []
hdf = pd.HDFStore('runtime_by_tool.hdf5')
hdf.append('hdf', df)
hdf.close()
