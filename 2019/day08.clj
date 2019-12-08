(ns adventofcode2019.day08
  (:require [clojure.string :as str]))

(defn- parse-input [input]
  (->> input
       (seq)
       (map int)
       (map #(- % (int \0)))))

(assert (= [1 2 3] (parse-input "123")))

(defn- layers [width height data]
  (partition (* width height) data))

(defn- number-of-zeros [data]
  (count (filter zero? data)))

(defn- product-of-number-of-digits [digits data]
  (->> digits
       (map (fn [digit] (count (filter #(= digit %) data))))
       (reduce * 1)))

(defn- part1 [data]
  (->> data
       (parse-input)
       (layers 25 6)
       (apply min-key number-of-zeros)
       (product-of-number-of-digits [1 2])))

(println (part1 (slurp "day08.txt")))

(defn- layers-for-pixel [layers i]
  (map #(nth % i) layers))

(defn- color [pixels]
  (let [px (first pixels)]
    (if (= 2 px)
      (color (rest pixels))
      px)))

(defn- part2 [data width height]
  (let [layers (->> data
                    (parse-input)
                    (layers width height))]
    (->> (range 0 (* width height))
         (map (fn [i]
                (color (layers-for-pixel layers i))))
         (map str)
         (map #(if (= "0" %) " " %))
         (partition width)
         (map #(str/join "" %))
         (str/join "\n"))))

(println (part2 (slurp "day08.txt") 25 6))
