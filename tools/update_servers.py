# When executed, this should check all the servers against the whitelist. It should add or remove depending on the whitelist. 


from voat_sql.utils.servers import ServerUtils


s = ServerUtils()

print(s.get_server('localhost:5001'))
