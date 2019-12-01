(ns adventofcode.day01
  (:use [clojure.string :only [split-lines]]
        [clojure.test :only [is]]))

(defn- fuel-for-mass [m]
  (int (- (Math/floor (/ m 3)) 2)))

(is (= 33583 (fuel-for-mass 100756)))

(defn- fuel-for-mass' [m]
  (let [fuel (fuel-for-mass m)]
    (if (<= fuel 0)
      0
      (+ fuel (fuel-for-mass' fuel)))))

(is (= 50346 (fuel-for-mass' 100756)))

(defn day01a [masses]
  (reduce + (map fuel-for-mass masses)))

(defn day01b [masses]
  (reduce + (map fuel-for-mass' masses)))

(let [masses (->> (slurp "day01.txt")
                  split-lines
                  (map #(Integer/parseInt %)))]
  (println (day01a masses))
  (println (day01b masses)))
