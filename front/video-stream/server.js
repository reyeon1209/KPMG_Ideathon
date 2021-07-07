//create a client
const { Storage } = require('@google-cloud/storage');
const projectId = 'meninblack-268711'//구글스토리지내의 projectId
const keyFilename = 'meninblackkey.json' // 구글스토리지 콘솔에서 key파일 생성

//서버 설정 
const express = require('express')
const fs = require('fs')
const path = require('path')
const app = express()

app.use(express.static(path.join(__dirname, 'public')))

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname + '/index.htm'))
})

app.get('/video', function(req, res) {
  const path = 'C:/Users/zm820/Desktop/img/1.mp4'
  const stat = fs.statSync(path)
  const fileSize = stat.size
  const range = req.headers.range

  if (range) {
    const parts = range.replace(/bytes=/, "").split("-")
    const start = parseInt(parts[0], 10)
    const end = parts[1]
      ? parseInt(parts[1], 10)
      : fileSize-1

    if(start >= fileSize) {
      res.status(416).send('Requested range not satisfiable\n'+start+' >= '+fileSize);
      return
    }
    
    const chunksize = (end-start)+1
    const file = fs.createReadStream(path, {start, end})
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    }

    res.writeHead(206, head)
    file.pipe(res)
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    }
    res.writeHead(200, head)
    fs.createReadStream(path).pipe(res)
  }

})
app.get('/img1',function(req,res){
  fs.readFile('assets/backBtn.png',function(error,data){
    res.writeHead(200,{ 'Content-Type': 'text/html'});
    res.end(data);
  
  })
})
app.get('/img2',function(req,res){
  fs.readFile('assets/name.png',function(error,data){
    res.writeHead(200,{ 'Content-Type': 'text/html'});
    res.end(data);
  
  })
})

app.listen(3000, function () {
  console.log('Listening on port 3000!')
})
