;; from the fennel repl.fnl
(local specials (require :fennel.specials))
(local compiler (require :fennel.compiler))

(fn default-on-values [xs]
  (io.write (table.concat xs "\t"))
  (io.write "\n"))

(fn default-on-error [errtype err lua-source]
  (io.write
   (match errtype
     "Lua Compile" (.. "Bad code generated - likely a bug with the compiler:\n"
                       "--- Generated Lua Start ---\n"
                       lua-source
                       "--- Generated Lua End ---\n")
     "Runtime" (.. (compiler.traceback (tostring err) 4) "\n")
     _ (: "%s error: %s\n" :format errtype (tostring err)))))

(fn reload [module-name env on-values on-error]
  ;; Sandbox the reload inside the limited environment, if present.
  (match (pcall (specials.load-code "return require(...)" env) module-name)
    (true old) (let [_ (tset package.loaded module-name nil)
                     (ok new) (pcall require module-name)
                     ;; keep the old module if reload failed
                     new (if (not ok)
                             (do
                               (on-values [new])
                               old)
                             new)]
                 (tset specials.macro-loaded module-name nil)
                 ;; if the module isn't a table then we can't make changes
                 ;; which affect already-loaded code, but if it is then we
                 ;; should splice new values into the existing table and
                 ;; remove values that are gone.
                 (when (and (= (type old) :table) (= (type new) :table))
                   (each [k v (pairs new)]
                     (tset old k v))
                   (each [k (pairs old)]
                     (when (= nil (. new k))
                       (tset old k nil)))
                   (tset package.loaded module-name old))
                 (on-values [:ok]))
    (false msg) (if (msg:match "loop or previous error loading module")
                    (do (tset package.loaded module-name nil)
                        (reload module-name env on-values on-error))
                    (. specials.macro-loaded module-name)
                    (tset specials.macro-loaded module-name nil)
                    ;; only show the error if it's not found in package.loaded
                    ;; AND macro-loaded
                    (on-error :Runtime (pick-values 1 (msg:gsub "\n.*" ""))))))
(lambda [module-name]
  (reload module-name nil default-on-values default-on-error))
