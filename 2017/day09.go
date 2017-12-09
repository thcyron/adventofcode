package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
)

func main() {
	stream, err := ioutil.ReadAll(os.Stdin)
	if err != nil {
		log.Fatalln(err)
	}
	stream = bytes.TrimSpace(stream)

	var (
		group        int
		garbage      bool
		escape       bool
		groupsum     int
		garbagecount int
	)
	for i := 0; i < len(stream); i++ {
		c := stream[i]
		if escape {
			escape = false
			continue
		}
		switch c {
		case '{':
			if garbage {
				garbagecount++
			} else {
				group++
			}
		case '}':
			if garbage {
				garbagecount++
			} else {
				groupsum += group
				group--
			}
		case '<':
			if garbage {
				garbagecount++
			} else {
				garbage = true
			}
		case '>':
			garbage = false
		case '!':
			escape = true
		case ',':
			if garbage {
				garbagecount++
			}
		default:
			if garbage {
				garbagecount++
			} else {
				panic(fmt.Sprintf("bad character while not in garbage mode: %v", c))
			}
		}
	}

	fmt.Println(groupsum)
	fmt.Println(garbagecount)
}
