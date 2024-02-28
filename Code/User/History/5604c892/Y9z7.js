const express = require('express');
const router = express.Router();
const path = require('path');
const blogs = require('../data/blogs')
router.get('/', (req,res)=>{
    res.sendFile(path.join(__dirname,"../templates/home.html"))
})
router.get('/blogs',(req,res)=>{
    blogs.forEach(element => {
        console.log(element.title)
    });
    res.sendFile(path.join(__dirname,"../templates/blogs.html"))
})
module.exports = router;
