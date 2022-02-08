# Install the workshop tools
## Prerequisites
You'll need
- an OpenShift cluster - with admin rights. You can create one by following the instructions [here](http:/try.openshift.com)
- the OpenShift command line interface, _oc_ available [here](https://docs.openshift.com/container-platform/4.6/cli_reference/openshift_cli/getting-started-cli.html)

## Installation procedure

There are two versions of this workshop you can choose to use:
- an FSI Use Case
- a Telco use case
Both are functionally identical - but use different product data examples, applicable to the chosen use case. At various part of the workshop, you use different files approapiate to your chosen use case.

If you are running this as a workshop, it is recommended you fork this repo as there are changes you can make to your instance of the repo, that will simplify the experience for the students. See section _Updating Tool URLs_ below.

Do the following:
- Clone this repo (or a fork thereof if you are a facilitator for students) and change directory into the root dir, _ml-workshop_.  Create a variable *REPO_HOME*_ for this directory
```
git clone https://github.com/masoodfaisal/ml-workshop
cd ml-workshop
export REPO_HOME=`pwd`
```
- On the OpenShift console, choose the _Copy Login Command_ as shown and paste the _oc login ..._ command it gives to a terminal.
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/29-copy-login-command.png)

- Create a new project on the terminal
```
oc new-project ml-workshop  
```

- On GUI, select click project ml-workshop to select it
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/30-select-ml-workshop-project.png)

- Before installation, you may need to get your OpenShift cluster administrator to adjust your limit ranges - or delete if this a test cluster without resource pressures. This is because, there are some moderate resource requirements associated with this workshop, e.g. Jenkins alone requires 4 vCPU and 4 Gi memory and there are other resource hungry elements as well. These are set here:
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/29-resource-limits.png)

- Next, install Open Data Hub Operator on the Operator Hub screen. Filter on _Open Data Hub_ and go with all the defaults. It will install in the openshift-operators namespace (this takes several minutes)
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/1-2-operatorhub-odh.png)


At this point, on GUI go to Installed Operators and wait until the _Open Data Hub_ related operator is installed.
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/1-5-operatorhub-install-succeededXXXXXXXXXX.png)


Now it's time to install the Jenkins Operator - our CICD engine. Click project ml-workshop to select it (it will have de-selected in the last step).
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/1-1-operatorhub-jen-1-v2.png)


From here, go with all the defaults, Clicking Install and again click on Install on the next screen.(this can take several minutes)

Now we'll install the tools that we'll use today, many of which are in the Open Data Hub. We've created a convenient manifest containing everything you need. You just need to apply is as follows:

```
oc project ml-workshop  
oc apply -f https://raw.githubusercontent.com/masoodfaisal/odh-manifests/master/kfdef/kfctl_openshift_ml_workshop.yaml
```

There is a known bug whereby two operator groups get created when operators are created in quick succession. 

So you need to do this check, maybe 30 seconds after the previous _oc apply_:
```
oc project ml-workshop  
oc get og
```
If it returns two entries, as shown, delete one as shown by running: 
```
oc delete og ml-workshop-XXXXX
(substituting your value for XXXXX)
```

![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/1-5-two-operator-groups-delete-one.png)


After a few minutes, on GUI go back to _Installed Operators_ and wait until these Open Data Hub and Jenkins operators are installed as shown. If any are still in _Pending Update_ state after 5 mins, delete them and they should install within 5-10 mins.
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/1-5-operatorhub-install-succeeded-incl--spark-seldon.png)


Now it's time to test each of the tools installed. Each of the tools we use should have an OpenShift Route created
## Test Routes
Then on the GUI, open the menu item _Networking->Routes_ and you'll see some routes including these and others:

![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/32-routes.png)

If _ml-modeldb-webapp_ is missing, run the following:
```
oc project ml-workshop  
oc expose svc modeldb-webapp
```
Test each route as follows:

- jenkins-ml-jenkins: login with your OpenShift credentials
- jupyterhub: 
The first thing we need to do, before we login, is install a custom Jupyter image that contains required libraries for the three data-science focused workshops. Then we label it so it appears in the Jupyter Spawn Image dropdown. For more on that, see [Adding custom notebook images](https://opendatahub.io/docs/administration/installation-customization/add-custom-image.html)


Now delete the _jupyterhub-XXXXXX_ pod and then login with your OpenShift credentials. On the Spawner page, the Jupyter Spawn Image dropdown should contain an entry called _ml-workshop_

- minio-ml-workshop-ui: login with credentials _minio / minio123_
- ml-modeldb-webapp: no credentials needed
- odh-dashboard: not required for the workshop
- superset: login with credentials _admin / admin_

## Import assets

### Jenkins

Login to Jenkins as described previously and choose New Item as shown.
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/33-jenkins-new-item.png)

