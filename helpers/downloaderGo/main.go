package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"

	"github.com/golang/glog"
)

// func download(url string) (bool, string, error) {
func download(url string) {
	tokens := strings.Split(url, "/")
	fileName := tokens[len(tokens)-1]
	fmt.Println(1)
	if _, err := os.Stat(fileName); !os.IsNotExist(err) {
		// return false, url, errors.New("File " + fileName + " already exist!")
		return
	}
	fmt.Println(2)

	file, err := os.Create(fileName)
	fmt.Println(3)
	glog.Infoln("File " + fileName + " created")
	if err != nil {
		// return false, url, err
		return
	}
	defer file.Close()

	resp, err := http.Get(url)
	if err != nil {
		// return false, url, err
		return
	}
	defer resp.Body.Close()

	_, err = io.Copy(file, resp.Body)
	if err != nil {
		// return false, url, err
		return
	}
	// return true, url, nil
	return
}

func main() {
	l := [34]string{"https://pp.vk.me/c627425/v627425634/1e303/CElN2liC1nw.jpg", "https://pp.vk.me/c622930/v622930449/60848/DRm_l1xywL8.jpg", "https://pp.vk.me/c622221/v622221844/489f2/NeQJit-nGrw.jpg", "https://pp.vk.me/c629511/v629511781/167af/Y-3ZABMIVmw.jpg", "https://pp.vk.me/c628428/v628428368/142bd/_IHxIet5_x4.jpg", "https://pp.vk.me/c628616/v628616471/19ce3/I1vXHqaX0_s.jpg", "https://pp.vk.me/c623818/v623818624/47edc/EL84Ah5urhU.jpg", "https://pp.vk.me/c629101/v629101275/13b7c/b-Q0SnPuo2o.jpg", "https://pp.vk.me/c624631/v624631559/47526/tf-etnoAfkU.jpg", "https://pp.vk.me/c628623/v628623729/1ce53/n-Uuq1zhfv4.jpg", "https://pp.vk.me/c622827/v622827480/4311c/uZAUE32uLAs.jpg", "https://pp.vk.me/c629415/v629415481/13b5b/WFV1sHDc3q0.jpg", "https://pp.vk.me/c628520/v628520363/1bbc0/IPHRIJs0EZQ.jpg", "https://pp.vk.me/c629218/v629218880/158a5/t4g6UwYDy6M.jpg", "https://pp.vk.me/c629218/v629218698/f180/g-9gm3ntApY.jpg", "https://pp.vk.me/c629218/v629218168/225b0/Y_S8HDoK-D0.jpg", "https://pp.vk.me/c629218/v629218358/1596e/0_GOCBYdd7Q.jpg", "https://pp.vk.me/c629218/v629218038/11ae0/otGz_Q4OCBI.jpg", "https://pp.vk.me/c629218/v629218456/13d58/iBLNBMjkQMM.jpg", "https://pp.vk.me/c629218/v629218917/144eb/OEz50Qkf-WI.jpg", "https://pp.vk.me/c629218/v629218271/1824d/yGCWziFseG4.jpg", "https://pp.vk.me/c629218/v629218732/11171/RbGuBmpKBvo.jpg", "https://pp.vk.me/c628618/v628618505/155b3/gO0rnFnVu40.jpg", "https://pp.vk.me/c621923/v621923710/380b4/4VU3oGLo2gs.jpg", "https://pp.vk.me/c627316/v627316622/190d3/K8PCylO61zY.jpg", "https://pp.vk.me/c622424/v622424983/3dfa3/dAshMaAFlT4.jpg", "https://pp.vk.me/c625417/v625417612/3d026/mV1bBiUweWE.jpg", "https://pp.vk.me/c628623/v628623836/172cc/jaXzSjPNxzo.jpg", "https://pp.vk.me/c629214/v629214393/15c72/zo5utvUVLj4.jpg", "https://pp.vk.me/c623423/v623423090/3fb6e/5e89tajneNU.jpg", "https://pp.vk.me/c629115/v629115547/111e7/1gYYlncX6pQ.jpg", "https://pp.vk.me/c627120/v627120884/1d075/MLvYJOxJJH0.jpg", "https://pp.vk.me/c629218/v629218506/10871/IgkK0HL11FU.jpg", "https://pp.vk.me/c623928/v623928953/44e26/ssHszZ8_zDE.jpg"}
	for _, url := range l {
		go func(url string) {
			download(url)
		}(url)
	}
	var input string
	fmt.Scanln(&input)
	// result, url, err := download("http://lorempixel.com/800/400/")
	fmt.Println("DONE!")
}
