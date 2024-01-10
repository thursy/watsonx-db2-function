# Empowering Watson Assistant: A Guide to Hosting Python Scripts as Cloud Functions for Natural Language Database Queries in DB2

Introducing a sample Cloud Function script that serves as a deployable extension of Watson Assistant, enhancing its capabilities to enable natural language queries to a DB2 database. Imagine interacting with Watson Assistant in a manner similar to consulting a data analyst. This extension empowers users to articulate complex queries in human language, just as a data analyst would construct SQL commands to perform aggregations on a database. 
The underlying technologies powering this project include:
- Watson Assistant for natural language understanding,
- watsonx.ai for providing GenAI LLM capabilities,
- DB2 as the database management system, and
- IBM Cloud Functions for the serverless execution of the Python script.

By merging these technologies, we aim to bridge the gap between conversational interfaces and powerful data querying, simplifying the interaction and querying process for users.

## __The expected Result:__

<img src="https://github.com/thursy/watsonx-db2-function/assets/32385413/e2316fab-1a5b-4332-bc73-739e4b63f500" alt="image" width="40%" height="auto">


## __The architecture:__

<img width="1114" alt="image" src="https://github.com/thursy/watsonx-db2-function/assets/32385413/11256a00-970a-4bf6-84ed-ddfa3af58b69">


## __Credentials required:__
- DB2 host, password, username
- watsonx.ai project ID
- IAM APIKEY
  
## __Replace all of required credentials in the app.py using your own credentials.__
Note: Git Clone this repo, and replace the with your own credentials, upload your file to IBM Cloud Shell or IBM Cloud CLI.
By using the Docker Image hosted in [DockerHub](https://hub.docker.com/repository/docker/thursysatriani/fn-watsonx/general),
you can use the CLI or Cloud Shell in IBM Cloud to run this commands:

```
bmcloud resource groups --default
ibmcloud target -g <replace_with_your_resource_group>
ibmcloud fn namespace target <your_namespace_name>

COMMAND TO DEPLOY using Docker:
ibmcloud fn action create <the-function-name-> --docker <docker-username/repo:tag> filepython.py --web true
ibmcloud fn action create myfunctionname --docker thursysatriani/fn-watsonx:ibmcfn app.py --web true
```


### References:
- Data – https://www.kaggle.com/datasets/thammuio/all-agriculture-related-datasets-for-india/ 
- Tutorial – https://medium.com/@yi.angela/connecting-watson-assistant-to-db2-with-ibm-cloud-function-and-a-custom-extension-89bbe4c6a83b 
- Sample code – https://github.com/thursy/watsonx-db2-function 
- Docker – https://hub.docker.com/repository/docker/thursysatriani/fn-watsonx/general 
- References – https://cloud.ibm.com/docs/openwhisk?topic=openwhisk-prep#prep_python_docker 

