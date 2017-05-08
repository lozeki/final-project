Create the Project

1. Create a new repository on GitHub without README, license, or gitignore files by click on the new button on repositories tab.

2. Open Git Bash on your PC.

3. Create a folder on your PC for the project.

4. Initialize the local directory as a Git repository.

   $ git init

5. Create README.md file and add the file to your repository.
   
   $ echo "# final-project" >> README.md
   $ git add README.md

6. Commit it to your local repository.

   $ git commit -m "Create the repo for final project"

7. Connect your repo to github ( you can copy the remote repository URL from your github setup page).

   $ git remote add origin https://github.com/lozeki/final-project.git

8. Push the changes in your local repository to GitHub (you’ll have to type your github usename and password when you push to github).
   
   $ git push -u origin master







