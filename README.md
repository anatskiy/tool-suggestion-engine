# Suggestion engine for galaxy

## goals

This extension of galaxy will provide suggestion of tools to use after the ones chosen in the workflow.

The suggestion will be made making use of the available workflows of the server.



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


