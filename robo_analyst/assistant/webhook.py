# -*- coding: utf-8 -*-

# robo_analyst
# By Cam <cpsweene@gmail.com>
#
# A Virtual Assistant created with flask and flask-assistant

import logging

from flask import Blueprint
from flask_assistant import Assistant, ask, tell, context_manager as manager, event
import arrow


blueprint = Blueprint('assist', __name__, url_prefix='/assist')
assist = Assistant(blueprint=blueprint)
logging.getLogger('flask_assistant').setLevel(logging.DEBUG)


@assist.action('Greetings')
def welcome():
    speech = """Hi! I'm robo analyst and I can help you learn more about the performance of your products.<br/><br/>

        With that said, do you want to know about <br/>
        a) sales
        b) quantity sold
        c) discounts
        d) refunds

    You can choose 1 or more of the metrics above if you like
    """
    return ask(speech)


@assist.action('SelectMetrics')
def set_metrics(metrics=[]):
    manager.add('metrics-complete')

    speech = """What time period would you like to see {} for? 
            (e.g. last 3 weeks, last 2 days, yesterday)""".format(metrics)
    manager.add('data', lifespan=15).set('metrics', metrics)  # context to hold all info
    return ask(speech)


##################
## Time Periods ##
##################

def parse_date_interval(date_time):
    start, end = date_time.split('/')
    try:
        delta = arrow.get(end) - arrow.get(start)

    except arrow.parser.ParserError:
        delta = arrow.get(end, 'HH:mm:ss') - arrow.get(start, 'HH:mm:ss')

    return delta


