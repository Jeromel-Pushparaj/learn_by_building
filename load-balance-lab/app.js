const express = require("express");
const os = require("os");
const app = express();

// app.get("/:num", (req, res) => {
//   var num = req.params.num;
//   var message = `Hello from ${os.hostname()}! - ${++num}`;
//   console.log(message);
//   const data = {
//     message: message,
//     timestamp: new Date().toISOString(),
//     num: num
//   };
//   res.json(data);
// });
//

let totalRequests = 0;

app.get("/", (req, res) => {
  totalRequests++;

  console.log(totalRequests);
  res.json({
    container: os.hostname(),
    total: totalRequests
  });

});

const port = 3000;
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
