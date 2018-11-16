# Variable Modification Guide

This document contains instructions for modifying variables for Abercrombie.com and Hollister.com pipeline-managed environments.

The guide assumes that the reader has setup their access to Github, and has proper read/write access to the 'akamai-build-pipeline' Abercrombie project (this project).

To obtain proper access, contact the project administrator.

To setup your local environment so that you can pull/modify/push variable artifacts, read the following document:

[Adding an SSH Key to your Github account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)


## Overview

The ANF automated build and deployment pipeline has been implemented in a way that it ingests variable files from Github rather than Akamai Luna Property Manager.

In a nutshell, the ANF build process will pull variable JSON artifacts (stored within this project) into the pipeline and replace the variables within the 'anf-md-staging' JSON artifact. Essentially, a 'build' process overwrites the variables within the anf-md-staging JSON rule tree with the environment variable artifacts- creating an environment specific deployment artifact (templatized Akamai metadata + environment specific variables).

![build diagram](https://github.com/AbercrombieAndFitch/akamai-build-pipeline/blob/master/docs/diagrams/ANF_build_process.png "ANF-HOL Build Process")



## Process

This guide will cover two specific variable modification use cases

- Creating and initializing a new property manager variable
- Modifying the values of existing property manager variables

As stated previously, this guide assumes that the reader has proper access and has setup their Github account.  It also assumes that the reader has initially cloned the project to their local machine previously before following the steps below.

### Creating a new variable

When creating a new property manager variable, it is important to understand that variables created and initialized for ANF/HOL environments (ex: swing.abercrombie.com_pm) is performed differently than for the 'anf-md-staging' environment.

- *anf-md-staging*: create using the Luna Property Manager UI
- *ANF / HOL environments*: create by editing the raw JSON variable artifacts

Follow the steps as described below:

1. Create a new variable in anf-md-staging, using Luna property manager.

Provide the variable with a proper name, and initialized value (or no value, if necessary). In our case, we will be adding a variable 'PMUSER_FOO':

![PM Screenshot](https://github.com/AbercrombieAndFitch/akamai-build-pipeline/blob/master/docs/diagrams/PM_variable.jpg "Creating a variable in Property Manager")

2. Save the changes to 'anf-md-staging' in property manager.

3. Navigate to the working directory containing the 'akamai-build-pipeline' project, on your local machine.

In my case, this directory is in '/Users/dmcallis/workspace/akamai-build-pipeline'

```
atl-mp43o:~ dmcallis$ cd workspace/akamai-build-pipeline/
atl-mp43o:akamai-build-pipeline dmcallis$ pwd
/Users/dmcallis/workspace/akamai-build-pipeline
```

4. Pull the contents of the 'akamai-build-pipeline' into your local environment.

This is done by submitting the command 'git pull' in the working directory containing the 'akamai-build-pipeline' project:

```
atl-mp43o:akamai-build-pipeline dmcallis$ git pull
remote: Counting objects: 6, done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 6 (delta 3), reused 3 (delta 1), pack-reused 0
Unpacking objects: 100% (6/6), done.
From github.com:AbercrombieAndFitch/akamai-build-pipeline
   3da02f4..92f4ee9  master     -> origin/master
Merge made by the 'recursive' strategy.
 README.md | 121 ++++++--------------------------------------------------------
 build.sh  |  81 ++++++++++++++++++++++++++++++++++-------
 2 files changed, 80 insertions(+), 122 deletions(-)
```

Your output may not 100% reflect the above, depending on recent changes to the project.

5. Navigate to the './metadata/var' directory within the project.

You should see 6 variable artifacts:

```
atl-mp43o:akamai-build-pipeline dmcallis$ cd metadata/var/
atl-mp43o:var dmcallis$ ls -ltr
total 192
-rw-r--r--  1 dmcallis  600  14689 Mar 22 10:21 www-2.hollisterco.com_pm.var.json
-rwxr-xr-x  1 dmcallis  600  14727 Mar 22 10:21 www-2.abercrombie.com_pm.var.json
-rw-r--r--  1 dmcallis  600  14667 Mar 22 10:21 swing-2.hollisterco.com_pm.var.json
-rwxr-xr-x  1 dmcallis  600  14718 Mar 22 10:21 swing-2.abercrombie.com_pm.var.json
-rw-r--r--  1 dmcallis  600  14666 Mar 22 10:21 cert-2.hollisterco.com_pm.var.json
-rwxr-xr-x  1 dmcallis  600  14719 Mar 22 10:21 cert-2.abercrombie.com_pm.var.json
```

6. Using a text editor (vi, etc), create an entry for the new variable within each artifact

```json
    {
        "value": "",
        "description": "",
        "name": "PMUSER_URL_COUNTRY",
        "sensitive": false,
        "hidden": false
    },
    {
        "name": "PMUSER_OMNI_EU_PATH",
        "description": "If paths fall under Omni EU condition, use this variable",
        "hidden": false,
        "sensitive": false,
        "value": "FALSE"
    },
    {
        "name": "PMUSER_FOO",
        "description": "Example for README",
        "hidden": false,
        "sensitive": false,
        "value": "BAR"
    }
]
```

NOTE: Do not forget to ensure the entry is properly indented, and a comma is added after the terminating bracket '}' from the previous entry! Failure to do so will result in the variable validation step to fail, breaking the pipeline sequence (for good reason, the JSON is invalid!).

7. Add the changes to the project using 'git add (FILE)'

Check the status of your changes using 'git status'

```
atl-mp43o:akamai-build-pipeline dmcallis$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	modified:   metadata/var/www-2.abercrombie.com_pm.var.json
```

Add the file using 'git add'

```
atl-mp43o:akamai-build-pipeline dmcallis$ git add metadata/var/www-2.abercrombie.com_pm.var.json
atl-mp43o:akamai-build-pipeline dmcallis$
```

Re-check the status, it should be listed as tracked and highlighted green.

```
atl-mp43o:akamai-build-pipeline dmcallis$ git status
On branch master
Your branch is up-to-date with 'origin/master'.
Changes to be committed:
  (use "git reset HEAD <file>..." to unstage)

	modified:   metadata/var/www-2.abercrombie.com_pm.var.json
```

Do this for every variable file you modify. In this example, I'm only adding an entry for ANF prod- depending on your specific requirements, you may need to add to all 6! Be mindful of the specific change you are implementing.

8. Commit your changes, include a message

```
atl-mp43o:akamai-build-pipeline dmcallis$ git commit -m 'Added variable FOO to ANF Prod'
[master 73935a9] Added variable FOO to ANF Prod
 3 files changed, 149 insertions(+), 3 deletions(-)
 create mode 100644 docs/diagrams/PM_variable.jpg
```

Ideally, you should include a link to the JIRA ticket for the requirement you are working on in your commit message.

9. Push the changes to the master branch of the project using 'git push origin master'

```
atl-mp43o:akamai-build-pipeline dmcallis$ git push origin master
Counting objects: 9, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 25.36 KiB | 6.34 MiB/s, done.
Total 9 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To github.com:AbercrombieAndFitch/akamai-build-pipeline.git
   bb0083c..73935a9  master -> master
```


### Modifying an existing variable value

Modifying an existing variable requires the same process as above, except the change implementer will simply change the 'value' field within the existing environment specific JSON file.

Simply follow steps 3 - 9 in the above process.

