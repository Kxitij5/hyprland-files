require("dotenv").config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
// always keep the require("dotenv").config(); line before using process.env.VARIABLE
const uri = process.env.DB_URI;
mongoose.connect(uri);
const connection = mongoose.connection;
connection.once('open', ()=>{
    console.log("Mongoose Connected to the database!");
})
const app = express();
const port = process.env.PORT || 3000;


app.use(cors());
app.use(express.json());


app.listen(port, ()=>{
    console.log(`The server is running on ${port}`);
})