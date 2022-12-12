fennel = require("fennel")
debug.traceback = fennel.traceback
table.insert(package.loaders, function(filename)
   if love.filesystem.getInfo(filename) then
      return function(...)
         return fennel.eval(love.filesystem.read(filename), {env=_G, filename=filename}, ...), filename
      end
   end
end)
pp = function(x) print(fennel.view(x)) end
local asyncrepl = require("asyncrepl.fnl")
asyncrepl.start()
-- jump into Fennel
require("game.fnl")
