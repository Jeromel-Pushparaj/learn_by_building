package main

import (
	"fmt"
	"sync"
	"time"
)

func main() {
	arr := make([]string, 20)
	var wg sync.WaitGroup

	wg.Add(2)

	go func() {
		for i := 0; i < len(arr); i++ {
			arr[i] = "-"
			time.Sleep(time.Millisecond * 1) // force interleaving
		}
		wg.Done()
	}()

	go func() {
		for i := 0; i < len(arr); i++ {
			arr[i] = "_"
			time.Sleep(time.Millisecond * 1) // force interleaving
		}
		wg.Done()
	}()

	wg.Wait()
	fmt.Println(arr)
}
