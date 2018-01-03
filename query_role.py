import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=123456, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

lua = """
        local cur = 0 
        local res = {} 
        local need = {} 
        repeat res = redis.call('SCAN', cur, 'match', KEYS[1], 'COUNT', 10) 
        
        cur = tonumber(res[1]) 
        
        if next(res[2]) ~= nil then 
            for i, v in ipairs(res[2]) do
                table.insert(need , v) 
            end
        end
        until cur == 0 
        
        return need 
    """

script = r.register_script(lua)
k = "role:*:info"
res = script(keys=[k], args=[]) 
print(res)
print("room:*:info size is: %d." % ( len(res) ) )

