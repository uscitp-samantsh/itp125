ITP 125: Introduction to Information Security -- Final Project -- Old Spice

This project was created for ITP 125: Introduction to Information Security at University of Southern California.

Summary

This command-line tool allows users to construct a voicemail (.mp3 file) using a set of options. The logic of this type of tool is very basic and intuitive. In order to create an .mp3 file from specified options, we need to (1) get user data concerning the voicemail, (2) retrieve only the necessary files from the internet, (3) construct the mp3 file and (4) cleanup any unneeded files. User-data is collected by a walkthrough method accessed by the --start option. The user is prompted for each option that goes into making the .mp3 file. Each option is checked for validity before constructing the .mp3 file.

File Retrieval

Though very straightforward, by recording which files the user will need from step 1, we can effectively download only the files we need form the internet in order to form the mp3 file.

MP3 Construction

Because different operating systems have different ways of creating mp3 files, the program first checks to see what type of operating system is running, then takes the downloaded files, combines them in the proper order, and finally writes them to the proper output file.

Clean-up

The application downloads several files from the internet, but we really don't want the user to retain these files. So instead, the program, using the proper commands for the corresponding operating system, removes those files from the system, to clean-up the location for the user.

Command Line

python final_project.py --start