def largest_period(days):
    weeks = int(days // 7)
    if weeks > 4:
        return 'ask-bymonth'

    elif weeks > 0:
        return 'ask-byweek'

    elif days > 0:
        return 'ask-byday'

    else:  # catch all
        return 'ask-bymonth'


@assist.context('metrics-set')
@assist.action('SelectTimePeriod', mapping={'date_time': 'sys.date-time'})
def begin_time_dialogue(date_time):

    # interval
    if '/' in date_time:

        delta = parse_date_interval(date_time)
        manager.get('data').set('time-delta', str(delta))
        ask_period = largest_period(delta.days)

        manager.add(ask_period, lifespan=1)
        return event('StepToProducts')

    else:
        return ask("Sorry I cant do single dates yet. Is there a range of time you'd like to see?")


# Asking each question, each called as event dependent on context

@assist.context('ask-bymonth')
@assist.action('StepToProducts')
def ask_by_month():
    return ask('Would you like to see this info by month?')


@assist.context('ask-byweek')
@assist.action('StepToProducts')
def ask_by_week():
    return ask('Would you like to see this info by week?')


@assist.context('ask-byday')
@assist.action('StepToProducts')
def ask_by_day():
    return ask('Would you like to see this info by day?')


# Save answer and ask next time period - uses follow-up intents in API.AI

@assist.context('ask-bymonth')
@assist.action('StepToProducts - yes/no')
def store_answer(answer):
    manager.add('ask-byweek', lifespan=1)
    manager.get('data').set('bymonth', answer)
    return event('StepToProducts')


@assist.context('ask-byweek')
@assist.action('StepToProducts - yes/no')
def store_answer(answer):
    manager.add('ask-byday', lifespan=1)
    manager.get('data').set('byweek', answer)
    return event('StepToProducts')


@assist.context('ask-byday')
@assist.action('StepToProducts - yes/no')
def store_answer(answer):
    manager.add('time-periods-complete')  # always end with day
    manager.get('data').set('byday', answer)
    return event('AskProductScope')


#######################
## Product Selection ##
#######################

@assist.action('AskProductScope')
def ask_products():
    metrics = manager.get('data').get('metrics')
    speech = """Do you want to see {} for: <br/><br/>
                a) all the products <br/>
                b) just for certain products?""".format(metrics)

    return ask(speech)


@assist.action('AskProductScope - followup')
def action_func(scope):
    manager.get('data').set('product-scope', scope)
    manager.add(scope + '-products')

    if scope == 'all': # Products are selected - all of them
        manager.get('data').set('products', 'all')
        manager.add('products-selected')
        return event('SelectMeasureType')

    else: # need to choose the products, then select mesauretype
        return event('SelectProducts')

@assist.context('specific-products')
@assist.action('SelectProducts')
def action_func():
    speech = """If you know what products you would like to see let me know.<br/><br/>
                Or if you'd like me to list them out type 'list products'..."""
    return ask(speech)

@assist.context('specific-products')
@assist.action('SelectProducts - followup')
def action_func(products):
    manager.get('data').set('products', products)
    manager.add('products-selected')
    return event('SelectMeasureType')


@assist.context('stores-selected')
@assist.action('SelectMeasureType')
def action_func():
    # import ipdb; ipdb.set_trace()
    metrics = manager.get('data').get('metrics')
    speech = 'Would you like to see {} for each store or just the total?'.format(metrics)
    return ask(speech)

@assist.context('stores-selected')
@assist.action('SelectMeasureType - followup')
def action_func(measure_type):
    manager.get('data').set('product-measure', measure_type)
    return event('AskStoreScope')



# Event for listing products
@assist.action('ListProducts')
def action_func():
    speech = """Heres a list of your current products:<br/><br/>
                - p1
                - p2
                - p3
                - p4
                """
    return ask(speech)

# Event for listing stores
@assist.action('ListStores')
def action_func():
    speech = """Heres a list of your current stores:<br/><br/>
                - s1
                - s2
                - s3
                - s4
                """
    return ask(speech)



#####################
## Store Selection ##
#####################

@assist.action('AskStoreScope')
def action_func():
    speech = """Would you like to see the information for<br/><br/>
                a) all stores<br/>
                b) certain stores?
                """
    return ask(speech)


@assist.action('AskStoreScope - followup')
def action_func(scope):
    manager.get('data').set('store-scope', scope)
    manager.add(scope + '-stores')

    if scope == 'all': # stores are selected - all of them
        manager.get('data').set('stores', 'all')
        manager.add('stores-selected')
        return event('SelectMeasureType')

    else: # need to choose the stores, then select mesauretype
        return event('SelectStores')


@assist.context('specific-stores')
@assist.action('SelectStores')
def action_func():
    speech = """If you know what stores you would like to see let me know.<br/><br/>
                Or if you'd like me to list them out type 'list stores'..."""
    return ask(speech)

@assist.context('specific-stores')
@assist.action('SelectStores - followup')
def action_func(stores):
    manager.get('data').set('stores', stores)
    manager.add('stores-selected')
    return event('SelectMeasureType')



@assist.context('stores-selected')
@assist.action('SelectMeasureType')
def action_func():
    metrics = manager.get('data').get('metrics')
    speech = 'Would you like to see information for each store or do you just want the {} to represent all stores?'.format(metrics)
    return ask(speech)

@assist.context('stores-selected')
@assist.action('SelectMeasureType - followup')
def action_func(measure_type):
    manager.get('data').set('store-measure', measure_type)
    return event('AskSortType')



###############
## Sort Info ##
###############

#TODO IN STEP 5 -- SKIP FIRST "q".
# if more then one metric call event to select metric - > ask how to sort selected metric
# else ask how to sort selected metric

@assist.action('StartSort')
def action_func():
    metrics = manager.get('data').get('metrics')
    if len(metrics) > 1:
        return event('SelectMetricToSort')

    else:
        return event('AskSortType')
        speech = 'How would you like to sort {}? <br/> a) from largest to smallest b) from smallest to largest'.format(metrics[0])
        return ask(speech)

@assist.action('SelectMetricToSort')
def action_func():
    speech = "Which measure would you like to sort the information by? <br/> {}".format(metrics)
    return ask(speech)

@assist.action('SelectMetricToSort - followup')
def action_func(metrics):
    manager.get('data').set('sort-metric', metrics)
    return event('AskSortType')

@assist.action('AskSortType')
def action_func():
    metrics = manager.get('data').get('metrics')
    speech = 'How would you like to sort {}? <br/> a) from largest to smallest b) from smallest to largest'.format(metrics[0])
    return ask(speech)

@assist.action('AskSortType - followup')
def action_func(sort_type):

    data = manager.get('data')

    speech = 'Sorting with the following parameters:<br/><br/>'
    for k, v in data.parameters.items():
        speech += '{}: {}<br/>'.format(k, v)

    return tell(speech)





if __name__ == '__main__':
    app.run(debug=True)


