import http from "k6/http";

export let options = {
  vus: 20,
  duration: "10s",
}

// var num = 1;
export default function () {
  http.get(`http://localhost:8080/`);
  // num = res.json()[0].num;

}
