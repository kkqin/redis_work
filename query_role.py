import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password='', socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

cur = 0
pass_one = 1

data = []
while (cur or pass_one):
    pass_one = 0

    lua = """
            local res = {} 
            res = redis.call('SCAN', ARGV[1], 'match', KEYS[1], 'COUNT', 10) 
            return res 
        """
    
    script = r.register_script(lua)
    k = "role:*:info"
    res = script(keys=[k], args=[cur]) 
    cur = int(res[0])
    if (len(res[1])):
        for it in res[1]:
            data.append(it)

print(data)
