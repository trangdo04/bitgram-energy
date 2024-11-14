import express from 'express'
import { saveOutput, getHistory } from '../controllers/outputController.js';

const outputRouter = express.Router()

outputRouter.post("/save", saveOutput)
outputRouter.post("/history", getHistory)

export default outputRouter;