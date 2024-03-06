# icon_tracker_parser
parser for transaction using icon tracker apis.

## Prerequisite

- python >= 3.11

## Installation

~~~
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt 
~~~

## Execution

~~~
$ python tx_counter.py
~~~

## Example
### Count of transactions at a date.

~~~
==========================================
[1] Count of transactions at a date.
[2] Count of transactions during a term.
[q] Quit
==========================================
Press key of menu: 1
==========================================
Enter information for transaction count.
tracker base url(DEFAULT:https://tracker.lisbon.icon.community): 
contract address(DEFAULT:cxdd0cb8465b15e2971272c1ecf05691198552f770): 2024-03-07
transaction method name(DEFAULT: create):
date for count(DEFAULT: today): 
###########################################
Request tx list ...
response.request.url=URL('https://tracker.lisbon.icon.community/...')
count=50
response.request.url=URL('https://tracker.lisbon.icon.community/...')
count=28
##########################################
date=2024-03-07, result=78
~~~

### Count of transactions during a term.
~~~
==========================================
[1] Count of transactions at a date.
[2] Count of transactions during a term.
[q] Quit
==========================================
Press key of menu: 2
==========================================
Enter information for transaction count.
tracker base url(DEFAULT:https://tracker.lisbon.icon.community): 
contract address(DEFAULT:cxdd0cb8465b15e2971272c1ecf05691198552f770): 
transaction method name(DEFAULT: create):
end date for count(DEFAULT: created date of contract): 20240301
###########################################
Request tx list ...
response.request.url=URL('https://tracker.lisbon.icon.community/...0')
skip=0, count_list=defaultdict(<class 'int'>, {'2024-03-07': 50})
response.request.url=URL('https://tracker.lisbon.icon.community/...100')
skip=100, count_list=defaultdict(<class 'int'>, {'2024-03-07': 40, '2024-03-06': 10})
response.request.url=URL('https://tracker.lisbon.icon.community/...200')
skip=200, count_list=defaultdict(<class 'int'>, {'2024-03-06': 50})
response.request.url=URL('https://tracker.lisbon.icon.community/...300')
skip=300, count_list=defaultdict(<class 'int'>, {'2024-03-06': 50})
response.request.url=URL('https://tracker.lisbon.icon.community/...400')
skip=400, count_list=defaultdict(<class 'int'>, {'2024-03-06': 50})
response.request.url=URL('https://tracker.lisbon.icon.community/...500')
...
##########################################
{
    "2024-03-07": 96,
    "2024-03-06": 186,
    "2024-03-05": 251,
    "2024-03-04": 253,
    "2024-03-03": 104,
    "2024-03-02": 108,
    "2024-03-01": 113
}
end_date=2024-03-01, total count=1111
~~~