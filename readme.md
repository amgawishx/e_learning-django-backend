  DBAPI Documentation 

*   [DBAPI Documentation](#dbapi-documentation)
    *   [Permissions](#permissions)
    *   [Syntax](#syntax)
    *   [Usage](#usage)
    *   [Response](#response)

DBAPI Documentation
===================

DBAPI is an API of the site _iCollege_ that’s mainly concerned with communication with the server’s database.

Permissions
-----------

The DBAPI usage is only viable via Ajax and inaccessible outside the client’s session and render Http404 if request submitted without viable session, and some advanced usages is only available for authenticated clients with different degrees of freedom depending on authentication level.

Syntax
------

For the usage of DBAPI, the following syntax is use:  
`[host]/dbapi/{handler}/{action}/{query}/`  
The `{query}` is expanded into the following at most:  
`{model}/{field}/{value}/{xkey}`  
Some handlers require all three, while others require only one, the `{model}`(which needs to be supplied to **ALL** handlers.)  
The `{action}`is the command executed by server to do some “action” on the data matching the `{query}` and it is specific for each handler, and some handlers have _none_.

Usage
-----

The API accepts GET, POST, PUT and DELETE HTTP requests which are supported Django REST framework, POST requests are used to create new values in the database, GET requests are used to retrieve information from the database, PUT requests used to update an existing values in the database while DELETE is used to remove data from the database.  
– GET handlers:

*   _fetch_: used to _retrieve_ data, actions:
    *   *   _all_: retrieve all data of _models_ from database, requires only _model_
    *   *   _filtered_: retrieve all data from database _matching_ the _query_, requires _full query_
    *   *   _single_: retrieve _single_ value from the database, requires _full query_
    *   if _xkey_ is supplied, the JSON response will carry only information of that field related to the item/s in the supplied query.
*   _searchsql_: used to directly execute SQL `SELECT` commands to the database, syntax: `{table}/{fields/separated/by/a/slash}/limiter/{limiter}/{condition}/`, for all data in table: `{table}/all/limiter/{limiter}/{condition}/` limiter option is optional,

– DELETE handler:

*   _lose_: used to _remove_ a full object from database, if you wish to only remove few fields of an object, use PUT handler with empty values.

– POST handler:

*   _lend_: used to create a new model in the database from form data, requires _model_, no actions.

– PUT handler:

*   _update_: used to update a model in the database from form data, requires _model_, no actions.

Response
--------

The DBAPI respond to _client_ only via _JSON objects_, in both scenarios of success and failure, the _JSON_ reponse has the following syntax:

    {
      'payload': [data...],
      'status': HTTP_STATUS_CODE (200,201,400, etc...)
    }
    

An example _JSON_ for a successful retrieval of data:

    {
      "payload": [
        {
          "id": 2,
          "last_login": "2020-03-23T03:18:23Z",
          "is_superuser": false,
          "username": "username1",
          "first_name": "Ahmed",
          "last_name": "Gawish",
          "email": "amgawish@student.aast.edu",
          "is_staff": true,
          "is_active": true,
          "date_joined": "2020-03-22T23:48:00Z",
          "email_status": true,
          "registration": 18102145,
          "university": "AASTMT",
          "college": "CET",
          "department": "CC",
          "semester": 1
        }
      ],
      "status": 200
    }
    

Some actions -although rarely- return only `"status"`, other actions on failure will return instead of `"payload"`.
