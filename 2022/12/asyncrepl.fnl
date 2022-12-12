; from https://gitlab.com/alexjgriffith/love-fennel
(require "love.event")
(fn prompt [cont?]
  (io.write (if cont? ".." ">> "))
  (io.flush)
  (.. (io.read) "\n"))

(fn looper [event channel]
  (match (channel:demand)
    [:write vals]
    (do
      (io.write (table.concat vals "	"))
      (io.write "\n"))
    [:read cont?]
    (love.event.push event (prompt cont?)))
  (looper event channel))

(match ...
  (event channel)
  (looper event channel))

{:start
  (fn start-repl []
    (let [code (love.filesystem.read "asyncrepl.fnl")
          luac (love.filesystem.newFileData (fennel.compileString code) "io")
          thread (love.thread.newThread luac)
          io-channel (love.thread.newChannel)
          coro (coroutine.create fennel.repl)
          options {
            :readChunk
              (fn [{: stack-size}]
                (io-channel:push [:read (< 0 stack-size)])
                (coroutine.yield))
            :onValues
              (fn [vals]
                (io-channel:push [:write vals]))
            :onError
              (fn [errtype err]
                (io-channel:push [:write [err]]))
            :moduleName "lib.fennel"}]
      (coroutine.resume coro options)
      (thread:start "eval" io-channel)
      (set love.handlers.eval
           (fn [input] (coroutine.resume coro input)))))}
