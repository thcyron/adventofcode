(ns adventofcode.day04
  (:require [clojure.string :as str]))

(defn- increasing? [digits]
  (if (<= (count digits) 1)
    true
    (let [a (nth digits 0)
          b (nth digits 1)]
      (if (<= a b)
        (increasing? (drop 1 digits))
        false))))

(defn- digits [n]
  (map #(Integer/parseInt %) (str/split (str n) #"")))

(defn- consecutive-groups [digits]
  (loop [groups []
         digits digits]
    (if (empty? digits)
      groups
      (let [d (first digits)
            g (take-while #(= d %) digits)
            r (drop (count g) digits)]
        (recur (conj groups g) r)))))

(defn day04a [start end]
  (->> (range start (inc end))
       (map digits)
       (filter increasing?)
       (filter (fn [digits]
                 (->> (consecutive-groups digits)
                      (map count)
                      (filter #(>= % 2))
                      (seq))))
       (count)))

(defn day04b [start end]
(->> (range start (inc end))
      (map digits)
      (filter increasing?)
      (filter (fn [digits]
        (let [groups (consecutive-groups digits)
              lens   (set (map count groups))]
          (and (contains? lens 2)
               (seq (filter #(>= % 2) lens))))))
      (count)))

(println (day04a 240298 784956))
(println (day04b 240298 784956))
