import express from 'express';
import http from 'http';
import {Server} from 'socket.io';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);
const io = new Server(server)

app.use(express.static(path.join(__dirname, 'src')));

io.on('connection', socket => {
    console.log('WE GOT A CONNECTION BOYZZZ WOOOOOOOO!!!!!');

    socket.on('offer', offer => socket.broadcast.emit('offer', offer));
    socket.on('answer', answer => socket.broadcast.emit('answer', answer));
    socket.on('ice-candidate', candidate => socket.broadcast.emit('ice-candidate', candidate));
});

const PORT = 3000;

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Servfer running at http://<your-local-ip>:${PORT}`)
});