(ns adventofcode.day10
  (:require [clojure.string :as str]))

(defn asteroids [input]
  (let [lines (map seq (str/split input #"\n"))
        height (count lines)
        width (count (first lines))]
    (for [x (range 0 width)
          y (range 0 height)
          :let [v (nth (nth lines y) x)]
          :when (= v \#)]
      {:x x :y y})))

(defn make-vector [a b]
  {:x (- (:x b) (:x a))
   :y (- (:y b) (:y a))})

(defn gcd [a b]
  (if (zero? b)
    (Math/abs a)
    (recur b (mod a b))))

(defn normalize-vector [{x :x y :y}]
  (let [d (gcd x y)]
    {:x (/ x d)
     :y (/ y d)}))

(defn detectable-asteroids [as a]
  (->> as
       (filter #(not= a %))
       (map #(make-vector a %))
       (map normalize-vector)
       set
       count))

(defn part1 [as]
  (apply max-key :c (map (fn [a]
                           {:a a :c (detectable-asteroids as a)}) as)))

(defn vector-length [v]
  (Math/sqrt (+ (Math/pow (:x v) 2) (Math/pow (:y v) 2))))

(assert (= 10.0 (vector-length {:x 10 :y 0})))

(defn bfs [x]
  (loop [res (lazy-seq)
         x x]
    (if (empty? x)
      res
      (recur (concat res (map first x))
             (filter seq (map rest x))))))

(assert (= [1 2 3 4 5] (vec (bfs [[1 4] [2] [3 5]]))))

(defn normalize-angle [p]
  (if (neg? p)
    (recur (+ (* 2 Math/PI) p))
    p))

(defn with-r-p [a b]
  (let [v (make-vector a b)
        r (vector-length v)
        p (cond (and (zero? (:x v)) (pos? (:y v))) Math/PI
                (and (zero? (:x v)) (neg? (:y v))) 0.0
                :else (+ (Math/atan2 (:y v) (:x v))
                         (/ Math/PI 2)))]
    (assoc b :r r :p (normalize-angle p))))

(defn part2 [as a]
  (let [by-p (->> as
                  (filter #(not= % a))
                  (map #(with-r-p a %))
                  (group-by :p))
        ps (sort (keys by-p))
        vap (bfs (map #(sort-by :r (get by-p %))
                      ps))]
    (nth vap 199)))

(let [as (asteroids (slurp "day10.txt"))]
  (let [r1 (part1 as)]
    (println (:c r1))
    (let [a (:a r1)
          r2 (part2 as a)]
      (println (+ (* (:x r2) 100) (:y r2))))))
