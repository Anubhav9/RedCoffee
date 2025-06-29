### Documentation for RedCoffee

The current documentation has been divided into 2 categories

* [If you are on Version 2.5 and above](#for-versions-25-and-above)
* [For all version between 0.2 and 2.4](#for-all-versions-between-02-and-24)

This is because from Version 2.5 onwards, there has been a change in the CLI Commands


### General Information regarding all versions

A brief about all the available flags is mentioned herein

| **Flag**       | **Required?** | **Description**                                                                                                                                                                                     |
|----------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--host`       | Yes           | The URL of your SonarQube server.|                                                                                                          |
| `--project`    | Yes           | The project key in SonarQube for which the PDF report should be generated.                                                                                                                          |
| `--path`       | Yes           | File path where the generated PDF report will be saved. As of now, you will be needed to explicitly mention the name of the file as well. So, it can be something like `Desktop/SonarQubeReport.pdf` |
| `--token`      | Yes           | Your SonarQube authentication token with API access permissions. Please note that this should begin with 'squ'. No other tokens are currently supported.                                            |


### For Versions 2.5 and above

Option 1
______
Please use the below CLI Command. You will need to change the variables in here

<pre>redcoffee generatepdf --host=http://localhost:9000 --project=my_project --path=./sonar-report.pdf --token=abcdef1234567890</pre>

In here, users are required to specify the complete URL of the SonarQube Server including the Protocol (HTTP/HTTPS). Here since the protocol is already provided, no Protocol Enforcement is needed from Server Side.


Option 2
______
Using the Protocol Flag to enforce a Protocol

<pre>redcoffee generatepdf --host=my-sonarqube-host:9000 --project=my_project --path=./sonar-report.pdf --token=abcdef1234567890 --protocol=https</pre>

Here since we have explicitly provided a protocol flag, the protocol flag takes the priority and protocol 'https' is enforced.

*What happens if protocol is provided in the host and also at the same time specified via Protocol Flag ?*

In this case as well, the protocol flag will take the priority.

### For all versions between 0.2 and 2.4

Please use the below command

<pre>redcoffee generatepdf --host=${YOUR_SONARQUBE_HOST_NAME} --project=${SONARQUBE_PROJECT_KEY} --path=${PATH WHERE PDF FILE IS TO BE STORED} --token=${SONARQUBE_USER_TOKEN}</pre>

### Latest Command addition in Version 2.16 and above

Pleased to introduce 2 new commands from v2.16 and onwards

`redcoffee diagnose --host={host_name} --token={sonarqube_user_token}` -  This is the healthcheck / sanity command. This makes sures that all the required infra / configurations needed for RedCoffee to be up and running are working fine. If you see something failing over here, its better to cross check the values being supplied.

`redcoffee support` - This is the support command. After running the `redcoffee diagnose` command, if you still could not figure out whats wrong or you need additional support or you might have figured out a bug or you want to request for a new feature, this command provides you with instruction on how to raise it to the maintainer.
