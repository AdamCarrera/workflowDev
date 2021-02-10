# workflowDev

Welcome to our new repository, this readme file will talk you through our new workflow.

**This is a work in progress**

# Github Workflow

## Getting Setup in Pycharm

1. Close the previous project (scan_tank) with File > Close Project
2. On the welcome screen, click "Get from VCS"
3. Log into Github, and download git if you see the prompt
4. Click on your github account, choose this repository and click clone
5. The project has been cloned onto your machine! Finally, configure your interpreter so that Pycharm uses our anaconda environments.

## Feature Development

1. When you are ready to develop a feature, open the repository on Github.com
2. Find the branch drop down menu
3. Type the name of your branch and click create branch, it should say that you are branching from the master branch
4. The branch has been created in the origin, the team can see your branch but in order to begin development you must check out the branch locally
5. In Pycharm, update the project with the blue arrow
6. In the bottom right, click on the branch menu, you should see your new branch as "origin/yourbranchname" under remote branches
7. Click on your remote branch and then click checkout

## Pull Requests

Your new feature is tested and stable, now it's time to merge your branch with the master branch!

1. On Github.com click on Pull Requests
2. There are two dropdown menus, one called "base" and one called "compare"
3. Select the master branch in the base menu and your branch in the compare menu, click "Create Pull Request", regardless of whether there are merge conflicts
4. Write a good title, and a short summary of what you will be adding/changing
5. When you are done, click create pull request again and notify the team

### Code Reviews

Part of this workflow includes code reviews. You must obtain one approving code review from one of your teammates before your code can be merged into the master branch. **Github will not let you merge without one.** This allows us to double check our code, and ensures that at least two people know what is happening with each change.

You can request a code review by clicking on the gear next to reviewers, this will let you type in your desired teammates username to request a review from them.

### Writing a Review

1. Open your teammates pull request, you can start a review by adding a comment to a specific line or by clicking on Start Review.
2. Look over what your teammate is changing. Add comments and constructive feedback where it is needed.
3. If everything looks good and github is able to merge the branches automatically, click on the review changes button, write a short summary and tick one of the three options below
    * Comment - Submits general feedback without explicit approval
    * Approve - Submits feedback with the approval to merge changes
    * Request - Submits feedback that must be addressed before merging
    
### Testing Code

We are able to test changes and resolve conflicts locally before merging our changes on the website.

A PR is a request for the branch to be merged, you can still work on your branch and push changes to the origin, those changes will show up in your pull request!

This allows you to
   * Make requested changes
   * Merge your local feature branch with your local master branch and test your code without worry

#### Merging Locally

1. Checkout your feature branch in Pycharm and make sure that your local master branch is up to date
2. Click on Git > Merge..., select master. This merges the local master branch into your local feature branch. This may sound backwards, but keep in mind the PR exists on your feature branch, not the master. The master branch cannot be pushed to directly, so if you merge your local feature branch into your local master branch you will be stuck
3. When the conflicts window opens, click on Merge
4. Examine and resolve each conflict. Sometimes you may want your changes, their changes, or both.
5. When the conflicts are resolved, you can test our your merged code and see how it runs
6. If something is wrong, you can always start over by deleting both local branches and checking them out again. This will bring you back to step 1
7. When you are satisfied with your merged code, push your changes to your feature branch in the origin! They will be reflected in the PR, and the reviewer will be able to see your merged code
