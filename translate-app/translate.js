const axios = require('axios');
const fs = require('fs');

// Substitua pela sua chave de API do Google Cloud Vision
const API_KEY = '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';
const visionUrl = `https://vision.googleapis.com/v1/images:annotate?key=${API_KEY}`;

async function detectTextInImage(imagePath) {
    // Lendo a imagem como um Buffer
    const imageBase64 = fs.readFileSync(imagePath, { encoding: 'base64' });

    // Criando o objeto de solicitação para a API do Google Vision
    const requestObj = {
        requests: [
            {
                image: {
                    content: imageBase64,
                },
                features: [
                    {
                        type: "TEXT_DETECTION",
                    },
                ],
            },
        ],
    };

    try {
        // Enviando a solicitação para a API do Google Vision
        const response = await axios.post(visionUrl, requestObj);
        
        // Obtendo o texto detectado da resposta
        const textAnnotations = response.data.responses[0].textAnnotations;
        if (textAnnotations && textAnnotations.length > 0) {
            const detectedText = textAnnotations[0].description;
            
            // Criando um objeto JavaScript com os dados desejados
            const result = {
                detectedText: detectedText,
            };

            console.log(result);
            return result;
        } else {
            console.log("Nenhum texto detectado na imagem.");
            return null;
        }
    } catch (error) {
        console.error('Erro ao enviar a imagem para o Google Vision API:', error.message);
        return null;
    }
}

// Exemplo de uso da função
const imagePath = '/translate-app/translate-images/casamento-leonardo-talita.jpeg';
detectTextInImage(imagePath);