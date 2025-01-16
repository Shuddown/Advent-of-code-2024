package main

import (
	"fmt"
	"os"
	"strings"
)

func check(e error) {
    if e != nil {
        panic(e)
    }
}

func main()  {
    data, err  := os.ReadFile("/home/sukessh/Programs/Advent-of-code-2024/AOC 2024/Day 1/input.txt")
    check(err)
    contents := strings.Split(string(data), " ")
    fmt.Println(contents)
}