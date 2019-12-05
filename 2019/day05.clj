(ns adventofcode.day05
  (:require [clojure.string :as str]))

(defn- mode [x]
  (case x
    \0 :position
    \1 :immediate))

(defn- modes [code]
  (->> code
       (format "%05d")
       (take 3)
       (reverse)
       (map mode)
       (vec)))

(assert (= [:immediate :immediate :position]) (modes 1102))

(defn- resolve-operand [codes value mode]
  (case mode
    :position (nth codes value)
    :immediate value))

(defn- resolve-operands [codes ip n]
  (let [code     (nth codes ip)
        operands (->> codes
                      (drop (inc ip))
                      (take n))
        modes    (take n (modes code))]
    (map
      (fn [[o m]] (resolve-operand codes o m))
      (map vector operands modes))))

(defn- run-arithmetic [f codes ip out]
  (let [[a b]  (resolve-operands codes ip 2)
        c      (nth codes (+ ip 3))
        result (f a b)]
    [(assoc codes c result) (+ ip 4) out]))

(defn- run-output [codes ip out]
  (let [[a] (resolve-operands codes ip 1)]
    [codes (+ ip 2) (conj out a)]))

(defn- run-jump [f codes ip out]
  (let [[a b] (resolve-operands codes ip 2)]
    (if (f a)
      [codes b out]
      [codes (+ ip 3) out])))

(defn- run-comparison [f codes ip out]
  (let [[a b]  (resolve-operands codes ip 2)
        c      (nth codes (+ ip 3))
        result (if (f a b) 1 0)]
    [(assoc codes c result)
     (+ ip 4)
     out]))

(defn- run-input [input codes ip out]
  [(assoc codes (nth codes (inc ip)) input)
   (+ ip 2)
   out])

(defn- opcode-function [input opcode]
  (case opcode
    1 (partial run-arithmetic +)
    2 (partial run-arithmetic *)
    3 (partial run-input input)
    4 (partial run-output)
    5 (partial run-jump (partial not= 0))
    6 (partial run-jump zero?)
    7 (partial run-comparison <)
    8 (partial run-comparison =)))

(defn- run
  ([input codes]
    (run input codes 0 []))
  ([input codes ip out]
    (let [opcode (mod (nth codes ip) 100)]
      (if (= 99 opcode)
        out
        (let [f (opcode-function input opcode)]
          (apply run input (f codes ip out)))))))

(assert (= [1] (run 1 [3 0 4 0 99])))

(defn- instructions-from-input [input]
  (->> (str/split input #",")
       (map #(Integer/parseInt %))
       (vec)))

(let [instructions (instructions-from-input (slurp "day05.txt"))
      result-a     (run 1 instructions)
      result-b     (run 5 instructions)]
  (assert (= [0 0 0 0 0 0 0 0 0 9006673] result-a))
  (println result-a)
  (assert (= [3629692] result-b))
  (println result-b))
