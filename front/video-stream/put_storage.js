// Creates a client
const { Storage } = require('@google-cloud/storage');
const projectId = ''    // 구글스토리지 내의 projectId
const keyFilename = ''  // 구글스토리지 콘솔에서 key파일 생성
const bucketName = '';  // 

const srcFilename = '2.mp4';
const destFilename = '2.mp4';

const storage = new Storage({projectId, keyFilename});

async function uploadEncryptedFile() {
    const options = {
        // The path to which the file should be uploaded, e.g. "file_encrypted.txt"
        destination: destFilename,
    };

    await storage.bucket(bucketName).upload(srcFilename, options);

    console.log();
}

uploadEncryptedFile().catch(console.error);