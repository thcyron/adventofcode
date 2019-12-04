(ns adventofcode.day03
  (:require [clojure.set]
            [clojure.string :as str]))

(defn- parse-path-component [comp]
  (let [dir (.toLowerCase (subs comp 0 1))
        len (Integer/parseInt (subs comp 1))]
    [(keyword dir) len]))

(defn- path-from-input [input]
  (map parse-path-component (str/split input #",")))

(defn- move [x y dir len]
  (case dir
    :r [(+ x len) y]
    :l [(- x len) y]
    :u [x (+ y len)]
    :d [x (- y len)]))

(defn- travel-points [x y dir len]
  (case dir
    :r (map #(do [% y]) (range x (+ x len 1)))
    :l (map #(do [% y]) (range x (- x len 1) -1))
    :u (map #(do [x %]) (range y (+ y len 1)))
    :d (map #(do [x %]) (range y (- y len 1) -1))))

(defn- travel-distance-to [points [dx dy]]
  (loop [ps   points
         dist 0]
    (let [[x y] (first ps)]
      (if (and (= x dx) (= y dy))
        dist
        (recur (rest ps) (inc dist))))))

(defn- points-for-path [path]
  (loop [points [[0 0]]
         path   path
         x      0
         y      0]
    (if (empty? path)
      points
      (let [[dir len] (first path)
            [x' y']   (move x y dir len)]
        (recur (concat points (rest (travel-points x y dir len)))
               (rest path)
               x'
               y')))))

(defn- manhattan-distance [[x y]]
  (+ (Math/abs x) (Math/abs y)))

(defn day03a [paths]
  (->> paths
       (map points-for-path)
       (map set)
       (apply clojure.set/intersection)
       (map manhattan-distance)
       (filter pos?)
       (apply min)))

(defn day03b [paths]
  (let [path-points (map points-for-path paths)]
    (->> path-points
         (map set)
         (apply clojure.set/intersection)
         (map (fn [[x y]]
                (reduce + (map #(travel-distance-to % [x y]) path-points))))
         (filter pos?)
         (apply min))))

(let [paths (->> (str/split (slurp "day03.txt") #"\n")
                 (map path-from-input))]
  (println (day03a paths))
  (println (day03b paths)))
