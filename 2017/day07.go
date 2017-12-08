package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"

	"github.com/thcyron/graphs"
)

var (
	reBranch = regexp.MustCompile(`^([a-z]+) \((\d+)\) -> (.+)$`)
	reLeaf   = regexp.MustCompile(`^([a-z]+) \((\d+)\)$`)
)

var weights = map[string]int{}

func main() {
	g := graphs.NewDigraph()
	r := bufio.NewScanner(os.Stdin)

	for i := 1; r.Scan(); i++ {
		line := strings.TrimSpace(r.Text())

		if m := reBranch.FindStringSubmatch(line); m != nil {
			name := m[1]
			weight, _ := strconv.Atoi(m[2])
			list := strings.Split(m[3], ", ")
			weights[name] = weight
			g.AddVertex(name)
			for _, n := range list {
				g.AddEdge(name, n, 0)
			}
			continue
		}

		if m := reLeaf.FindStringSubmatch(line); m != nil {
			name := m[1]
			weight, _ := strconv.Atoi(m[2])
			weights[name] = weight
			g.AddVertex(name)
			continue
		}

		log.Fatalf("invalid line %d\n", i)
	}

	topsortList, _, _ := graphs.TopologicalSort(g)
	bottom := topsortList.Front().Value.(string)
	fmt.Println(bottom)

	fix, _ := balanceFix(g, bottom)
	fmt.Println(fix)
}

func balanceFix(g *graphs.Graph, bottom string) (int, bool) {
	ws := map[string]int{}
	for he := range g.HalfedgesIter(bottom) {
		w := 0
		graphs.DFS(g, he.End, func(v graphs.Vertex, stop *bool) {
			w += weights[v.(string)]
		})
		ws[he.End.(string)] = w
	}

	outliner, ow, nw := findOutliner(ws)
	if outliner == "" {
		return 0, true
	}

	diff, ok := balanceFix(g, outliner)
	if ok {
		return weights[outliner] - (ow - nw), false
	}
	return diff, false
}

func findOutliner(weights map[string]int) (string, int, int) {
outer:
	for n1, w1 := range weights {
		var w int
		for n2, w2 := range weights {
			if n1 == n2 {
				continue
			}
			if w1 == w2 {
				continue outer
			}
			w = w2
		}
		return n1, w1, w
	}
	return "", 0, 0
}
