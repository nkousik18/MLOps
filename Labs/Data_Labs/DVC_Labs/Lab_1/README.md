## Data Version Control (DVC)

- [DVC](https://dvc.org/) is an open-source tool that serves as a powerful asset in the machine learning project toolkit, with a primary focus on data versioning.
- **Data versioning** is a critical aspect of any ML project. It allows you to track changes and updates in your datasets over time, ensuring you can always recreate, compare, and reference specific dataset versions used in your experiments.
- In this lab tutorial, we will be utilizing DVC with Google Cloud Storage to enhance data versioning capabilities, ensuring efficient data management and collaboration within your machine learning project.
### Creating a Google Cloud Storage Bucket
1. Navigate to [Google Cloud Console](https://console.cloud.google.com/).
2. Ensure you've created a new project specifically for this lab.
3. In the Navigation menu, select "Cloud Storage," then go to "Buckets," and click on "Create a new bucket."
4. Assign a unique name to your bucket.
5. Select the region as `us-east1`
6. Proceed by clicking "Continue" until your new bucket is successfully created.
7. Once the bucket is created, we need to get the credentials to connect the GCP remote to the project. Go to the `IAM & Admin` service and go to `Service Accounts` in the left sidebar.
8. Click the `Create Service Account` button to create a new service account that you'll use to connect to the DVC project in a bit. Now you can add the name and ID for this service account and keep all the default settings. We've chosen `mlops_dvc_labs_1` for the name. Click `Create and Continue` and it will show the permissions settings. Select `Owner` in the dropdown and click `Continue`.
9. Then add your user to have access to the service account and click `Done`. Finally, you'll be redirected to the `Service accounts` page. You’ll see your service account and you’ll be able to click on `Actions` and go to where you `Manage keys` for this service account. 
10. Once you’ve been redirected, click the `Add Key` button and this will bring up the credentials you need to authenticate your GCP account with your project. Proceed by downloading the credentials in JSON format and securely store the file. This file will serve as the authentication mechanism for DVC when connecting to Google Cloud.
### Installing DVC with Google Cloud Support
- Ensure you have DVC with Google Cloud support installed on your system by using the following command:
	`pip install dvc[gs]`
- Note that, depending on your chosen [remote storage](https://dvc.org/doc/user-guide/data-management/remote-storage), you may need to install optional dependencies such as `[s3]`, `[azure]`, `[gdrive]`, `[gs]`, `[oss]`, `[ssh]`. To include all optional dependencies, use `[all]`.
- Run this command to setup google cloud bucket as your storage `dvc remote add -d myremote gs://<mybucket>`
- In order for DVC to be able to push and pull data from the remote, you need to have valid GCP credentials.
- Run the following command for authentication `dvc remote modify --mlops_dvc_labs_1 credentialpath <YOUR JSON TOKEN LOCATION>`
### Tracking Data with DVC
- Ensure you have downloaded the [required data](https://www.kaggle.com/datasets/yasserh/wine-quality-dataset) and placed it in the "data" folder, renaming the file to "winewuality_red.csv"
- To initiate data tracking, execute the following steps:
	1. Run the `dvc init` command to initialize DVC for your project. This will generate a `.dvc` file that stores metadata and configuration details. Your `.dvc` file config metadata will look something like this
	```
    [core]
    no_scm = True
    analytics = false
    remote = myremote
	['remote "myremote"']
    url = gs://mlops_dvc_labs_1
	```

	dvc remote modify --git-action-gcp credentialpath git-action-gcp git-action-gcp-3e47dbac54ff.json 
	2. Next, use `dvc add data/wineQuality_red.csv` to instruct DVC to start tracking this specific dataset.
	3. To ensure version control, add the generated `.dvc` file to your Git repository with `git add data/wineQuality_red.csv`.
	4. Also, include the `.gitignore` file located in the "data" folder in your Git repository by running `git add data/.gitignore`.
	5. To complete the process, commit these changes with Git to record the dataset tracking configuration.

- To push your data to the remote storage in Google Cloud, use the following DVC command: `dvc push` This command will upload your data to the Google Cloud Storage bucket specified in your DVC configuration, making it accessible and versioned in the cloud.

### Handling Data Changes and Hash Updates
Whenever your dataset undergoes changes, DVC will automatically compute a new hash for the updated file. Here's how the process works:
- **Update the Dataset:** modify the existing data/winequality-red.csv file or make changes to your transformation script, such as adding new computed columns or adjusting thresholds.
  ```
  python scripts/modify_wine.py
  ```
- **Update DVC Tracking:** Execute `dvc add data/winequality-red-modified.csv`
-  DVC will compute a new hash for the modified file.
Since the data changed, this hash will differ from the previous one, signaling an updated version of the dataset.
- **Commit and Push:** Commit the changes with Git and push them to your Git repository. This records the update to the dataset, including the new hash.
```
git add data/winequality-red-modified.csv.dvc .gitignore scripts/modify_wine.py
git commit -m "Updated wine dataset and transformation script"
git push

```
- **Storage in Google Cloud:** When you run dvc push, DVC uploads the updated dataset to the Google Cloud Storage bucket specified in your DVC configuration. Each version of the dataset is stored as a distinct object within the bucket, organized for easy retrieval.
#### Reverting to Previous Versions with Hashes
To revert to a previous dataset version:
- **Checkout Git Commit:** Use Git to checkout the specific commit where the desired dataset version was last committed. For example, run `git checkout <commit-hash>`
- **Use DVC:** After checking out the Git commit, use DVC to retrieve the dataset version corresponding to that commit by running `dvc checkout`. DVC uses the stored hash to identify and fetch the correct dataset version associated with that commit.

> 💡You can follow [this](https://www.youtube.com/watch?v=kLKBcPonMYw&list=PL7WG7YrwYcnDb0qdPl9-KEStsL-3oaEjg&pp=iAQB) tutorial to learn about DVC in detail.
