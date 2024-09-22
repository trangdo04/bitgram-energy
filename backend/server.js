import express from 'express'
import cors from 'cors'
import { connectDB } from './config/database.js'

const app = express()
const port = 4000

app.use(express.json())
app.use(cors())

connectDB();

app.get("/",(req, res)=>{
    res.send("API working")
})

app.listen(port, () => {
    console.log(`Server started on port: ${port}`)
})