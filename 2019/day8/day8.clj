#!/usr/bin/env clojure

(require '[clojure.string :as str])

(defn to-int [s] (Integer/parseInt s))

(defn to-ints [s] (map (fn [c] (to-int (str c))) s))

(defn count-x [layer x]
  (apply + (map (fn [c] (if (= x c) 1 0)) layer)))

(defn count-zeros [layer]
  (count-x layer 0))

(defn split-layers [data width height]
  (let [layersize (* width height)
        nlayers (/ (count data) layersize)]
    (map (fn [x] (to-ints
                   (subs data
                         (* x layersize)
                         (* (+ x 1) layersize))))
         (range nlayers))))

(defn day8 [data width height]
  (let [layers (split-layers data width height)
        best (apply min-key count-zeros layers)]
        (* (count-x best 1) (count-x best 2))))

(defn paint [color previous]
  (if (= 2 previous) color previous))

(defn pretty [picture]
  (map (fn [x]
           (if (= 1 x) "X" " "))
       picture))

(defn display [picture width]
  (let [rows (partition width picture)]
    (doall (map (fn [row] (println (str/join "" row))) rows))))

(defn day8b [data width height]
  (let [layers (split-layers data width height)
        picture (reduce (fn [top bottom] (map paint bottom top)) layers)]
    (display (pretty picture) width)))

(def input (str/trim (slurp "input.txt")))
(println (day8 input 25 6))
(day8b input 25 6)
