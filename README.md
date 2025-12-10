## EcoGuardMonitor 
It is a modern, web-based environmental monitoring application designed to track, analyze, and report pollution levels in real time. The system helps individuals, communities, and environmental agencies monitor air quality and take proactive measures toward a healthier environment.
## authentication and user roles
User login/logout system

Admin-only user registration

Three user roles:

Admin – Full access, manages users and system settings

Agent – Adds/edits/deletes pollution readings

Viewer – Read-only access for dashboards and reports
## tools of use
- django
- python libraries(ready made snippets)
 - pillow
  - cloudinary: media storage,url access
  - python-decouple : media tasks
## apps in the project
- accounts : authentication and authorization(Signup (registration)
,Login
Logout,
Forgot password / Reset password
Role-based authorization (Admin vs Regular User))
- media_assets : uploads images,crud operations
## steps
- install the libraries
pip install -r requirements.txt
- creation of app
- configuration of the project settings ,,register (apps,cloudinary)

# authentication and authorization(accounts.py)
- identity identification
-access priviledges
1. creation af the user model,,,models.py
2. Extend the integrated form captures,,,forms.py
3. create the views action for registration and login, logout and profile views,custompasswordresetview,custompasswordresetconfirmview , --> views.py
4. registration of the views action as url route - url.py
5. admin models registration
6. registration of the apps urls to the project urls
7. creation of the templates folder
8. make migrations


 ## template creation
 1. configuration level
  - blocks definition
  - linking to css,bootstrap
  - linking to js files
  2. creation of other pages by extending the base.html
  ## model views template


  ## media asset app views
  '''
1. Dashboard View : this allows my users to see uploaded items set as public
2. My media view: this allows my users to see their uploaded items
3. upload media view: this allows my users to upload new media items
4. Edit media view: this allows my users to edit their uploaded media items
5. Delete media view: this allows my users to delete their uploaded media items
6. Media detail view: this allows my users to view details of a specific media item  
'''
1. create a .env file for development purposes - store your info as variable references
2. create a .gitignore file for push purposes - include .env as one of the ignored files
 This abstracts  sensitive info from the main application code

 ## MPESA INTEGRATION
 1. Created a separate app that will contain our mpesa integration procedures
 2. create a model , transactions model
 3. settings.py project - configure the needed environmental credentials
  
