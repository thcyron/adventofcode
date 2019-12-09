(ns adventofcode.day09
  (:require [clojure.string :as str]))

(defn- mode [x]
  (case x
    \0 :position
    \1 :immediate
    \2 :relative))

(defn- modes [code]
  (->> code
       (format "%05d")
       (take 3)
       (reverse)
       (map mode)
       (vec)))

(assert (= [:immediate :immediate :position]) (modes 1102))
(assert (= [:position ::position :relative]) (modes 203))

(defn- opcode [state]
  (nth (:memory state) (:ip state)))

(defn- operand [state pos]
  (nth (:memory state) (+ (:ip state) 1 pos)))

(defn- operand-mode [state pos]
  (let [modes (modes (opcode state))]
    (nth modes pos)))

(defn- resolve-address [state pos]
  (let [addr (operand state pos)
        mode (operand-mode state pos)]
    (case mode
      :position addr
      :relative (+ (:rb state) addr))))

(defn- assoc-codes [codes idx value]
  (let [actual-size (count codes)
        needed-size (inc idx)
        diff        (- needed-size actual-size)]
    (if (pos? diff)
      (assoc (vec (concat codes (take diff (repeat 0)))) idx value)
      (assoc codes idx value))))

(defn- resolve-operands [state n]
  (->> (range 0 n)
       (map (fn [i]
              (let [o (operand state i)
                    m (operand-mode state i)]
                (case m
                  :position (nth (:memory state) o)
                  :immediate o
                  :relative (nth (:memory state) (+ (:rb state) o))))))))

(defn- run-arithmetic [f state]
  (let [[a b] (resolve-operands state 2)
        res   (f a b)]
    (-> state
        (update :memory #(assoc-codes % (resolve-address state 2) res))
        (update :ip #(+ % 4)))))

(defn- run-output [state]
  (let [[a] (resolve-operands state 1)]
    (-> state
        (update :ip #(+ % 2))
        (update :out #(conj % a)))))

(defn- run-jump [f state]
  (let [[a b] (resolve-operands state 2)]
    (if (f a)
      (assoc state :ip b)
      (update state :ip #(+ % 3)))))

(defn- run-comparison [f state]
  (let [[a b] (resolve-operands state 2)
        res   (if (f a b) 1 0)]
    (-> state
        (update :memory #(assoc-codes % (resolve-address state 2) res))
        (update :ip #(+ % 4)))))

(defn- run-input [state]
  (-> state
      (update :inputs #(rest %))
      (update :memory #(assoc-codes % (resolve-address state 0) (first (:inputs state))))
      (update :ip #(+ % 2))))

(defn- run-rb [state]
  (let [[a] (resolve-operands state 1)]
    (-> state
        (update :rb #(+ % a))
        (update :ip #(+ % 2)))))

(defn- opcode-function [opcode]
  (case opcode
    1 (partial run-arithmetic +)
    2 (partial run-arithmetic *)
    3 (partial run-input)
    4 (partial run-output)
    5 (partial run-jump (partial not= 0))
    6 (partial run-jump zero?)
    7 (partial run-comparison <)
    8 (partial run-comparison =)
    9 (partial run-rb)))

(defn- run [inputs codes]
  (loop [state {:memory codes :inputs inputs :rb 0 :ip 0 :out []}]
    (let [opcode (mod (nth (:memory state) (:ip state)) 100)]
      (if (= 99 opcode)
        (:out state)
        (let [f (opcode-function opcode)]
          (recur (f state)))))))

(assert (= [1] (run [1] [3 0 4 0 99])))

(defn- instructions-from-input [input]
  (->> (str/split input #",")
       (map #(Long/parseLong %))
       (vec)))

(let [instructions (instructions-from-input (slurp "day09.txt"))]
  (println (first (run [1] instructions)))
  (println (first (run [2] instructions))))
