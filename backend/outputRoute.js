import express from 'express'
import { saveOutput } from './outputController.js';

const outputRouter = express.Router()

outputRouter.post("/save", saveOutput)

export default outputRouter;