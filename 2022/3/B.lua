#!/bin/lu9

s_prios = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
prios = {}
for i=1, #s_prios do
	prios[s_prios:sub(i, i)] = i
end

total = 0
group = {}
for line in io.input():lines() do
	table.insert(group, line)
	if #group == 3 then
		badge = '?'
		for i=1, #group[1] do
			badge = group[1]:sub(i,i)
			if group[2]:find(badge) and group[3]:find(badge) then
				break
			end
		end
		--print('badge', badge)
		total = total + prios[badge]
		group = {}
	end
end
print(total)