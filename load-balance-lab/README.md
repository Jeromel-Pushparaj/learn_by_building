# Load Balancer Experiment with Nginx, Multiple App Servers, and K6 Load Testing

This repository documents an experiment designed to understand how load balancing works in practice.
Instead of studying theory alone, this project demonstrates the behavior of a load balancer under real traffic by creating a small distributed system locally and testing it with a load generator.

The goal is to observe how many requests each application container receives when placed behind an Nginx load balancer and then subjected to high traffic from K6.

---

## 1. Overview

This project consists of the following components:

- Three identical application servers running in separate containers
- An Nginx load balancer configured to distribute traffic to all three
- A K6 load testing script that generates high-volume traffic
- A simple counter inside each application to track how many requests it serves
- Logging to visualize load distribution clearly

This setup provides a small-scale production-like environment for learning and experimentation.

---

## 2. Architecture

```
           +---------------------+
           |     K6 Load Test    |
           +----------+----------+
                      |
                      v
            +---------------------+
            |   Nginx Load Balancer |
            +---------+------------+
                      |
    ---------------------------------------------
    |                   |                       |
    v                   v                       v
+---------+       +---------+             +---------+
| App 1   |       | App 2   |             | App 3   |
+---------+       +---------+             +---------+
```

Each application container increments a local request counter on every incoming request and returns the container name and counter value in the response.
This makes load distribution observable.

---

## 3. Application Server

Each app instance exposes a simple endpoint that returns the number of requests handled.

Example (Node.js):

```js
const express = require("express");
const os = require("os");

const app = express();
let totalRequests = 0;

app.get("/", (req, res) => {
  totalRequests++;
  res.json({
    container: os.hostname(),
    total: totalRequests,
  });
});

app.listen(3000, () => {
  console.log("Application server running");
});
```

Each container will have its own hostname, making it possible to differentiate traffic.

---

## 4. Nginx Load Balancer Configuration

Example load balancer configuration:

```nginx
http {
    upstream backend_servers {
        server app1:3000;
        server app2:3000;
        server app3:3000;
    }

    server {
        listen 8080;

        location / {
            proxy_pass http://backend_servers;
        }
    }
}
```

By default, Nginx uses round-robin load balancing.

---

## 5. K6 Load Testing Script

Example `k6` script:

```js
import http from "k6/http";

export let options = {
  vus: 20,
  duration: "10s",
};

export default function () {
  http.get("http://localhost:8080/");
}
```

Running this script generates high traffic and reveals how Nginx distributes requests.

---

## 6. Running the Experiment

1. Start all containers:

```
docker compose up --build
```

2. Run the K6 load test:

```
k6 run loadtest.js
```

3. Observe console output from each application container:

```
App1: total requests: 920
App2: total requests: 915
App3: total requests: 910
```

4. Compare this with K6 output:

```
Total requests: 18404
Average RPS: ~1839
```

The distribution should be roughly even, validating the behavior of the load balancer.

---

## 7. Results and Insights

Key observations:

- The load balancer successfully distributed requests across all application containers.
- Each container received nearly equal traffic, confirming round-robin behavior.
- The system handled thousands of requests within seconds.
- Tracking per-container request counts provides clear visibility into load distribution.
- Building a hands-on environment explains load balancing more effectively than theory alone.

---

## 8. Why This Works as a Learning Tool

This experiment demonstrates core concepts:

- Horizontal scaling
- Stateless application design
- Load balancing algorithms
- Request distribution patterns
- Performance testing
- Distributed system behavior
- Containerized microservices workflow

Because the entire setup runs locally, it is safe, repeatable, and cost-free.

---

## 9. Future Improvements

Potential extensions:

- Add a weighted load balancer configuration
- Test least-connections or IP-hash strategies
- Add Prometheus + Grafana for metrics visualization
- Add autoscaling simulation
- Introduce artificial delays or failures to test resilience
- Compare Locust and K6 under identical conditions
- Add a caching layer in front of the application
- Introduce message queues to study backpressure

---

## 10. Conclusion

This experiment provides a clear and practical way to understand how load balancing behaves in real systems.
By simulating high traffic locally and observing distribution across multiple application servers, core backend concepts become much easier to grasp and internalize.

This repository is intended as a learning resource for anyone wanting a deeper understanding of load balancing, traffic distribution, and system scaling.
