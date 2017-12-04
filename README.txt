—————————————
INTRODUCTION:
—————————————
PROJECT: Item Catalog

DESCRIPTION: Website for cataloging cars

AUTHORS: Steven Huynh


———————————————————————
OPERATING INSTRUCTIONS:
———————————————————————
1) Make sure you have the virtual machine environment set up.
  - Follow the link to help set up your VM if you haven't already:
    https://www.vagrantup.com/
2) Navigate to the vagrant directory in the terminal
3) Execute ‘vagrant up’ then ‘vagrant ssh’ in the terminal
4) Navigate to the vagrant folder within the virtual environment after logging in
5) Locate the 'catalog' folder and ensure the following most important files are there:
  - application.py
  - data.py
  - database_setup.py
6) Within your virtual machine, run 'data.py'
7) Afterwards, run 'application.py'
8) Your webpage should be up and running on your local machine!


—————————
CONTENTS:
—————————
- static
  - styles.css
- templates
  - deleteBrand.html
  - deleteModel.html
  - editModel.html
  - home.html
  - login_success.html
  - login.html
  - modelInfo_personal.html
  - modelInfo.html
  - models_personal.html
  - models.html
  - newModel.html
  - publicHome.html
  - publicModelInfo.html
  - publicModels.html
- application.py
- client_secrets.json
- data.db
- data.py
- database_setup.py
- database_setup.pyc
- README.txt
