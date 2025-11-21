package version

import (
	"fmt"
	"runtime"
)

func Withchannel() {
	// runtime.GOMAXPROCS(1)
	fmt.Println(runtime.GOMAXPROCS(0))

	size := 20
	arr := make([]string, size)

	ch := make(chan struct {
		idx int
		val string
	})

	go func() {
		for i := 0; i < size; i++ {
			ch <- struct {
				idx int
				val string
			}{i, "-"}
		}
	}()

	go func() {
		for i := 0; i < size; i++ {
			ch <- struct {
				idx int
				val string
			}{i, "_"}
		}
	}()

	// main goroutine is consumer
	for i := 0; i < size*2; i++ {
		msg := <-ch
		arr[msg.idx] = msg.val
	}

	fmt.Println(arr)
}
