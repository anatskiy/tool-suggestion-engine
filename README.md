# Suggestion engine for galaxy

## goals

This extension of galaxy will provide suggestion of tools to use after the ones chosen in the workflow.

The suggestion will be made making use of the available workflows of the server.


## Installation

### Dependencies

- pandas
- sqlite3
- bioblend
- re (temporary)

>sudo pip install pandas sqlite3 re


## Manual

Synopsis:

- From one existing instances, existing histories and workflows are downloaded (standalone python script).
- Downloaded histories and workflows are uploaded to a temporary galaxy instance
- and suggestions are computed and stored in an HDF store.



### Install a brand new galaxy instance (or remove histories and 

>git clone https://github.com/galaxyproject/galaxy
>cd galaxy


### Do some administration stuff

> cp config/galaxy.ini.sample config/galaxy.ini

Using the UI, register and get an API key ([wiki](https://wiki.galaxyproject.org/Learn/API))

Store the API key in `../galaxy_api_key` (file in the parent folder of `galaxy/`)


### Extract histories and workflows with the python script (reads the database):

>cd $GALAXY_DIRECTORY
>python extract-histories-and-workflows-from-an-instance.py

This creates the file `histories.csv`.


### Load histories to the brand new galaxy instance, extract workflows and get suggestions

> python suggestions-from-history.py

This produces an hdf file named `recommendation_table.hdf`

with the following structure:

| tool | suggestion | proof |
|:-----|:-----------|:------|
|      |            |       |

[Structure of HDF file]

The `suggestion` is the most frequent tool present after the selected `tool` in the used history.

The `proof` columun contains the number of occurences of this association.


----

# Development considerations


## Modularity

This engine should have several levels (in decreasing deepness order)

- data  collection (cf intergalactic radio telescope)
- data analysis and model building (macĥine learning)
- input of user expectations (configuration)
- evaluation of input data with regards to the model (real time )
- visual display of analysis


## User experience

- "NEW: a recommendation engine"
- "this will influence your work, the goal is to speed you up, the risk is to kill your creativity or prevent you from learning"
- "enter how much you want to be helped" LEVEL=(default=1) "and when you want to be asked to update these parameters" RECALL=(default=next_week)
- "now when there is a good recommendation, you will see it"
- "As you have added <tool_id> to your workflow, it would be interesting that you use <proposed_tool_id> as <reason>".
- we need more (and more and infinitely more) data to improve the recommendation model. If you accept that your workflow be used for data mining, anonymously, click here. Thanks and good luck to keep in the process of privacy saving.


