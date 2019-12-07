(ns adventofcode.day06
  (:require [clojure.string :as str]))

(defn- build-tree [specs]
  (loop [tree {}
         specs specs]
    (if (empty? specs)
      tree
      (let [spec (first specs)
            [orbitee orbiter] spec
            orbiters (get tree orbitee [])]
        (recur (assoc tree orbitee (conj orbiters orbiter))
               (rest specs))))))

(defn- update-counts [counts orbitee orbiters]
  (if (empty? orbiters)
    counts
    (let [orbiter (first orbiters)]
      (update-counts
        (assoc counts orbiter (inc (get counts orbitee 0)))
        orbitee
        (rest orbiters)))))

(defn- total-indirects [tree]
  (loop [counts {}
         queue ["COM"]]
    (if (empty? queue)
      (reduce + 0 (vals counts))
      (let [orbitee    (first queue)
            orbiters   (get tree orbitee)
            new-queue  (concat (rest queue) orbiters)
            new-counts (update-counts counts orbitee orbiters)]
        (recur new-counts new-queue)))))

(defn- find-orbitee [tree orbiter]
  (first (for [[k v] tree
                :when (some #(= orbiter %) v)] k)))

(defn- path [tree source]
  (loop [node source
         p []]
    (case (get tree node)
      nil (reverse p)
      (recur (find-orbitee tree node)
             (conj p node)))))

(defn- number-of-orbit-changes [tree source destination]
  (loop [sp (path tree source)
         dp (path tree destination)]
    (if (= (first sp) (first dp))
      (recur (rest sp) (rest dp))
      (+ (count sp) (count dp)))))

(let [input (slurp "day06.txt")
      lines (str/split input #"\n")
      specs (map #(str/split % #"\)") lines)
      tree  (build-tree specs)]
  (println (total-indirects tree))
  (println (number-of-orbit-changes
             tree
             (find-orbitee tree "YOU")
             (find-orbitee tree "SAN"))))
