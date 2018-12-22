import datetime, re
from django.db.models import Q

# tokenize the input string and return two list, one that start with (-) and one that not
def get_tokenize(query_string):
    # Regex to split on double-quotes, single-quotes, and continuous non-whitespace characters.
    split_pattern = re.compile('("[^"]+"|\'[^\']+\'|\S+)')
    
    # Pattern to remove more than one inter white-spaces and more than one "-"
    space_cleanup_pattern = re.compile('[\s]{2,}')
    dash_cleanup_pattern = re.compile('^[-]{2,}')
    
    # Return the list of keywords.
    keywords = [dash_cleanup_pattern.sub('-', space_cleanup_pattern.sub(' ', t.strip(' "\''))) \
                    for t in split_pattern.findall(query_string) \
                        if len(t.strip(' "\'')) > 0]
    include = [ word for word in keywords if not word.startswith('-')]
    exclude = [ word.lstrip('-') for word in keywords if word.startswith('-')]
    return include, exclude

# builds a query for included terms in a text search 
def get_query_includes(tokenized_terms, search_fields):
    query = None
    for term in tokenized_terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

# builds a query for excluded terms in a text search 
def get_query_excludes(tokenized_terms, search_fields):
    query = None
    for term in tokenized_terms:
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query | or_query
    return query

# builds a query for both included & excluded terms in a text search 
def get_query(query_string, search_fields):
    include_terms, exclude_terms = get_tokenize(query_string)
    include_q = get_query_includes(include_terms, search_fields)
    exclude_q = get_query_excludes(exclude_terms, search_fields)
    query = None
    if include_q and exclude_q:
        query = include_q & ~exclude_q
    elif not exclude_q:
        query = include_q
    else:
        query = ~exclude_q
    return query

# query against user last update
def get_date_query(update=0):
    query = None
    update = get_integer(update)
    if update:
        update = (datetime.date.today() - datetime.timedelta(update))
        query = Q(**{"userprofile__updated_at__gte": update.isoformat()})
    return query

# query for not null and not black fields
def get_not_null_and_not_blank_query(field=None):
    if not field:
        return field
    null_q = Q(**{"%s__isnull" % field: True})
    empty_q = Q(**{field: ''})
    return ~ (null_q | empty_q)

# query to ensure profile has been filled in
def get_completed_profile_query():
    return Q(**{"userprofile__filled_in": True})
  
# unicode to integer
def get_integer(value='0'):
    try:
        return int(value)
    except:
        return 0

