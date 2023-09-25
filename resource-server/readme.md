# Resource Server  

To run components, fill in ``config.py`` with your Autlete credenitals then:

* Install the requirements:
    * ``pip install requirements.txt``
* To run the resource server (i.e., the baseline API) on port 8080:
    * ``python3 resource_server.py``
* To run utAPIa proxy to enforce the policies on port 8000:
    * ``python3 proxy.py``

