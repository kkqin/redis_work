import redis

r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=123456, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

lua = """
        local cur = 0 
        local res = {} 
        local need = {} 
        repeat res = redis.call('SSCAN', KEYS[1], cur, 'COUNT', 10) cur = tonumber(res[1]) 
        table.insert(need , res[2]) 
        until cur == 0 
        
        return need 
    """;

script = r.register_script(lua)
k = "role.room:all"
res = script(keys=[k], args = [] ) # is a list

def delete_room(room_id):
    """ func """
  
    id_ = room_id.decode("utf-8")
    k = "room:" + id_  + ":info"
    arg1 = id_

    lua2 = """
            redis.call('SREM', 'role.room:all', ARGV[1])
            redis.call('ZREM', 'room.book:start', ARGV[1])
            redis.call('ZREM', 'room.book:end', ARGV[1])
            redis.call('SADD', 'room_ids:all', ARGV[1])
            redis.call('DEL', KEYS[1])
            return true;
            """;
    
    script2 = r.register_script(lua2)
    script2(keys=[k], args = [arg1])

for room_id in res[0][0:-1]:
    delete_room(room_id)