Name it _deploy-model_, select _Pipeline_ as shown and click *OK*:
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/34-new-item-deploy-model.png)

Now go ahead and click _This project is parameterized_ and add the 2 String parameters _namespace_ (with default ml-workshop) and *experiment_id* as shown:
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/35-pipeline-param.png)

Don't save it yet.

Scroll down to the _Pipeline_ section. Inside the _Script_ box, you need to paste in a _Jenkinsfile_.


Copy the contents of this [Jenkinsfile](https://raw.githubusercontent.com/masoodfaisal/ml-workshop/main/jenkins-pipeline/model/Jenkinsfile) and click *Save*:

![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-add-jenkinsfile.png)


Next, you need to ensure the Jenkins Service IPs are set. 
- Inside Jenkins, navigate to _Jenkins -> Manage Jenkins_
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-manage-1.png)

- Scroll down to _Manage Nodes and Clouds_
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-manage-2.png)

- Choose _Configure Clouds_
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-manage-3.png)

- Click _Kubernetes Cloud Details_
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-manage-4.png)

- Scroll down to _Jenkins URL_ and _Jenkins Tunnel_. They should look like this (Jenkins URL starting with _http_ and with port 8080, Jenkins Tunnel just an IP and port 50000)
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-manage-5.png)

- If not, open a new tab and go to Networking -> Services, filter on _Jenkins_ and get the 2 IPs and slot them into the previous section (_Jenkins URL_ and _Jenkins Tunnel_) remembering to begin _Jenkins URL_ with a _http_ and save there.
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/36-jenkins-services.png)

--------------------------------------------------------------------------------------------------------


# Adding users to the workshop
We provide a sample 30 user setup: _user1_.._user30_ each with the password _openshift_
These have beeen populated to the file _users.htpasswd_ in this directory.
First we create a secret with those users and their password:
```
cd $REPO_HOME/docs
oc create secret generic htpass-secret --from-file=htpasswd=users.htpasswd -n openshift-config
```
We've created a custom resource that sets up this htpasswd mechanism on OpenShift - which we apply as follows:
```
oc apply -f htpasswd.cr
```

If you need to give the users access to their own namespace(project), say _userX-project_. We also need to give Jenkins (used for CICD) access to each user's project.
That can be done as follows:
```
for i in {1..30}
do
    oc new-project user$i-project
    oc adm policy add-role-to-user admin user$i -n user$i-project
    oc adm policy add-role-to-user admin user$i -n ml-workshop
    oc create sa seldon-manager -n user${i}-project
    oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:user${i}-project:seldon-manager -n user${i}-project
    oc adm policy add-role-to-user admin system:serviceaccount:ml-workshop:jenkins-ml-jenkins -n user$i-project
done
oc adm policy add-cluster-role-to-user cluster-admin user29
```
Note 
- **this will invalidate any other logins like opentlc-mgr** - so I added admin access for one of my users, user29.

If you need to create users with different credentials consult [this blog](https://medium.com/kubelancer-private-limited/create-users-on-openshift-4-dc5cfdf85661) - on which these instructions are based.


--------------------------------------------------------------------------------------------------------


# Updating Tool URLs
As mentioned above, if you are running this as a workshop, it is recommended you fork this repo.  The reason is, after you install the tools, your OpenShift Service IP addresses for various tools will be different for each installation. It is recommended for simplicity, that you update yours with your cluster's values, so your students don't have to.
If you are forking the repo, you'll need to update the docs (all .md files in this directory) and replace all instances of https://github.com/masoodfaisal/ml-workshop with https://github.com/**YOUR_REPO**/ml-workshop

You need to find **your** IP addresses for  
a) the Minio object storage Service which we'll refer to as MINIO_ADDRESS, and 

b) the Verta.ai model repository Service which we'll refer to as VERTA_ADDRESS.

