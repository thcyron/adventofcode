(ns adventofcode.day02
    (:use [clojure.string :only [split]]
          [clojure.test :only [is]]))

(defn- run-op [instr pos op]
  (let [op-a (nth instr (nth instr (+ pos 1)))
        op-b (nth instr (nth instr (+ pos 2)))
        dest (nth instr (+ pos 3))
        res  (op op-a op-b)]
    (vec (assoc instr dest res))))

(defn- run [instr pos]
  (case (nth instr pos)
    1  (run (run-op instr pos +) (+ pos 4))
    2  (run (run-op instr pos *) (+ pos 4))
    99 (first instr)))

(defn- day02a [instr]
  (run instr 0))

(defn- day02b [instr]
  (let [result (first (for [noun (range 0 99)
                            verb (range 0 99)
                            :let [r (run (-> instr (assoc 1 noun) (assoc 2 verb)) 0)]
                            :when (= r 19690720)]
                        {:noun noun :verb verb}))]
    (+ (* 100 (:noun result)) (:verb result))))

(defn- instr-from-input [input]
  (vec (map #(Integer/parseInt %) (split input #","))))

(let [instr (instr-from-input "1,9,10,3,2,3,11,0,99,30,40,50")]
  (is (day02a instr) 3500))

(let [instr  (instr-from-input (slurp "day02.txt"))
      instr' (-> instr (assoc 1 12) (assoc 2 2))]
  (println (day02a instr'))
  (println (day02b instr')))
