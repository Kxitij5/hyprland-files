const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const uri = process.env.DB_URI;
mongoose.connect(uri, {useNewUrlParser: true, useCreateIndex: true});
const connection = mongoose.connection;

require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;


app.use(cors());
app.use(express.json());


app.listen(port, ()=>{
    console.log(`The server is running on ${port}`);
})