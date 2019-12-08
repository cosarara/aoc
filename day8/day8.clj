#!/usr/bin/env clojure

(defn to-int [s] (Integer/parseInt s))

(defn to-ints [s] (map (fn [c] (to-int (str c))) s))

(defn count-x [layer x]
  (apply + (map (fn [c] (if (= x c) 1 0)) layer)))

(defn count-zeros [layer]
  (count-x layer 0))

(defn day8 [data width height]
  (let [layersize (* width height)
        nlayers (/ (count data) layersize)
        layers (map (fn [x] (to-ints
                              (subs data
                                    (* x layersize)
                                    (* (+ x 1) layersize))))
                    (range nlayers))
        best (apply min-key count-zeros layers)]
        (* (count-x best 1) (count-x best 2))
    ))

(require '[clojure.string :as str])
(def input (str/trim (slurp "input.txt")))
(println (day8 input 25 6))
