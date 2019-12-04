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

(defn- travel-distance-to [path [dx dy]]
  (loop [path path
          dist 0
          x    0
          y    0]
    (let [[dir len] (first path)
            points   (set (travel-points x y dir len))]
      (if (contains? points [dx dy])
        (+ dist (Math/abs (- dx x)) (Math/abs (- dy y)))
        (let [[x' y'] (move x y dir len)]
          (recur (rest path)
                  (+ dist len)
                  x'
                  y'))))))

(defn- points-for-path [path]
  (loop [points #{}
         path   path
         x      0
         y      0]
    (if (empty? path)
      points
      (let [[dir len] (first path)
            [x' y']   (move x y dir len)]
        (recur (set (concat points (travel-points x y dir len)))
               (rest path)
               x'
               y')))))

(defn- manhattan-distance [[x y]]
  (+ (Math/abs x) (Math/abs y)))

(defn day03a [paths]
  (->> paths
       (map points-for-path)
       (apply clojure.set/intersection)
       (map manhattan-distance)
       (filter pos?)
       (apply min)))

(defn day03b [paths]
  (->> paths
       (map points-for-path)
       (apply clojure.set/intersection)
       (map (fn [[x y]]
              (apply + (map #(travel-distance-to % [x y]) paths))))
       (filter pos?)
       (apply min)))

(let [paths (->> (str/split (slurp "day03.txt") #"\n")
                 (map path-from-input))]
  (println (day03a paths))
  (println (day03b paths)))
