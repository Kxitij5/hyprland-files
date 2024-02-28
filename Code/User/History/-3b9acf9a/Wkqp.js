const express = require('express');
const path = require('path');
const app = express();
const port = 3000;

app.use('/',(require(path.join(__dirname, 'routes/route.js'))))

app.listen(port, ()=>{console.log(`Server listening at http://localhost:${port}`)})

