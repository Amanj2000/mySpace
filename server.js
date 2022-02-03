const express = require('express');
const app = express();

app.set('view engine', 'ejs');
const PORT = 8000;

app.get('/', (req, res) => {
    res.send("mySpace HomePage.")
})

app.listen(PORT)