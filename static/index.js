
async function sendData() {


    const statusDiv = document.getElementById('status');
    statusDiv.innerText = 'Отправка...';


    if (!token || !chat_id || !text) {
    statusDiv.innerText = 'Заполните все поля!';
    return;
}

    console.log(document.getElementById('text').value);

    const payload = {
        token: document.getElementById('token').value,
        chat_id: document.getElementById('chat_id').value,
        message: {
            text: document.getElementById('text').value
    }
    };
    try {
        const response = await fetch('/send_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        console.log(result)
        if (result.status == "ok"){
            statusDiv.innerText = 'Сообщение успешно отправлено!';
        }
    } catch (error) {
        statusDiv.innerText = 'Ошибка запроса: ' + error;
    }
}
