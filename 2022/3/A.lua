#!/bin/lu9
-- a shame I can't have shebangs portable between plan9 and posix

s_prios = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
prios = {}
for i=1, #s_prios do
	prios[s_prios:sub(i, i)] = i
end

total = 0
for line in io.input():lines() do
	--print('line:', line, 'length:', #line)
	local a = line:sub(1, #line//2)
	local b = line:sub(#line//2+1)
	--print('a:', a)
	--print('b:', b)
	local c = '?'
	for i=1, #a do
		c = a:sub(i,i)
		if b:find(c) then
			break
		end
	end
	total = total + prios[c]
end
print(total)