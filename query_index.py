import sys
import redis

assert(len(sys.argv) >= 2)
#print(type())

room_id = sys.argv[1]
print(room_id)
r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, password=123456, socket_timeout=None, connection_pool=None, charset='utf-8', errors='strict', unix_socket_path=None)

lua = """
        local cur = 0 
        local res = {} 
        local need = {} 
        repeat res = redis.call('HSCAN', KEYS[1], cur) cur = tonumber(res[1]) 
        if next(res) ~= nil then 
            table.insert(need, res[2]) 
        end
        until cur == 0 
        
        return need 
    """

script = r.register_script(lua)
k = "room.index:all"
res = script(keys=[k], args=[ sys.argv[1] ]) 

#for _id in res[0][0:]:
#    d = _id.decode("utf-8")
#    if d == room_id:
#        print(d)

res = res[0]
for _id in range(0, len(res)):
    d = res[_id].decode("utf-8")
    if d == room_id:
        print(res[_id - 1], d)

