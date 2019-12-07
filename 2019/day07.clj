(ns adventofcode.day06
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

(defn- run-arithmetic [f inputs codes ip out]
  (let [[a b]  (resolve-operands codes ip 2)
        c      (nth codes (+ ip 3))
        result (f a b)]
    [inputs (assoc codes c result) (+ ip 4) out]))

(defn- run-output [inputs codes ip out]
  (let [[a] (resolve-operands codes ip 1)]
    [inputs codes (+ ip 2) (conj out a)]))

(defn- run-jump [f inputs codes ip out]
  (let [[a b] (resolve-operands codes ip 2)]
    (if (f a)
      [inputs codes b out]
      [inputs codes (+ ip 3) out])))

(defn- run-comparison [f inputs codes ip out]
  (let [[a b]  (resolve-operands codes ip 2)
        c      (nth codes (+ ip 3))
        result (if (f a b) 1 0)]
    [inputs
     (assoc codes c result)
     (+ ip 4)
     out]))

(defn- run-input [inputs codes ip out]
  [(rest inputs)
   (assoc codes (nth codes (inc ip)) (first inputs))
   (+ ip 2)
   out])

(defn- opcode-function [opcode]
  (case opcode
    1 (partial run-arithmetic +)
    2 (partial run-arithmetic *)
    3 (partial run-input)
    4 (partial run-output)
    5 (partial run-jump (partial not= 0))
    6 (partial run-jump zero?)
    7 (partial run-comparison <)
    8 (partial run-comparison =)))

(defn- run
  ([inputs codes]
    (run inputs codes 0 []))
  ([inputs codes ip out]
    (let [opcode (mod (nth codes ip) 100)]
      (if (= 99 opcode)
        out
        (let [f (opcode-function opcode)]
          (apply run (f inputs codes ip out)))))))

(assert (= [1] (run [1] [3 0 4 0 99])))

(defn- instructions-from-input [input]
  (->> (str/split input #",")
       (map #(Integer/parseInt %))
       (vec)))

(defn- thruster-signal [instructions settings]
  (loop [last-output 0
         settings settings]
    (if (empty? settings)
      last-output
      (let [out (run [(first settings) last-output] instructions)]
        (recur (last out) (rest settings))))))

(assert (= 54321 (thruster-signal [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0] [0 1 2 3 4])))
(assert (= 65210 (thruster-signal [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0] [1 0 4 3 2])))

(defn- thruster-signal-loop [instructions settings]
  (loop [i    0
         amps (vec (map (fn [x] [[x] instructions 0 []]) settings))]
    (let [amp (nth amps i)
          [inputs instr ip out] amp
          j (mod (inc i) (count amps))
          opcode (mod (nth instr ip) 100)]
      (case
        opcode
        ; halt
        99 (if (zero? i)
             (first inputs)
             (recur j (assoc amps i nil)))
        ; input
        3 (recur i
                 (assoc amps i (run-input (if (empty? inputs) [0] inputs) instr ip out)))
        ; output
        4 (let [[new-inputs instr ip new-out] (run-output inputs instr ip out)
                next-amp (nth amps j)
                new-amp-inputs (concat (nth next-amp 0) new-out)
                new-next-amp (assoc next-amp 0 new-amp-inputs)]
            (recur j (-> amps
                         (assoc i [new-inputs instr ip out])
                         (assoc j new-next-amp))))
        (let [f (opcode-function opcode)]
          (recur i (assoc amps i (f inputs instr ip out))))))))

(assert (= 139629729 (thruster-signal-loop [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5] [9 8 7 6 5])))

(defn permutations [s]
  (lazy-seq (if (seq (rest s))
              (apply concat (for [x s]
                              (map #(cons x %) (permutations (remove #{x} s)))))
              [s])))

(defn- max-thruster-signal [instructions]
  (->> (permutations [0 1 2 3 4])
       (map (partial thruster-signal instructions))
       (apply max)))

(defn- max-thruster-signal-loop [instructions]
  (->> (permutations [5 6 7 8 9])
       (map (partial thruster-signal-loop instructions))
       (apply max)))

(let [instructions (instructions-from-input (slurp "day07.txt"))]
  (println (max-thruster-signal instructions))
  (println (max-thruster-signal-loop instructions)))
