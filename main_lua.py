from lupa import LuaRuntime

lua_code = '''\
function(N, i, total)
  local char, unpack = string.char, table.unpack
  local result = ""
  local M, ba, bb, buf = 2/N, 2^(N%8+1)-1, 2^(8-N%8), {}
  local start_line, end_line = N/total * (i-1), N/total * i - 1
  for y=start_line,end_line do
    local Ci, b, p = y*M-1, 1, 0
    for x=0,N-1 do
      local Cr = x*M-1.5
      local Zr, Zi, Zrq, Ziq = Cr, Ci, Cr*Cr, Ci*Ci
      b = b + b
      for i=1,49 do
        Zi = Zr*Zi*2 + Ci
        Zr = Zrq-Ziq + Cr
        Ziq = Zi*Zi
        Zrq = Zr*Zr
        if Zrq+Ziq > 4.0 then b = b + 1; break; end
      end
      if b >= 256 then p = p + 1; buf[p] = 511 - b; b = 1; end
    end
    if b ~= 1 then p = p + 1; buf[p] = (ba-b)*bb; end
      result = result .. char(unpack(buf, 1, p))
    end
    return result
end
'''


def LuaMandelbrot(thrCnt, size):

    def LuaMandelbrotFunc(i, lua_func):
        results[i] = lua_func(size, i + 1, thrCnt)

    t1 = time.time()
    lua_funcs = [LuaRuntime(encoding=None).eval(lua_code)
                 for _ in range(thrCnt)]

    results = [None] * thrCnt

    threads = [threading.Thread(target=LuaMandelbrotFunc, args=(i, lua_func))
               for i, lua_func in enumerate(lua_funcs)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    result_buffer = b''.join(results)
    dt = time.time() - t1
    print(f"dt={dt:.2f}")

    image = Image.frombytes('1', (size, size), result_buffer)
    image.show()