MINIO_ADDRESS and VERTA_ADDRESS are retrieved by navigating to Networking -> Services and locate the IP of their respective Services (verta being named _ml-modeldb-webapp_):
![](https://github.com/masoodfaisal/ml-workshop/blob/main/docs/images/38-service_ips.png)

MINIO_ADDRESS uses port 9000 and needs to be substituted in one file */notebook/Merge_Data.ipynb*. Open that file and search for _:9000_. Replace that with your MINIO_ADDRESS.

VERTA_ADDRESS uses port 3000 needs to be substituted in two files */notebook/Model_Experiments.ipynb* and */notebook/Train_Model.ipynb*. Open each of those files and search for _:3000_. Replace that value in each file with your VERTA_ADDRESS.

Save each of the three files and commit to your fork of this repository.


--------------------------------------------------------------------------------------------------------

## Configure the S3 Storage

### Download the Files Used For This Setup

<span style="color:yellow">*REVISIT: Insert the instructions for downloading the files that will be uploaded below.*</span>

### Configure Upload Files to the rawdata Bucket

1. Open the OpenShift console in your browser.
2. Click: **Networking > Routes**

![](./images/openshift-routes.png)

3. Scroll down to find *minio-ml-workshop-ui*. 
4. Click the Minio url under **Location** heading

OpenShift opens a new browser tab and launches the Minio console and diaplays the login screen.

![](./images/minio-1.png)

5. Enter the following credentials:
* Username: **minio**
* Password: **minio123**
6. Click **Login**

Minio displays the main console and all of the existing S3 buckets.

![](./images/minio-2.png)

7. Scroll down to find the *Raw Data* bucket.
8. Click **Browse**.

Minio displays the bucket contents.

You will now upload two folders (*customers* and *products*) to the *rawdata* bucket.

### Upload the *customers* data

9. Click: **Upload Files > Upload Folder**

Minio prompts for the folder to upload.

10. Navigate to the *customers* folder you extracted earlier. 
11. Click: **Upload**.

Minio uploads the folder and all file contents to the *raw data* S3 bucket.

### Upload the *products* data

12. Click: **Upload Files > Upload Folder**

Minio prompts for the folder to upload.

13. Navigate to the *products* folder you extracted earlier. 
14. Click: **Upload**.

Minio uploads the folder and all file contents to the *raw data* S3 bucket.

The result should look like the following figure:

![](./images/minio-3.png)

### Change the *model* Bucket's Permissions

15. Click **Buckets** in the Minio console pane.
16. Scroll down to locate the **models** bucket.
17. Click **Manage**

Minio displays a configuration screen for the **models** bucket

![](./images/minio-4.png)

18. Click the **Edit** icon setting under **Accesses Policy**

Minio displays **Change Access Policy** dialog box.

![](./images/minio-5.png)

19. Change this setting to **Public**.
20. Click **Set**.

The updated configuration is displayed.

![](./images/minio-6.png)

--------------------------------------------------------------------------------------------------------

## Configure Superset

Now you need to set up Superset to talk to our S3 and Kafka raw data via Trino - exposing the data via SQL.

1. Open the OpenShift console in your browser tab.

![](./images/openshift-routes.png)

2. Click the url for *superset*

OpenShift opens a new browser tab and displays the Superset login page.

![](./images/superset-1.png)

5. Enter the following credentials:
* Username: **admin**
* Password: **admin**
6. Click **SIGN IN**

Superset diaplays the main console.

![](./images/superset-2.png)

7. Click: **Data > Databases**

Superset displays a list of configured databases.

![](./images/superset-3.png)

8. Click: the **"+ DATABASE"** button

Superset prompts for the database connection details

![](./images/superset-4.png)

9. Click the **Supported Databases** drop-down list
10. Scroll down to the entry **Trino** and click it.
11. Copy and paste the following text into the **SQL Alchemy URI** text box:
```
trino://admin@trino-service:8080
```
12. Click **Test Connection**.

If all steps have been performed correctly, Superset displays the message **Connection looks good!**.

![](./images/superset-5.png)

13. Click the **Advanced** tab in the **Edit Database** form.

Superset prompts for the advanced database configuration.

![](./images/superset-6.png)

14. Click **SQL Lab**.
15. Complete the form as illustrated in the following figure:
![](./images/superset-7.png)
16. Click **Finish**

17. Click **SQL Lab Settings** in the main toolbar.
18. Click **Saved Queries**.

![](./images/superset-8.png)

19. Click the **+ QUERY** button.

<span style="color:yellow">*NOTE: **DO NOT SAVE THE QUERY**. We don't save this as it only needs to be run once per workshop*</span>

20. Copy and paste the query editor.

```
CREATE TABLE hive.default.customer1 (
  customerId varchar,
  gender varchar,
  seniorCitizen varchar,
  partner varchar,
  dependents varchar,
  tenure varchar
)
WITH (format = 'CSV',
  skip_header_line_count = 1,
  EXTERNAL_LOCATION='s3a://rawdata/'
)
```

<span style="color:yellow">REVISIT: Cannot complete writing these steps in the current environment. Come back and complete these...</span>

21. Click **Run**.

Superset displays *Result - true* as shown. 
![](./images/40-superset-saved-queries-3-run-createtable.png)

22. Replace the CREATE TABLE with
```
SELECT kafkaData.*, s3Data.*  
from customerchurn.default.data kafkaData,
 	hive.default.customer1 s3Data
where cast(kafkaData.customerId as VARCHAR) = s3Data.customerId
```
Run the query as shown. You should see a resultset spaning personal and product consumption customer data. 
![](./images/40-superset-saved-queries-3-run-joinedquery.png)

Click Save AS - naming the query **Kafka-CSV-Join**

We're now done with setup!
