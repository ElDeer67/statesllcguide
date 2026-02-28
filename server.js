const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8086;

const server = http.createServer((req, res) => {
    let filePath;
    const url = req.url.split('?')[0]; // strip query strings
    
    if (url === '/' || url === '/index.html') {
        filePath = path.join(__dirname, 'index.html');
    } else if (url === '/about.html') {
        filePath = path.join(__dirname, 'about.html');
    } else if (url.endsWith('-llc.html')) {
        // Serve any state LLC page dynamically
        const filename = url.slice(1); // remove leading /
        filePath = path.join(__dirname, filename);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 - Page Not Found</h1><p><a href="/">Go to homepage</a></p>');
        return;
    }
    
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404, { 'Content-Type': 'text/html' });
            res.end('<h1>404 - Page Not Found</h1><p><a href="/">Go to homepage</a></p>');
            return;
        }
        
        res.writeHead(200, { 
            'Content-Type': 'text/html',
            'Cache-Control': 'public, max-age=3600'
        });
        res.end(data);
    });
});

server.listen(PORT, '0.0.0.0', () => {
    console.log(`✅ StateBusinessGuide server running on port ${PORT}`);
    console.log(`📍 Local: http://localhost:${PORT}`);
    console.log(`\n🚀 52 pages available (50 states + homepage + about)`);
});
