
#Dump a python list into an SQL table with a single column
def ListToSqlColumn(cur, tableName, varlist):
    var_string = ','.join(['(?)'] * len(varlist))  #Create string of size N like this: "(?), (?), (?), (?)"
    query_string = 'INSERT INTO %s VALUES %s;' % (tableName, var_string)
    cur.execute(query_string, varlist)