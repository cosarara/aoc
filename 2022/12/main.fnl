(local lume (require "lume"))

(var grid "")
(local graph [])

(lambda icol [iterator]
	(icollect [a _ iterator] a))

(lambda split [s sep]
	(icol (s:gmatch (.. "[^" sep "]+"))))

(lambda load-input [?filename]
  (local s (love.filesystem.read (or ?filename "example")))
  (set grid (collect [line _ (s:gmatch "[^\n]+")]
              (collect [char _ (line:gmatch ".")] char)))
  grid)

(lambda make-graph []
  (each [k v (ipairs grid)] v
  ))

(fn love.load []
  (load-input))

(fn love.draw []
  (love.graphics.print
    "Hello from Fennel!\nPress q to quit" 10 10)
  (love.graphics.rectangle "fill" 50 50 20 20)
  )

(local reload (require "reload.fnl"))
(fn love.keypressed [key]
  (when (= "f5" key)
    (let [name "main.fnl"]
      (reload name)))
  (when (= "q" key)
    (love.event.quit)))

(print "main.fnl loaded!")
{:load-input load-input
 :make-graph make-graph}
