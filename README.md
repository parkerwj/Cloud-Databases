# Overview

This project aims to further my learning on how to integrate a cloud database into a program. The software created is a photo editing database management program that allows photographers to add/update sessions, track the number of images edited, and calculate amounts due. The program is integrated with a Firebase Cloud Database to allow for easy access and sharing of data among different users.

[Software Demo Video](https://www.youtube.com/watch?v=EQ_h5ioNwu0)

# Cloud Database

The program uses a Firebase Cloud Database to store all data. The database has a collection called "photographers" which contains documents for each photographer. Each document has fields for the photographer's name, website, email, and their sessions. The sessions field is a subcollection that contains documents for each session with fields for session type, is_paid, session name, session date, delivered date, number of images, price per image, and return date.

# Development Environment

This program was developed using Python 3.11.5. The Firebase Python SDK was used to access the Cloud Database.

# Useful Websites

- [Firebase Docs](https://firebase.google.com/docs)
- [Python Docs](https://docs.python.org/3/)
- [PyCharm Docs](https://www.jetbrains.com/help/pycharm/)

# Future Work

- Add authentication for different users
- Implement a calendar feature to track session dates
- Improve user interface
- Allow for exporting/printing of data and reports