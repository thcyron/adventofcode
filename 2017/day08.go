package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

var registers = map[string]int{}

type instruction struct {
	r   string // register
	op  string // operation
	off int    // offset
	cr  string // condition register
	cop string // condition operator
	cv  int    // condition value
}

func (i instruction) cond() bool {
	switch i.cop {
	case "==":
		return registers[i.cr] == i.cv
	case "!=":
		return registers[i.cr] != i.cv
	case "<":
		return registers[i.cr] < i.cv
	case ">":
		return registers[i.cr] > i.cv
	case "<=":
		return registers[i.cr] <= i.cv
	case ">=":
		return registers[i.cr] >= i.cv
	}
	panic("bad cop")
}

func (i instruction) exec() {
	if i.cond() {
		switch i.op {
		case "inc":
			registers[i.r] += i.off
		case "dec":
			registers[i.r] -= i.off
		default:
			panic(fmt.Sprintf("bad op: %q", i.op))
		}
	}
}

func main() {
	var (
		s            = bufio.NewScanner(os.Stdin)
		re           = regexp.MustCompile(`^([a-z]+) (inc|dec) (-?\d+) if ([a-z]+) (==|!=|<|>|<=|>=) (-?\d+)$`)
		instructions []instruction
		m            int
	)

	for i := 1; s.Scan(); i++ {
		line := strings.TrimSpace(s.Text())

		m := re.FindStringSubmatch(line)
		if m == nil {
			log.Fatalf("invalid line %d\n", i)
		}

		inst := instruction{
			r:   m[1],
			op:  m[2],
			cr:  m[4],
			cop: m[5],
		}

		inst.off, _ = strconv.Atoi(m[3])
		inst.cv, _ = strconv.Atoi(m[6])

		instructions = append(instructions, inst)
	}

	for i, inst := range instructions {
		inst.exec()
		if i == 0 {
			m = max()
		} else {
			if n := max(); n > m {
				m = n
			}
		}
	}

	fmt.Println(max())
	fmt.Println(m)
}

func max() int {
	var (
		first = true
		m     int
	)
	for _, v := range registers {
		if first {
			first = false
			m = v
		} else if v > m {
			m = v
		}
	}
	return m
}
