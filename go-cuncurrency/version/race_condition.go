package version

import (
	"fmt"
	"sync"
)

func RaceCondition() {
	arr := make([]string, 20)
	var wg sync.WaitGroup

	wg.Add(1)

	go func() {
		for i := 0; i < len(arr); i++ {
			arr[i] = "-"
		}
		wg.Done()
	}()

	go func() {
		for i := 0; i < len(arr); i++ {
			arr[i] = "_"
		}
		wg.Done()
	}()

	wg.Wait()
	fmt.Println(arr)
}
