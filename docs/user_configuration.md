Django have built-in support for managing access to pages and makes it possible to have different access levels of users, please read more are [django's homepage](https://docs.djangoproject.com/en/3.2/topics/auth/default/)

We recommend that you set up at least two groups, admin and flowcell. Where admin can: 

- change/add users and flowcells
- delete uploaded flowcells.

| Name | Permission | Description |
| :--- | :--- | : --- |
| admin | <ul><li>auth &#124; user &#124; Can add user</li><li>auth &#124; user &#124; Can change user</li><li>auth &#124; user &#124; Can view user</li></ul> | Users belonging to this group have the ability <br /> to add, change and view users |
| flowcell | <ul><li>dataprocessor &#124; flowcell &#124; Can delete flowcell</li><li> dataprocessor &#124; flowcell &#124; Can view flowcell </li><li> dataprocessor &#124; samples run data &#124; Can<br />delete samples run data </li><li> dataprocessor &#124; batch run &#124; Can delete <br /> batch run </li></ul> | Users belonging to this group have the<br />ability to delete flowcells and the<br />information bound to the flowcell. |

** Note ** that the super user, created by running `python3 manage.py createsuperuser`, have access to everything and can do whatever he/she wants.