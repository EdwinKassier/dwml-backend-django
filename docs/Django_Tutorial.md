## Django Tutorial

### *Edwin Kassier*


---


## Introduction

Django is best described as the python web framework that comes with "batteries included". Where Flask and Fast API give you more freedom to build how you see fit, DJango is more rigid in its structure. This isn't a bad thing necessarily, but it does require you to learn the ins and outs of the framework before you can get up and running. Learning Django is worthwhile for two reasons: 1, it might not make sense at the time, but it is forcing you to conform to alot of best practices and 2, its age and reliability means that many larger tech firms will be using DJango if they are primarily working in python on the backend. Therefore learning Django is a wise move if you want to become a better developer and increase your employability, if you are just trying to achieve a simple task the learning curve may be difficult for you.


## An overview of Django

As mentioned, Django is set up to build a scalable web framework conforming to many best practices right out of the box. For example, in Flask we would need to set up the blueprint design pattern ourselves as an optional step, Django forces you to confirm to this design pattern. Meaning we immediately have a backend set up to handle partitioned routes, this is great for future scaling of the backend to handle specific routes related to certain types of tasks.

This is by design as Django needs to accommodate its built in admin functions routes using its standard `admin/` blueprint.

Django's admin functions handle the routes necessary to handle things like admin access, database access and viewing/manipulating the tables in your database.

While there are routes related to specific admin functions in a UI interface, the more mundane tasks for working with the framework, such as starting the server or working with some of the basic DB functions like migrations are handled through the provided `manage.py` command lime utility

For example, you can start the server by running `python manage.py runserver`, manage.py acts as your portal to interacting with the framework when performing system level operations

Another important command to remember is the two most used migrations commands: `python manage.py makemigrations` to scan through your current models and generate the code necessary to update your Database where necessary and then `python manage.py migrate` to run those migrations to update the structure of your Database tables. This could be something like adding or updating columns within a table. All of Djangos DB actions are assuming you are using SQL based database.

Speaking of databases, how does Django handle its data? Django assumes your database is in a SQL format (SQlite, PostgreSQL etc.) and has built its own ORM (Object Relationship Management) system using the `models.py` class which I mentioned briefly above. The purpose of an ORM system is to abstract away the need to handle raw SQL and instead deal with data in a class representation instead. Say for example you want to handle data relating to specific user, instead of having to use `SELECT * FROM USERS WHERE X == Y`, you can query that table via a command like `USERS.objects.get(X=Y)`. This is a simplified example, but you can see how abstracting away the complexity of SQL will improve your development velocity, not having to deal with the nitty gritty of the database.

To make this process even more user friendly I have found the use of serializers to be very helpful. A serializer in the context of Django models is a layer of code that can take the output of a query like `USERS.objects.get(X=Y)` and transform it into a native python datatype, such as a dictionary, that we can more easily work with.


For your enrichment, for python environments where you don't have Django's built in models system, you can use a library called [SQL Alchemy](https://www.example.com) to achieve a very similar result


Finally is the question of how routes in a Django api are handled. Django at its baseline is built to be a catch-all web server that can perform business logic, compose that output into an HTML view (called templates) and then return that response to the frontend to be rendered. Using Django as a pure RESTful API was a seemingly later addition. However, we can turn Django into a RESTful api using the popular `djangorestframework` library. 

Using this library, much like Django has its `views.py` and `urls.py` files, we can set up `api_urls.py` and `api_views.py` files that follow the same structure. Setting up the publicly accessible urls in `api_urls.py` and then linking them to the business logic needed to provide a response in the `api_views.py` file. Then when the urls are registered in the base instance we can set out a prefix for the partition using `path('api/v1/', include("api.api_urls"))`.

Now when you start the api all of your routes will be available to you.


## FAQs

### Why do we register models with the admin system?

This is so that you will be able to interact with those tables directly using the admin UI as well as making the tables visible to the system processes when doing migrations






