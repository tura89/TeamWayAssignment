<h2>TeamWay assignment:</h2>

```commandline
Build a REST application from scratch that could serve as a work planning service.


Business requirements:

    A worker has shifts
    A shift is 8 hours long
    A worker never has two shifts on the same day
    It is a 24 hour timetable 0-8, 8-16, 16-24


Preferably write a couple of units tests.
```

<h3>To run the server:</h3>

1. Clone the repository
2. Docker should be installed
3. from `/TeamWayAssignment` folder:

```console
$ sudo docker build -t python-django-app .

$ sudo docker run -it -p 8000:8000 python-django-app
```

The api can now be accessed at http://localhost:8000/api/shifts/

To log in, use `alex` as both username and passsword

The list of all endpoints is available at http://localhost:8000/api/

1. api/shifts - lists all shifts in chronological dates. New shifts can be added at this endpoint.
2. api/shifts/\<int:pk\> - specific shift, where \<int:pk\> is its id. It can be modified or deleted at this endpoint.
3. api/workers - lists all workers. New workers can be added at this endpoint.
4. api/workers/\<int:pk\> - specific worker, where \<int:pk\> is its id. It can be modified or deleted at this endpoint. 
5. api/workers/\<int:pk\>/shifts - Same functionality as api/shifts, except shifts are limited to those belonging to worker with the specified id.

<h3> Testing </h3>

To get container name:
```console
 $ docker ps
```
```console
 $ docker exec -it <container_name> /bin/bash 
```
In docker
```commandline
:/code#  python shifts_manager/manage.py test apimanager
```