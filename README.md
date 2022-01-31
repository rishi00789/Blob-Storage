# Blob-Storage



#Solution
-This project has been built with respect to the essential requirements of a BLOB storage system.
-Mainly used Flask for app routes such as login,signup,upload etc.
-Used SQLITE3 database to store the credentials as well as the files uploaded by each user.
-Hashed each password entry through SHA256 encryption.
-Error Handling is also taken care of i.e user enters invalid username or password,etc.
-Handeled Session management for each user to reduce traffic.

#Features
-Login/Signup:User create an account on the application and logs into the application using  valid username and password.
-Files:User can now view all the files he has access to and has uploaded.
-Upload:User can upload ant format file onto the storage system.
-Share:User can share their files with any valid user of the application.
-View/Download:User can view or Download the files onto their local system.
-Rename:User can rename files according to their choice.
-Delete:User can delete files according to their choice.
-Logout:User can successfully logout and the changes will be preserved on the storage system.


#Deployment 
-https://blob-file-storage.herokuapp.com/
