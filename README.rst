Data Analyst bot
===============================

A Virtual Assistant created with flask and flask-assistant

Setup
-----

API.AI and Server Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1. Create a new Agent within the `API.AI Console_`
2. Click "Fullfillment" left side menu and enable webhook
3. With `ngrok`_ installed:

    .. code-block:: bash
    
        ./ngrok http 5000

3. Copy the **Forwarding https** url and paste it as the webhook URL in the "Fullfillment" menu

Project Environment
^^^^^^^^^^^^^^^^^^^

 It is recommended to use a virtual environment


1. Clone and move into project directory

    .. code-block:: bash
    
        git clone https://github.com/treethought/robo-analyst
        cd Data Analyst bot

    
2. Within the `API.AI Console_`, click the "gear" icon next to the API.AI agent name.
3. Locate the Client and Developer access tokens under `API keys`

4. Set the Client and Developer Access token environment variables
    
    .. code-block:: bash
    
        export CLIENT_ACCESS_TOKEN='YOUR CLIENT ACCESS TOKEN'
        export DEV_ACCESS_TOKEN='YOUR DEVELOPER ACCESS TOKEN'

    
5. Set the ``FLASK_APP`` and ``FLASK_DEBUG`` environment variables

    .. code-block:: bash
    
        export FLASK_APP=autoapp.py
        export FLASK_DEBUG=1


6. Install requirements
   
   .. code-block:: bash
   
        pip install -r requirements.txt


Development
-----------

Register Assistant Schema with API.AI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First update the `templates/` directory as needed and then run

.. code-block:: bash

    schema assistant/webhook.py

Running the Flask App
^^^^^^^^^^^^^^^^^^^^^
    
    .. code-block:: bash

        flask run



Testing the Assistant from the Command Line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To quickly send queries to your agent and view the responses:

    .. code-block:: bash
    
        query assistant/webhook.py


Deployment
----------

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.

Heroku
^^^^^^

Create Heroku app

    .. code-block:: bash
    
        heroku create robo-analyst
        git remote add stage git@heroku.com:robo-analyst.git

Configure Heroku app

    .. code-block:: bash
    
        heroku config:set CLIENT_ACCESS_TOKEN='YOUR CLIENT ACCESS TOKEN' -r stage

Deploy

    Commit and push changes

    .. code-block:: bash


        git push stage master





.. _`API.AI Console`: https://console.api.ai/api-client/#/login
.. _`ngrok`: https://ngrok.com/